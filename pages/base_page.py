"""Base page object.

Все классы страниц наследуются от :class:`BasePage`. Он предоставляет
оболочку, учитывающую Allure, вокруг Selenium WebDriver, чтобы конкретные страницы могли
выражать намерение (click, enter_text, select_by_value) без повторения шаблонного ожидания
"""
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from config import EXPLICIT_WAIT_TIMEOUT


class BasePage:
    """Общие примитивы взаимодействия, используемые каждым объектом страницы."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_TIMEOUT)

    @allure.step("Открыть URL: {url}")
    def open(self, url: str):
        """Перейдите к *url*."""
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: tuple):
        """Дождитесь появления *локатора* в DOM и верните элемент.."""
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator: tuple):
        """Подождать хотя бы одного совпадения с *locator*, затем отобразите все совпадения."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    @allure.step("Нажать на элемент: {locator}")
    def click(self, locator: tuple):
        """Подождать, пока *локатор* станет кликабельным, и нажмите на него."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Введи текст '{text}' в: {locator}")
    def enter_text(self, locator: tuple, text: str):
        """Очистить поле ввода в *локаторе* и введите в него *текст*."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Выбрать значение в выпадающем списке '{value}': {locator}")
    def select_by_value(self, locator: tuple, value: str):
        """Выбрать ``<option>`` по его атрибуту ``value``."""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)

    @allure.step("Получить текст из элемента: {locator}")
    def get_text(self, locator: tuple) -> str:
        """Возвратить видимый текст элемента по адресу *locator*."""
        return self.find_element(locator).text

    def get_texts(self, locator: tuple) -> list[str]:
        """Возвратить видимый текст каждого элемента, соответствующего *locator*."""
        elements = self.find_elements(locator)
        return [el.text for el in elements]

    def wait_for_element(self, locator: tuple, timeout: int = EXPLICIT_WAIT_TIMEOUT):
        """Подождать до *timeout* секунд, пока не появится *locator*."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = EXPLICIT_WAIT_TIMEOUT):
        """Подождать до *timeout* секунд, пока *locator* станет доступным для нажатия."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll_to_element(self, element):
        """Прокрутить элемент в вертикальном центре области просмотра."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            element
        )
