import random

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = BasePage.BASE_URL

    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-12")

    @allure.step("Open main page")
    def open_main_page(self):
        self.open(self.URL)

    @allure.step("Search for '{keyword}'")
    def search(self, keyword: str):
        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Get all simple products from main page")
    def get_products_with_cart_button(self) -> list[dict]:
        products = []
        seen_ids = set()
        cards = self.find_elements(self.PRODUCT_CARDS)
        for card in cards:
            try:
                cart_btn = card.find_element(By.CSS_SELECTOR, "a.productcart")
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

    @allure.step("Select {count} random products from main page")
    def get_random_products(self, count: int) -> list[dict]:
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
