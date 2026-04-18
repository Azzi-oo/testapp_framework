import time

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, ".productname h1 span")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "ul.productpagecart a.cart")

    @allure.step("Set product quantity to {quantity}")
    def set_quantity(self, quantity: int):
        qty_input = self.find_element(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    @allure.step("Click Add to Cart")
    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Add product to cart: '{product_url}' qty={quantity}")
    def open_and_add_to_cart(self, product_url: str, quantity: int):
        """Navigate to product page, set quantity, and add to cart."""
        self.open(product_url)
        self.set_quantity(quantity)
        self.add_to_cart()
        time.sleep(2)
