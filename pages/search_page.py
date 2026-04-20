"""Страница результатов поиска.

Открывается после отправки поискового запроса в заголовке любой страницы.
"""
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchPage(BasePage):
    """Cтраница результатов поиска."""

    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".fixed_wrapper a.prdocutname")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnails.grid .thumbnail")
    PRODUCT_GRID = (By.CSS_SELECTOR, ".thumbnails.grid")

    SORT_NAME_ASC = "pd.name-ASC"

    @allure.step("Сортировать результаты поиска по: {sort_value}")
    def sort_by(self, sort_value: str):
        """Выбрать указанный параметр сортировки и дождитесь перезагрузки сетки."""
        self.select_by_value(self.SORT_DROPDOWN, sort_value)
        self.wait_for_element(self.PRODUCT_GRID)

    @allure.step("Получить ссылки на товары из результатов поиска")
    def get_product_links(self) -> list[dict]:
        """Для каждого результата возвращаю ``[{"name": ..., "link": ...}]``."""
        products = []
        name_elements = self.find_elements(self.PRODUCT_NAMES)
        for el in name_elements:
            products.append({
                "name": el.text,
                "link": el.get_attribute("href"),
            })
        return products

    @allure.step("Получить названия товаров из результатов поиска")
    def get_product_names(self) -> list[str]:
        """Возвращать только заголовки результатов поиска в порядке их отображения."""
        return self.get_texts(self.PRODUCT_NAMES)

    @allure.step("Получить отсортированные ссылки на товары по ключевому слову '{keyword}'")
    def search_and_sort(self, keyword: str) -> list[dict]:
        """Вспомогательная функция: открыть главную страницу, выполнить поиск по *ключевому слову*,
        отсортировать по алфавиту, вернуться по ссылкам."""
        from pages.main_page import MainPage
        main = MainPage(self.driver)
        main.open_main_page()
        main.search(keyword)
        self.sort_by(self.SORT_NAME_ASC)
        return self.get_product_links()
