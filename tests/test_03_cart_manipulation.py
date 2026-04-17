import random
import time

import allure
import pytest
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@allure.epic("Shopping Flow")
@allure.feature("Cart Manipulation")
@pytest.mark.cart
class TestCartManipulation:
    """Test Case 3: Add 5 random products from main page with random quantity,
    remove even-numbered products, check total."""

    @allure.story("Add products, remove even-numbered, verify total")
    @allure.title("Add 5 random products, remove even-numbered from cart, verify total")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_random_remove_even_verify_total(self, driver):
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)

        # Step 1: Open main page and get available products
        with allure.step("Open main page and collect available products"):
            main_page.open_main_page()
            all_products = main_page.get_products_with_cart_button()
            # Deduplicate by product_id
            seen_ids = set()
            unique_products = []
            for p in all_products:
                if p["product_id"] and p["product_id"] not in seen_ids:
                    seen_ids.add(p["product_id"])
                    unique_products.append(p)
            assert len(unique_products) >= 5, (
                f"Expected at least 5 unique products, got {len(unique_products)}"
            )

        # Step 2: Randomly select 5 products
        with allure.step("Randomly select 5 unique products"):
            selected = random.sample(unique_products, 5)
            allure.attach(
                "\n".join(
                    f"{i+1}. {p['name']} ({p['price']})"
                    for i, p in enumerate(selected)
                ),
                name="Selected products",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Step 3: Add each product with random quantity
        added_products = []
        for i, product in enumerate(selected):
            qty = random.randint(1, 5)
            with allure.step(
                f"Add product {i+1}: '{product['name']}' with qty={qty}"
            ):
                driver.get(product["link"])
                product_page.set_quantity(qty)
                product_page.add_to_cart()
                added_products.append({
                    "name": product["name"],
                    "quantity": qty,
                })
                time.sleep(2)

        # Step 4: Go to cart
        with allure.step("Open cart page"):
            cart_page.open_cart()

        # Step 5: Verify 5 items in cart
        with allure.step("Verify cart has 5 items"):
            rows_data = cart_page.get_cart_rows_data()
            assert len(rows_data) == 5, (
                f"Expected 5 items in cart, got {len(rows_data)}"
            )
            allure.attach(
                "\n".join(
                    f"{i+1}. {r['name']} - ${r['unit_price']} x {r['quantity']} "
                    f"= ${r['total_price']}"
                    for i, r in enumerate(rows_data)
                ),
                name="Cart contents before removal",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Step 6: Remove even-numbered products (2nd and 4th, indices 1 and 3)
        with allure.step("Remove even-numbered products (2nd and 4th)"):
            # Remove 4th first (higher index) to avoid index shifting
            cart_page.remove_product(3)
            time.sleep(1)
            cart_page.remove_product(1)
            time.sleep(1)

        # Step 7: Verify 3 items remain
        with allure.step("Verify 3 items remain in cart"):
            rows_data = cart_page.get_cart_rows_data()
            assert len(rows_data) == 3, (
                f"Expected 3 items after removal, got {len(rows_data)}"
            )
            allure.attach(
                "\n".join(
                    f"{i+1}. {r['name']} - ${r['unit_price']} x {r['quantity']} "
                    f"= ${r['total_price']}"
                    for i, r in enumerate(rows_data)
                ),
                name="Cart contents after removal",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Step 8: Verify cart sub-total
        with allure.step("Verify cart sub-total matches expected"):
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
