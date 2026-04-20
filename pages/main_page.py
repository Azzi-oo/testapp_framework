"""Главная (домашняя) страница.

Предоставляет доступ к вспомогательным функциям поиска и «случайного выбора товаров»,
используемым в тестах процесса покупок.
"""
import random

import allure
from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница магазина."""

    URL = BASE_URL

    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    CART_BUTTONS = (By.CSS_SELECTOR, "a.productcart")
    CARD_ANCESTOR_XPATH = "./ancestor::div[contains(@class,'col-')][1]"

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        """Перейти на главную страницу."""
        self.open(self.URL)

    @allure.step("Поиск по '{keyword}'")
    def search(self, keyword: str):
        """Ввести *ключевое слово* в поле поиска в заголовке и отправьте запрос."""
        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Поиск простых товаров на главной странице")
    def get_products_with_cart_button(self) -> list[dict]:
        """Возвращать товары, имеющиеся в наличии и представленные в одном варианте, на главную страницу.

        Пропускает варианты товаров, кнопка «Добавить в корзину» которых ведет на страницу с подробным описанием товара (тег ``href`` не заканчивается на ``#``) и
        удаляет дубликаты по ``data-id``.
        """
        products = []
        seen_ids = set()
        cart_buttons = self.find_elements(self.CART_BUTTONS)
        for cart_btn in cart_buttons:
            try:
                card = cart_btn.find_element(By.XPATH, self.CARD_ANCESTOR_XPATH)
                href = cart_btn.get_attribute("href")
                if not (href and href.endswith("#")):
                    continue

                product_id = cart_btn.get_attribute("data-id")
                if not product_id or product_id in seen_ids:
                    continue
                seen_ids.add(product_id)

                name_el = card.find_element(By.CSS_SELECTOR, "a.prdocutname")
                name = name_el.text
                link = name_el.get_attribute("href")

                try:
                    price = card.find_element(By.CSS_SELECTOR, ".oneprice").text
                except Exception:
                    try:
                        price = card.find_element(By.CSS_SELECTOR, ".pricenew").text
                    except Exception:
                        price = "$0.00"

                if name and link:
                    products.append({
                        "name": name,
                        "link": link,
                        "price": price,
                        "product_id": product_id,
                    })
            except Exception:
                continue
        return products

    @allure.step("Выбрать {count} рандомные товары на главной странице")
    def get_random_products(self, count: int) -> list[dict]:
        """Открыть главную страницу и получите *количество* уникальных случайных товаров."""
        self.open_main_page()
        products = self.get_products_with_cart_button()
        assert len(products) >= count, (
            f"Expected at least {count} unique products, got {len(products)}"
        )
        selected = random.sample(products, count)
        allure.attach(
            "\n".join(f"{i+1}. {p['name']} ({p['price']})" for i, p in enumerate(selected)),
            name="Selected products",
            attachment_type=allure.attachment_type.TEXT,
        )
        return selected
