"""Pytest fixtures: browser driver + one fixture per page object."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import IMPLICIT_WAIT_TIMEOUT
from pages.main_page import MainPage
from pages.category_page import CategoryPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.fixture
def driver():
    """Fresh Chrome WebDriver per test; quits automatically on teardown."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(IMPLICIT_WAIT_TIMEOUT)

    yield driver

    driver.quit()


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
def category_page(driver):
    return CategoryPage(driver)


@pytest.fixture
def search_page(driver):
    return SearchPage(driver)


@pytest.fixture
def product_page(driver):
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)
