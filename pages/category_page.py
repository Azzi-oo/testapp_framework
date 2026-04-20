"""Страница со списком категорий.

Используется в тестах сортировки для проверки порядка сортировки по названию/цене.
"""
import allure
from selenium.webdriver.common.by import By

from config import CATEGORY_URL
from pages.base_page import BasePage


class CategoryPage(BasePage):
    """Страница со списком категорий."""

    URL = CATEGORY_URL

    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".fixed_wrapper a.prdocutname")
    PRODUCT_PRICES_ONE = (By.CSS_SELECTOR, ".pricetag .oneprice")
    PRODUCT_PRICES_NEW = (By.CSS_SELECTOR, ".pricetag .pricenew")
    PRODUCT_GRID = (By.CSS_SELECTOR, ".thumbnails.grid")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnail")

    SORT_NAME_ASC = "pd.name-ASC"
    SORT_NAME_DESC = "pd.name-DESC"
    SORT_PRICE_ASC = "p.price-ASC"
    SORT_PRICE_DESC = "p.price-DESC"

    @allure.step("Открыть страницу категории")
    def open_category(self):
        """Перейти на страницу настроенной категории.."""
        self.open(self.URL)

    @allure.step("Сортировать по: {sort_value}")
    def sort_by(self, sort_value: str):
        """Выбрать указанный параметр сортировки и дождитесь перезагрузки сетки.."""
        self.select_by_value(self.SORT_DROPDOWN, sort_value)
        self.wait_for_element(self.PRODUCT_GRID)

    @allure.step("Получить все названия продуктов")
    def get_product_names(self) -> list[str]:
        """Возвратить видимые названия товаров в порядке их отображения в списке.."""
        return self.get_texts(self.PRODUCT_NAMES)

    @allure.step("Получить все цены на продукцию")
    def get_product_prices(self) -> list[float]:
        """Возвратить видимые цены товаров в порядке их отображения в списке."""
        prices = []
        cards = self.find_elements(self.PRODUCT_CARDS)
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
