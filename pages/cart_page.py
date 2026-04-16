import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_URL = BasePage.BASE_URL + "index.php?rt=checkout/cart"

    CART_TABLE = (By.CSS_SELECTOR, ".contentpanel table, .contentpanel form")
    CART_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    PRODUCT_NAME_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(2) a")
    UNIT_PRICE_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(4) .price")
    TOTAL_PRICE_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(6) .price")
    QUANTITY_INPUT_IN_ROW = (By.CSS_SELECTOR, "td:nth-child(5) input[type='text']")
    REMOVE_BUTTON_IN_ROW = (By.CSS_SELECTOR, "td a.btn")
    UPDATE_BUTTON = (By.ID, "cart_update")
    CART_TOTAL = (By.CSS_SELECTOR, ".contentpanel .cart_total .totalamount .bold")
    EMPTY_CART = (By.CSS_SELECTOR, ".empty_cart")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a.btn.btn-default")

    @allure.step("Open cart page")
    def open_cart(self):
        self.open(self.CART_URL)

    @allure.step("Get number of items in cart")
    def get_cart_items_count(self) -> int:
        try:
            rows = self.find_elements(self.CART_ROWS)
            return len(rows)
        except Exception:
            return 0

    @allure.step("Get cart rows data")
    def get_cart_rows_data(self) -> list[dict]:
        """Get all cart row data: name, unit_price, quantity, total_price."""
        rows_data = []
        rows = self.find_elements(self.CART_ROWS)
        for row in rows:
            try:
                name = row.find_element(*self.PRODUCT_NAME_IN_ROW).text.strip()

                unit_price_text = row.find_element(
                    *self.UNIT_PRICE_IN_ROW
                ).text.replace("$", "").replace(",", "").strip()
                unit_price = float(unit_price_text)

                qty_input = row.find_element(*self.QUANTITY_INPUT_IN_ROW)
                quantity = int(qty_input.get_attribute("value"))

                total_text = row.find_element(
                    *self.TOTAL_PRICE_IN_ROW
                ).text.replace("$", "").replace(",", "").strip()
                total_price = float(total_text)

                rows_data.append({
                    "name": name,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "total_price": total_price,
                    "row_element": row,
                })
            except Exception:
                continue
        return rows_data

    @allure.step("Find cheapest product in cart")
    def find_cheapest_product_index(self) -> int:
        rows_data = self.get_cart_rows_data()
        if not rows_data:
            return -1
        min_price = min(r["unit_price"] for r in rows_data)
        for i, r in enumerate(rows_data):
            if r["unit_price"] == min_price:
                return i
        return 0

    @allure.step("Update quantity for row {row_index} to {new_quantity}")
    def update_quantity(self, row_index: int, new_quantity: int):
        rows = self.find_elements(self.CART_ROWS)
        row = rows[row_index]
        qty_input = row.find_element(*self.QUANTITY_INPUT_IN_ROW)
        self.scroll_to_element(qty_input)
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))
        update_btn = self.find_element(self.UPDATE_BUTTON)
        self.scroll_to_element(update_btn)
        update_btn.click()
        time.sleep(2)

    @allure.step("Remove product at row {row_index}")
    def remove_product(self, row_index: int):
        rows = self.find_elements(self.CART_ROWS)
        row = rows[row_index]
        remove_btn = row.find_element(*self.REMOVE_BUTTON_IN_ROW)
        self.scroll_to_element(remove_btn)
        remove_btn.click()
        time.sleep(2)

    @allure.step("Get cart total")
    def get_cart_total(self) -> float:
        total_text = self.get_text(self.CART_TOTAL)
        return float(total_text.replace("$", "").replace(",", "").strip())

    @allure.step("Calculate expected total from rows")
    def calculate_expected_total(self) -> float:
        rows_data = self.get_cart_rows_data()
        return sum(r["unit_price"] * r["quantity"] for r in rows_data)
