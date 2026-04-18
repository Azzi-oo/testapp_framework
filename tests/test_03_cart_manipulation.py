import random

import allure
import pytest


@allure.epic("Shopping Flow")
@allure.feature("Cart Manipulation")
@pytest.mark.cart
class TestCartManipulation:
    """Тест-кейс 3: Добавить 5 случайных товаров, удалить четные, проверить итоговую сумму."""

    @allure.story("Добавить товары, удалить товары с четными номерами, проверить общую сумму.")
    @allure.title("Добавить 5 случайных товаров, удалить четные из корзины, проверить общую сумму.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_random_remove_even_verify_total(self, main_page, product_page, cart_page):
        # Select 5 random products from main page
        selected = main_page.get_random_products(5)

        # Add each product with random quantity
        for product in selected:
            product_page.open_and_add_to_cart(product["link"], random.randint(1, 5))

        # Open cart and verify 5 items
        cart_page.open_cart()
        assert len(cart_page.get_cart_rows_data()) == 5

        # Remove even-numbered products (2nd, 4th)
        cart_page.remove_even_products()
        assert len(cart_page.get_cart_rows_data()) == 3

        # Verify sub-total
        cart_page.assert_subtotal_matches()
