"""Project configuration.

Values can be overridden via environment variables so the same code can run
against staging/prod or a local mirror without edits. Import from this module
instead of hardcoding URLs or timeouts inside page objects.
"""
import os


BASE_URL = os.environ.get("BASE_URL", "https://automationteststore.com/")

CATEGORY_PATH = "index.php?rt=product/category&path=68"
CART_PATH = "index.php?rt=checkout/cart"

CATEGORY_URL = BASE_URL + CATEGORY_PATH
CART_URL = BASE_URL + CART_PATH

EXPLICIT_WAIT_TIMEOUT = int(os.environ.get("EXPLICIT_WAIT_TIMEOUT", "15"))
IMPLICIT_WAIT_TIMEOUT = int(os.environ.get("IMPLICIT_WAIT_TIMEOUT", "10"))
