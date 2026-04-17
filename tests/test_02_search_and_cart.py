import random
import time

import allure
import pytest
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@allure.epic("Shopping Flow")
@allure.feature("Search and Cart")
@pytest.mark.search_cart
class TestSearchAndCart:
    """Тест-кейс 2: Поиск, сортировка, добавить карту, и проверка итоговой суммы после удвоения дещевой карты"""

    @allure.story("Поиск, добавление товаров, изменение содержимого корзины, проверка общей суммы.")
    @allure.title("Поиск 'shirt', добавить 2-й и 3-й товары, удвоить самый дешевый товар количество, проверить итоговую сумму.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_add_and_verify_cart(self, driver):
        main_page = MainPage(driver)
        search_page = SearchPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Открыть главную страницу и выполните поиск 'shirt'"):
            main_page.open_main_page()
            main_page.search("shirt")

        with allure.step("Сортировать результаты поиска по Name A-Z"):
            search_page.sort_by(SearchPage.SORT_NAME_ASC)

        with allure.step("Отсортированный список товаров"):
            products = search_page.get_product_links()
            assert len(products) >= 3, (
                f"Expected at least 3 search results, got {len(products)}"
            )
            allure.attach(
                "\n".join(f"{i+1}. {p['name']}" for i, p in enumerate(products)),
                name="Sorted search results",
                attachment_type=allure.attachment_type.TEXT,
            )

        second_product = products[1]
        qty_second = random.randint(2, 5)
        with allure.step(
            f"Add 2nd product '{second_product['name']}' with qty={qty_second}"
        ):
            driver.get(second_product["link"])
            product_page.set_quantity(qty_second)
            product_page.add_to_cart()
            time.sleep(2)

        with allure.step("Вернуться к результатам поиска"):
            driver.back()
            driver.back()
            search_page.sort_by(SearchPage.SORT_NAME_ASC)

        products = search_page.get_product_links()
        third_product = products[2]
        qty_third = random.randint(2, 5)
        with allure.step(
            f"Add 3rd product '{third_product['name']}' with qty={qty_third}"
        ):
            driver.get(third_product["link"])
            product_page.set_quantity(qty_third)
            product_page.add_to_cart()
            time.sleep(2)

        with allure.step("Открыть страницу корзины"):
            cart_page.open_cart()

        with allure.step("Убедитесь, что в корзине 2 товара."):
            rows_data = cart_page.get_cart_rows_data()
            assert len(rows_data) == 2, (
                f"Expected 2 items in cart, got {len(rows_data)}"
            )

        with allure.step("Найти самый дешевый товар и удвойте его количество."):
            cheapest_idx = cart_page.find_cheapest_product_index()
            current_qty = rows_data[cheapest_idx]["quantity"]
            new_qty = current_qty * 2
            allure.attach(
                f"Cheapest: {rows_data[cheapest_idx]['name']} "
                f"(${rows_data[cheapest_idx]['unit_price']})\n"
                f"Current qty: {current_qty}, New qty: {new_qty}",
                name="Cheapest product details",
                attachment_type=allure.attachment_type.TEXT,
            )
            cart_page.update_quantity(cheapest_idx, new_qty)

        with allure.step("Проверьте, соответствует ли итоговая сумма в корзине ожидаемым значениям."):
            expected_total = cart_page.calculate_expected_total()
            actual_total = cart_page.get_cart_subtotal()
            allure.attach(
                f"Expected sub-total: ${expected_total:.2f}\n"
                f"Actual sub-total: ${actual_total:.2f}",
                name="Total comparison",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert abs(actual_total - expected_total) < 0.01, (
                f"Cart sub-total mismatch: expected ${expected_total:.2f}, "
                f"got ${actual_total:.2f}"
            )
