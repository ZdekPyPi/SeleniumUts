from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import time

CAPABILITIES = {
    "browserName": "chrome",
    "version":     "110.0",
    "name":        "default",
    "enableVNC"  : True,
    "enableVideo": False,
    "sessionTimeout": "30m"
}

DEFAULT_OPTIONS = [
    #"--disable-web-security",
    "--verbose",
    #"--no-sandbox",
    "--disable-infobars",
    "--disable-extensions",
    "--disable-notifications",
    "--disable-gpu",
    '--start-maximized',
    '--disable-blink-features=AutomationControlled',
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
]


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

class CustomRemoteDriver(RemoteWebDriver):
    def create_web_element(self, element_id):
        return CWebElement(self, element_id)


class SeleniumUts:
    driver = None

    def close(self):
        """
        Desc:
            Close the browser.\n
        Args: None
        """
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_loads(self, tm=5):
        wait = WebDriverWait(self.driver, 60)
        wt = lambda a: self.driver.execute_script("return document.readyState==\"complete\";")
        wait.until(wt)
        time.sleep(tm)

    def open_page(self,page):
        """
        Desc:
            Open a page in the browser.\n
            and wait for it to load.\n
        Args:
            - ``page`` - The URL of the page to be opened.
        Returns:
            - The WebDriver instance.
        """
        self.driver.get(page)
        self.driver.implicitly_wait(2)
        self.wait_loads()

        return self.driver

    def wait_xpath(self,path,time=20,throw=True):
        """
        Desc:
            Wait for an element to be visible using its XPATH.\n
        Args:
            - ``path`` - The XPATH of the element to be waited for.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 20 seconds.
            - ``throw`` - If True, raises an exception if the element is not found within the time limit.
        Returns:
            - The WebElement if found, otherwise None.
        """
        try:
            element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located((By.XPATH, path)))
            return element
        except:
            if throw: raise
            return None

    def scroll_end(self):
        """
        Desc:
            Scroll to the end of the page.\n
        Args: None
        """

        get_pos = lambda:self.driver.execute_script("return document.documentElement.scrollTop")

        while True:
            atual_pos = get_pos()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            future_pos = get_pos()
            if  future_pos == atual_pos:
                break

    def setupSelenium(
            self,
            host,
            name="default",
            use_selenoid=False,
            cust_opt = [],
            remove_default_options=False,
            download_path=None,
            selenoid_browser=("chrome","128.0")
        ) -> webdriver:
        
        
        #===================== OPTIONS ==============================
        options = []
        if not remove_default_options:
            options = DEFAULT_OPTIONS
        options += cust_opt

        web_options = uc.ChromeOptions() if not use_selenoid else webdriver.ChromeOptions()
        for op in options: 
            web_options.add_argument(op)

        web_options.headless = False

        #==================== PREFERENCES ===========================
        prefs = {
            "download.default_directory"             : download_path,
            "download.directory_upgrade"             : True,
            "download.prompt_for_download"           : False,
            "safebrowsing.enabled"                   : False,
            "credentials_enable_service"             : False,
            "profile.password_manager_enabled"       : False,
            "autofill.profile_enabled"               : False,
            "plugins.always_open_pdf_externally"     : True,
            "profile.password_manager_leak_detection": False,
        }
        web_options.add_experimental_option("prefs", prefs)
    

        #================== START BROWSER ===========================

        if use_selenoid:
            web_options.add_experimental_option("useAutomationExtension", False)
            web_options.add_experimental_option("excludeSwitches", ["enable-automation"])

            CAPABILITIES["name"]        = name
            CAPABILITIES["browserName"] = selenoid_browser[0]
            CAPABILITIES["version"]     = selenoid_browser[1]
            web_options.set_capability(name="selenoid:options", value=CAPABILITIES)
            web_options.set_capability(name="browserName",      value=CAPABILITIES["browserName"])

            self.driver = CustomRemoteDriver(command_executor=host, options=web_options)
        else:
            self.driver = uc.Chrome(options=web_options)

        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        return self.driver