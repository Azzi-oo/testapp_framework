import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class BasePage:
    BASE_URL = "https://automationteststore.com/"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Open URL: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Find element: {locator}")
    def find_element(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Find all elements: {locator}")
    def find_elements(self, locator: tuple):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    @allure.step("Click element: {locator}")
    def click(self, locator: tuple):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Enter text '{text}' into: {locator}")
    def enter_text(self, locator: tuple, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Select dropdown option by value '{value}': {locator}")
    def select_by_value(self, locator: tuple, value: str):
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)

    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: tuple) -> str:
        return self.find_element(locator).text

    def get_texts(self, locator: tuple) -> list[str]:
        elements = self.find_elements(locator)
        return [el.text for el in elements]

    def wait_for_element(self, locator: tuple, timeout: int = 15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = 15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            element
        )
