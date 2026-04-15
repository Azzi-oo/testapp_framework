import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CategoryPage(BasePage):
    # Apparel & accessories category with 8 products
    CATEGORY_URL = BasePage.BASE_URL + "index.php?rt=product/category&path=68"

    # Locators
    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".fixed_wrapper a.prdocutname")
    PRODUCT_PRICES_ONE = (By.CSS_SELECTOR, ".pricetag .oneprice")
    PRODUCT_PRICES_NEW = (By.CSS_SELECTOR, ".pricetag .pricenew")
    PRODUCT_GRID = (By.CSS_SELECTOR, ".thumbnails.grid")

    # Sort option values
    SORT_NAME_ASC = "pd.name-ASC"
    SORT_NAME_DESC = "pd.name-DESC"
    SORT_PRICE_ASC = "p.price-ASC"
    SORT_PRICE_DESC = "p.price-DESC"

    @allure.step("Open category page")
    def open_category(self):
        self.open(self.CATEGORY_URL)

    @allure.step("Sort by: {sort_value}")
    def sort_by(self, sort_value: str):
        self.select_by_value(self.SORT_DROPDOWN, sort_value)
        self.wait_for_element(self.PRODUCT_GRID)

    @allure.step("Get all product names")
    def get_product_names(self) -> list[str]:
        return self.get_texts(self.PRODUCT_NAMES)

    @allure.step("Get all product prices")
    def get_product_prices(self) -> list[float]:
        prices = []
        cards = self.find_elements(
            (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-12")
        )
        for card in cards:
            try:
                price_el = card.find_element(By.CSS_SELECTOR, ".oneprice")
            except Exception:
                try:
                    price_el = card.find_element(By.CSS_SELECTOR, ".pricenew")
                except Exception:
                    continue
            price_text = price_el.text.replace("$", "").replace(",", "").strip()
            if price_text:
                prices.append(float(price_text))
        return prices
