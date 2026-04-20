"""Cтраница корзины покупок.

Обработчики событий считывают строки в корзине, изменяют количество,
удаляют товары и проверяют промежуточную сумму.
"""
import time

import allure
from selenium.webdriver.common.by import By

from config import CART_URL
from pages.base_page import BasePage


class CartPage(BasePage):
    """Shopping-cart page."""

    URL = CART_URL

    ALL_TABLE_ROWS = (By.CSS_SELECTOR, ".product-list table.table tr")
    PRODUCT_NAME_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(2) a")
    UNIT_PRICE_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(4)")
    TOTAL_PRICE_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(6)")
    QUANTITY_INPUT_IN_ROW = (By.CSS_SELECTOR, "input[name^='quantity[']")
    REMOVE_BUTTON_IN_ROW = (By.CSS_SELECTOR, "a[href*='remove=']")
    UPDATE_BUTTON = (By.ID, "cart_update")
    SUB_TOTAL = (By.CSS_SELECTOR, "#totals_table tr:first-child td:nth-child(2) span.bold")

    @allure.step("Открыть страницу корзины")
    def open_cart(self):
        """Перейти на страницу корзины"""
        self.open(self.URL)

    def _get_product_rows(self):
        """Возвращать только те `<tr>`, которые содержат `<td>` (пропускать строку заголовка)."""
        all_rows = self.find_elements(self.ALL_TABLE_ROWS)
        return [r for r in all_rows if r.find_elements(By.TAG_NAME, "td")]

    @allure.step("Получить данные о строках корзины")
    def get_cart_rows_data(self) -> list[dict]:
        """Возвращать ``[{name, unit_price, quantity, total_price}]`` для каждой строки."""
        rows_data = []
        for row in self._get_product_rows():
            try:
                name = row.find_element(*self.PRODUCT_NAME_IN_ROW).text.strip()
                unit_price = float(
                    row.find_element(*self.UNIT_PRICE_IN_ROW)
                    .text.replace("$", "").replace(",", "").strip()
                )
                quantity = int(
                    row.find_element(*self.QUANTITY_INPUT_IN_ROW)
                    .get_attribute("value")
                )
                total_price = float(
                    row.find_element(*self.TOTAL_PRICE_IN_ROW)
                    .text.replace("$", "").replace(",", "").strip()
                )
                rows_data.append({
                    "name": name,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "total_price": total_price,
                })
            except Exception:
                continue
        return rows_data

    @allure.step("Обновить количество для строки {row_index} to {new_quantity}")
    def update_quantity(self, row_index: int, new_quantity: int):
        """Установить значение параметра *row_index* равным *new_quantity* и нажмите "Обновить"."""
        rows = self._get_product_rows()
        qty_input = rows[row_index].find_element(*self.QUANTITY_INPUT_IN_ROW)
        self.scroll_to_element(qty_input)
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))
        update_btn = self.find_element(self.UPDATE_BUTTON)
        self.scroll_to_element(update_btn)
        update_btn.click()
        time.sleep(2)

    @allure.step("Удалить товар в строке {row_index}")
    def remove_product(self, row_index: int):
        """Нажать на значок удаления в строке по адресу *row_index*.."""
        rows = self._get_product_rows()
        remove_btn = rows[row_index].find_element(*self.REMOVE_BUTTON_IN_ROW)
        self.scroll_to_element(remove_btn)
        remove_btn.click()
        time.sleep(2)

    @allure.step("Получить итоговую сумму корзины")
    def get_cart_subtotal(self) -> float:
        """Обработать и вернуть отображаемую в корзине промежуточную сумму."""
        text = self.get_text(self.SUB_TOTAL)
        return float(text.replace("$", "").replace(",", "").strip())

    @allure.step("Рассчитать ожидаемую сумму по строкам")
    def calculate_expected_total(self) -> float:
        """Сложить значение ``unit_price * quantity`` по текущим строкам."""
        rows_data = self.get_cart_rows_data()
        return sum(r["unit_price"] * r["quantity"] for r in rows_data)

    @allure.step("Удвоить количество самого дешевого товара")
    def double_cheapest_quantity(self):
        """Найти самый дешевый товар по цене за единицу и удвойте его количество."""
        rows = self.get_cart_rows_data()
        cheapest_idx = min(range(len(rows)), key=lambda i: rows[i]["unit_price"])
        current_qty = rows[cheapest_idx]["quantity"]
        new_qty = current_qty * 2
        allure.attach(
            f"Product: {rows[cheapest_idx]['name']}\n"
            f"Unit price: ${rows[cheapest_idx]['unit_price']}\n"
            f"Qty: {current_qty} -> {new_qty}",
            name="Cheapest product details",
            attachment_type=allure.attachment_type.TEXT,
        )
        self.update_quantity(cheapest_idx, new_qty)

    @allure.step("Удалить товары с четными номерами (2-й, 4-й)")
    def remove_even_products(self):
        """Удаляет строки, индексируемые с 1 (2-я, 4-я и т. д.).

        Итерация начинается с наивысшего индекса и идет вниз, поэтому более ранние удаления не
        сдвигают индексы строк, которые еще предстоит удалить.
        """
        cart_size = len(self._get_product_rows())
        even_indices = [i for i in range(1, cart_size, 2)]
        for idx in reversed(even_indices):
            self.remove_product(idx)

    @allure.step("Проверить, соответствует ли итоговая сумма в корзине ожидаемым значениям")
    def assert_subtotal_matches(self):
        """Ошибка будет допущена, если промежуточная сумма на странице отличается от пересчитанной общей суммы."""
        expected = self.calculate_expected_total()
        actual = self.get_cart_subtotal()
        allure.attach(
            f"Expected: ${expected:.2f}\nActual: ${actual:.2f}",
            name="Sub-total comparison",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert abs(actual - expected) < 0.01, (
            f"Cart sub-total mismatch: expected ${expected:.2f}, got ${actual:.2f}"
        )
