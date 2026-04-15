import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = BasePage.BASE_URL

    # Locators
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-12")
    PRODUCT_NAME_LINKS = (By.CSS_SELECTOR, "a.prdocutname")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "a.productcart")
    CART_BADGE = (By.CSS_SELECTOR, ".label.label-orange")

    @allure.step("Open main page")
    def open_main_page(self):
        self.open(self.URL)

    @allure.step("Search for '{keyword}'")
    def search(self, keyword: str):
        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Get all products with Add to Cart button on main page")
    def get_products_with_cart_button(self) -> list[dict]:
        """Returns list of dicts with product name, price, and link for products
        that can be directly added to cart (href='#')."""
        products = []
        cards = self.find_elements(self.PRODUCT_CARDS)
        for card in cards:
            try:
                cart_btn = card.find_element(By.CSS_SELECTOR, "a.productcart")
                href = cart_btn.get_attribute("href")
                # Products that can be added directly have href="#" or no href
                name_el = card.find_element(By.CSS_SELECTOR, "a.prdocutname")
                name = name_el.text
                link = name_el.get_attribute("href")
                product_id = cart_btn.get_attribute("data-id")

                # Try to get price
                try:
                    price_el = card.find_element(By.CSS_SELECTOR, ".oneprice")
                    price = price_el.text
                except Exception:
                    try:
                        price_el = card.find_element(By.CSS_SELECTOR, ".pricenew")
                        price = price_el.text
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
