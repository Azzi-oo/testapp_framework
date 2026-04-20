"""Centralized test data.

Tests should import values from here rather than inlining literals so that
scenarios can be tuned from one place (e.g. switching the search keyword or
adjusting quantity ranges without editing individual test bodies).
"""

SEARCH_KEYWORD = "shirt"

MIN_SORTED_PRODUCTS = 4
MIN_SEARCH_RESULTS = 3

RANDOM_PRODUCT_COUNT = 5
EXPECTED_REMAINING_AFTER_EVEN_REMOVAL = 3

CART_MIN_QUANTITY = 1
CART_MAX_QUANTITY = 5

SEARCH_CART_MIN_QUANTITY = 2
SEARCH_CART_MAX_QUANTITY = 5

SEARCH_CART_PRODUCT_INDICES = (1, 2)
