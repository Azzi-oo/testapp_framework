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
    def test_sort_by_name_asc(self, driver):
        page = CategoryPage(driver)
        page.open_category()

        with allure.step("Сортировка по Name A - Z"):
            page.sort_by(CategoryPage.SORT_NAME_ASC)

        with allure.step("Verify product names are in ascending order"):
            names = page.get_product_names()
            assert len(names) >= 4, f"Expected at least 4 products, got {len(names)}"
            names_lower = [n.lower() for n in names]
            assert names_lower == sorted(names_lower), (
                f"Products are not sorted A-Z.\nActual: {names}"
            )

    @allure.story("Сортировка по имени")
    @allure.title("Продукты сортированы по Name Z-A")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_desc(self, driver):
        page = CategoryPage(driver)
        page.open_category()

        with allure.step("Сортировка по Name Z - A"):
            page.sort_by(CategoryPage.SORT_NAME_DESC)

        with allure.step("Verify product names are in descending order"):
            names = page.get_product_names()
            assert len(names) >= 4, f"Expected at least 4 products, got {len(names)}"
            names_lower = [n.lower() for n in names]
            assert names_lower == sorted(names_lower, reverse=True), (
                f"Products are not sorted Z-A.\nActual: {names}"
            )

    @allure.story("Сортировка по цене возрастания")
    @allure.title("Продукты сортированы по цене Low to High")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_asc(self, driver):
        page = CategoryPage(driver)
        page.open_category()

        with allure.step("Сортировка по цене Low > High"):
            page.sort_by(CategoryPage.SORT_PRICE_ASC)

        with allure.step("Verify product prices are in ascending order"):
            prices = page.get_product_prices()
            assert len(prices) >= 4, f"Expected at least 4 prices, got {len(prices)}"
            assert prices == sorted(prices), (
                f"Prices are not sorted Low>High.\nActual: {prices}"
            )

    @allure.story("Сортировка по цене убывания")
    @allure.title("Продукты сортированы по цене High to Low")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_desc(self, driver):
        page = CategoryPage(driver)
        page.open_category()

        with allure.step("Сортировка по цене High > Low"):
            page.sort_by(CategoryPage.SORT_PRICE_DESC)

        with allure.step("Verify product prices are in descending order"):
            prices = page.get_product_prices()
            assert len(prices) >= 4, f"Expected at least 4 prices, got {len(prices)}"
            assert prices == sorted(prices, reverse=True), (
                f"Prices are not sorted High>Low.\nActual: {prices}"
            )
