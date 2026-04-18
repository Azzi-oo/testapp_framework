import random

import allure
import pytest


@allure.epic("Shopping Flow")
@allure.feature("Search and Cart")
@pytest.mark.search_cart
class TestSearchAndCart:
    """Тест-кейс 2: Поиск, сортировка, добавить в корзину, проверка итоговой суммы после удвоения дешевого товара"""

    @allure.story("Поиск, добавление товаров, изменение содержимого корзины, проверка общей суммы.")
    @allure.title("Поиск 'shirt', добавить 2-й и 3-й товары, удвоить самый дешевый, проверить итоговую сумму.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_add_and_verify_cart(self, main_page, search_page, product_page, cart_page):
        # Search "shirt" and sort by name A-Z
        main_page.open_main_page()
        main_page.search("shirt")
        search_page.sort_by(search_page.SORT_NAME_ASC)

        products = search_page.get_product_links()
        assert len(products) >= 3
        search_url = search_page.driver.current_url

        # Add 2nd product with random quantity
        product_page.open_and_add_to_cart(products[1]["link"], random.randint(2, 5))

        # Return to search results, add 3rd product
        search_page.open(search_url)
        search_page.sort_by(search_page.SORT_NAME_ASC)
        products = search_page.get_product_links()
        product_page.open_and_add_to_cart(products[2]["link"], random.randint(2, 5))

        # Open cart, verify 2 items
        cart_page.open_cart()
        assert len(cart_page.get_cart_rows_data()) == 2

        # Double cheapest product quantity and verify total
        cart_page.double_cheapest_quantity()
        cart_page.assert_subtotal_matches()
