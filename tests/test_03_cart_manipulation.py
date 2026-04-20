"""Тест манипуляций с корзиной.

Тест-кейс 3: добавить N случайных товаров, удалить строки с четными индексами и проверить, что
промежуточная сумма корзины по-прежнему соответствует пересчитанной общей сумме.
"""

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
        selected = main_page.get_random_products(5)

        for product in selected:
            product_page.open_and_add_to_cart(product["link"], random.randint(1, 5))

        cart_page.open_cart()
        assert len(cart_page.get_cart_rows_data()) == 5

        cart_page.remove_even_products()
        assert len(cart_page.get_cart_rows_data()) == 3

        cart_page.assert_subtotal_matches()
