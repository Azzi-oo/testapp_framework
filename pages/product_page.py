import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, ".productname h1 span")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "ul.productpagecart a.cart")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productfilneprice .price .total-price")
    CART_SUCCESS = (By.CSS_SELECTOR, ".added_to_cart, .alert-success")

    @allure.step("Set product quantity to {quantity}")
    def set_quantity(self, quantity: int):
        qty_input = self.find_element(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    @allure.step("Click Add to Cart")
    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Get product name")
    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    @allure.step("Get product price")
    def get_product_price(self) -> float:
        price_text = self.get_text(self.PRODUCT_PRICE)
        return float(price_text.replace("$", "").replace(",", "").strip())
