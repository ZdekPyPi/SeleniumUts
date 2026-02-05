from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import time


class CWebElement(WebElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delayed_send(self, word, delay=0.5):
        """
        Desc:
            Send keys to the element with a delay between each character.\n
        Args:
         - ``word`` - The string to be sent to the element.
         - ``delay`` - The delay between each character in seconds.
            Default: 0.5 seconds.
        """
        for c in word:
            self.send_keys(c)
            time.sleep(delay)

    def focus(self):
        """Foca no elemento"""
        self.parent.execute_script("arguments[0].scrollIntoView(true);", self)
        time.sleep(0.5)
        self.parent.execute_script("arguments[0].focus();", self)
        return self

    def select_by_text(self, text):
        """Seleciona item em dropdown pelo texto visível"""
        Select(self).select_by_visible_text(text)
        return self

    def select_by_value(self, value):
        """Seleciona item em dropdown pelo valor"""
        Select(self).select_by_value(value)
        return self

    def click_js(self):
        """Clica no elemento usando JavaScript (evita toggle indesejado)"""
        self.driver.execute_script("arguments[0].click();", self)
        return self
