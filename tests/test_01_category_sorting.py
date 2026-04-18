import allure
import pytest
from pages.category_page import CategoryPage


@allure.epic("Product Catalog")
@allure.feature("Сортировка категории")
@pytest.mark.sorting
class TestCategorySorting:
    """Тест-кейс 1: Фильтр категорий — Сортировка по имени и цене"""

    @allure.story("Сортировка по имени")
    @allure.title("Продукты сортированы по Name A-Z")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_asc(self, category_page):
        category_page.open_category()
        category_page.sort_by(CategoryPage.SORT_NAME_ASC)

        names = category_page.get_product_names()
        assert len(names) >= 4
        names_lower = [n.lower() for n in names]
        assert names_lower == sorted(names_lower), f"Not sorted A-Z: {names}"

    @allure.story("Сортировка по имени")
    @allure.title("Продукты сортированы по Name Z-A")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_desc(self, category_page):
        category_page.open_category()
        category_page.sort_by(CategoryPage.SORT_NAME_DESC)

        names = category_page.get_product_names()
        assert len(names) >= 4
        names_lower = [n.lower() for n in names]
        assert names_lower == sorted(names_lower, reverse=True), f"Not sorted Z-A: {names}"

    @allure.story("Сортировка по цене возрастания")
    @allure.title("Продукты сортированы по цене Low to High")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_asc(self, category_page):
        category_page.open_category()
        category_page.sort_by(CategoryPage.SORT_PRICE_ASC)

        prices = category_page.get_product_prices()
        assert len(prices) >= 4
        assert prices == sorted(prices), f"Not sorted Low>High: {prices}"

    @allure.story("Сортировка по цене убывания")
    @allure.title("Продукты сортированы по цене High to Low")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_desc(self, category_page):
        category_page.open_category()
        category_page.sort_by(CategoryPage.SORT_PRICE_DESC)

        prices = category_page.get_product_prices()
        assert len(prices) >= 4
        assert prices == sorted(prices, reverse=True), f"Not sorted High>Low: {prices}"
