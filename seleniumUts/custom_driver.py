from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from seleniumUts.webelement import CWebElement
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class CustomRemoteDriver(RemoteWebDriver):
    def create_web_element(self, element_id):
        return CWebElement(self, element_id)


class CustomChromeDriver(Chrome):
    def create_web_element(self, element_id):
        return CWebElement(self, element_id)

    def find_element(
        self, by=By.ID, value=None, selenium_uts=None, time=None, custom_error=None
    ):
        # Faz a busca normal
        element = super().find_element(by, value)

        # Injeta as informações de busca no objeto CWebElement recém-criado
        if isinstance(element, CWebElement):
            element._found_by = by
            element._query_path = value
            element.selenium_uts = selenium_uts
            element.time = time
            element.custom_error = custom_error

        return element

    # É importante fazer o mesmo para find_elements (lista)
    def find_elements(
        self, by=By.ID, value=None, selenium_uts=None, time=None, custom_error=None
    ):
        elements = super().find_elements(by, value)
        for el in elements:
            if isinstance(el, CWebElement):
                el._found_by = by
                el._query_path = value
                el.selenium_uts = selenium_uts
                el.time = time
                el.custom_error = custom_error
        return elements
