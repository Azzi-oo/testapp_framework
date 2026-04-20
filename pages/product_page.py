"""Страница с подробной информацией о товаре.

Используется для добавления конкретного товара (по URL) в корзину в выбранном количестве.
"""
import time

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Страница с подробным описанием конкретного товара."""

    PRODUCT_NAME = (By.CSS_SELECTOR, ".productname h1 span")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "ul.productpagecart a.cart")

    @allure.step("Установить количество продукта на {quantity}")
    def set_quantity(self, quantity: int):
        """Заменить поле количества на *количество*."""
        qty_input = self.find_element(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    @allure.step("Нажать «Добавить в корзину»")
    def add_to_cart(self):
        """Нажать кнопку «Добавить в корзину» на странице товара."""
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Добавить товар в корзину: '{product_url}' qty={quantity}")
    def open_and_add_to_cart(self, product_url: str, quantity: int):
        """Открыть *product_url*, укажите *quantity*, нажмите «Добавить в корзину»."""
        self.open(product_url)
        self.set_quantity(quantity)
        self.add_to_cart()
        time.sleep(2)
