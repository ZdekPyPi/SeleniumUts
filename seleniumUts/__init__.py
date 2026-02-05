from seleniumUts.custom_driver import CustomChromeDriver, CustomRemoteDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from time import time, sleep
from pathlib import Path
from glob import glob
import base64

CAPABILITIES = {
    "browserName": "chrome",
    "version": "110.0",
    "name": "default",
    "enableVNC": True,
    "enableVideo": False,
    "sessionTimeout": "30m",
}

DEFAULT_OPTIONS = [
    # "--disable-web-security",
    "--verbose",
    # "--no-sandbox",
    "--disable-infobars",
    "--disable-extensions",
    "--disable-notifications",
    "--disable-dev-shm-usage",
    "--force-device-scale-factor=0.67",
    "--disable-gpu",
    "--start-maximized",
    "--kiosk-printing",
    "--disable-blink-features=AutomationControlled",
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
]


class SeleniumUts:
    driver = None

    default_download_path = None
    current_download_path = None

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
        """
        Desc:
            Wait for the page to load completely.\n
        Args:
            - ``tm`` - Additional time to wait after the page is loaded in seconds. Default is 5 seconds.
        Returns: None
        """
        wait = WebDriverWait(self.driver, tm)
        wt = lambda a: self.driver.execute_script(
            'return document.readyState=="complete";'
        )
        wait.until(wt)

    def open_page(self, page):
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

    def wait_xpath(self, path, time=20, multiple=False, throw=True, custom_error=None):
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
            if multiple:
                # Espera até que TODOS os elementos correspondentes estejam visíveis
                elements = WebDriverWait(self.driver, time).until(
                    lambda d: self.driver.find_elements(
                        By.XPATH,
                        path,
                        selenium_uts=self,
                        time=time,
                        custom_error=custom_error,
                    )
                )
                return elements
            else:
                element = WebDriverWait(self.driver, time).until(
                    lambda d: self.driver.find_element(
                        By.XPATH,
                        path,
                        selenium_uts=self,
                        time=time,
                        custom_error=custom_error,
                    )
                )
                return element
        except Exception:
            if throw:
                if custom_error:
                    raise Exception(custom_error)
                else:
                    raise
            return None

    def wait_css(self, selector, time=20, throw=True, custom_error=None):
        """
        Desc:
            Wait for an element to be visible using its CSS selector.\n
        Args:
            - ``selector`` - The CSS selector of the element to be waited for.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 20 seconds.
            - ``throw`` - If True, raises an exception if the element is not found within the time limit.
        Returns:
            - The WebElement if found, otherwise None.
        """
        try:
            element = WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except Exception:
            if throw:
                if custom_error:
                    raise Exception(custom_error)
                else:
                    raise
            return None

    def wait_id(self, element_id, time=10, throw=True, custom_error=None):
        """
        Desc:
            Wait for an element to be present using its ID.\n
        Args:
            - ``element_id`` - The ID of the element to be waited for.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 10 seconds.
            - ``throw`` - If True, raises an exception if the element is not found within the time limit.
        Returns:
            - The WebElement if found, otherwise None.
        """
        try:
            elem = WebDriverWait(self.driver, time).until(
                lambda d: self.driver.find_element(
                    By.ID,
                    element_id,
                    selenium_uts=self,
                    time=time,
                    custom_error=custom_error,
                )
            )
            return elem
        except Exception:
            if throw:
                if custom_error:
                    raise Exception(custom_error)
                else:
                    raise
            return None

    def scroll_end(self):
        """
        Desc:
            Scroll to the end of the page.\n
        Args: None
        """

        get_pos = lambda: self.driver.execute_script(
            "return document.documentElement.scrollTop"
        )

        while True:
            atual_pos = get_pos()
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            sleep(2)
            future_pos = get_pos()
            if future_pos == atual_pos:
                break

    def accept_alert(self, time=10):
        """
        Desc:
            Wait for an alert to be present and accept it.\n
        Args:
            - ``time`` - Maximum time to wait for the alert in seconds. Default is 10 seconds.
        Returns:
            - The text of the alert.
        """
        try:
            WebDriverWait(self.driver, time).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            txt = alert.text
            alert.accept()
            return txt
        except Exception:
            return None

    def disable_animations(self):
        css_kill_animations = """
        /* 1. Mata as durações */
        *, *::before, *::after {
            transition-duration: 0s !important;
            transition-delay: 0s !important;
            animation-duration: 0s !important;
            animation-delay: 0s !important;
        }

        /* 2. Força a visibilidade imediata de elementos que dependem de animação para aparecer */
        [style*="opacity: 0"],
        [style*="opacity:0"],
        .fade, .collapse, .hidden {
            opacity: 1 !important;
            display: block !important;
            visibility: visible !important;
        }

        /* 3. Reseta transformações que deixariam o elemento fora da tela (comum em slide-ins) */
        * {
            transform: none !important;
            perspective: none !important;
        }
                """

        self.add_style(css_kill_animations)

    def new_tab(self):
        """
        Desc:
            Open a new browser tab and switch to it.\n
        Returns: None
        """
        self.driver.execute_script("window.open('');")
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def switch_to_new_tab(self):
        """
        Desc:
            Switch to the most recently opened browser window.\n
        Returns: None
        """
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def close_current_tab(self):
        """
        Desc:
            Close the current browser tab and switch to the previous one.\n
        Returns: None
        """
        all_windows = self.driver.window_handles

        if len(all_windows) > 1:
            # 1. Identifica qual é a aba atual antes de fechar
            current_window = self.driver.current_window_handle

            # 2. Encontra o índice da aba atual na lista de abas
            current_index = all_windows.index(current_window)

            # 3. Fecha a aba atual
            self.driver.close()

            # 4. Define o destino: a aba anterior (index - 1)
            # ou a primeira aba se a atual for a única restando
            new_window = all_windows[current_index - 1]

            self.driver.switch_to.window(new_window)

    def back_main_tab(self):
        """
        Desc:
            Switch back to the first browser tab.\n
        Returns: None
        """
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[0])

    def go_to_tab(self, index):
        """
        Desc:
            Switch to a specific browser tab by index.\n
        Args:
            - ``index`` - The index of the tab to switch to (0-based).
        Returns: None
        """
        windows = self.driver.window_handles
        if index < len(windows):
            self.driver.switch_to.window(windows[index])

    def element_exists_xpath(self, xpath, time=5):
        """
        Desc:
            Check if an element exists by XPATH.\n
        Args:
            - ``xpath`` - The XPATH of the element to be checked.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 5 seconds.
        Returns:
            - True if the element exists, False otherwise.
        """
        try:
            WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def element_exists_css(self, selector, time=5):
        """
        Desc:
            Check if an element exists by CSS selector.\n
        Args:
            - ``selector`` - The CSS selector of the element to be checked.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 5 seconds.
        Returns:
            - True if the element exists, False otherwise.
        """
        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except Exception:
            return False

    def element_exists(self, by, value, time=5):
        """
        Desc:
            Check if an element exists by a given locator strategy.\n
        Args:
            - ``by`` - The locator strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).
            - ``value`` - The value of the locator.
            - ``time`` - Maximum time to wait for the element in seconds. Default is 5 seconds.
        Returns:
            - True if the element exists, False otherwise.
        """
        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def change_download_path(self, download_path):
        self.driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(Path(download_path).resolve())},
        )
        self.current_download_path = download_path

    def restore_download_path(self):
        self.driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {
                "behavior": "allow",
                "downloadPath": str(Path(self.default_download_path).resolve()),
            },
        )
        self.current_download_path = self.default_download_path

    def wait_downloads_done(
        self, timeout_start=10, timeout_end=60, file_path=None, escape=False
    ):
        temp_files = (
            lambda: glob(f"{self.current_download_path}/*.crdownload")
            + glob(f"{self.current_download_path}/*.tmp")
            + glob(f"{self.current_download_path}/*.part")
        )

        scape_files = lambda: glob(
            f"{self.current_download_path}/{glob.escape(file_path)}"
        )
        not_scape_files = lambda: glob(f"{self.current_download_path}/{file_path}")

        if file_path:
            start_time = time()
            while not (scape_files() if escape else not_scape_files()):
                if time() - start_time >= timeout_end:
                    raise Exception("Download file not detected")

            while temp_files():
                sleep(0.3)
            return scape_files() if escape else not_scape_files()

        # AGUARDA OS DOWNLOADS INICIAREM
        start_time = time()
        while not temp_files():
            if time() - start_time >= timeout_start:
                raise Exception("Download files not detected")

        while temp_files():
            sleep(0.3)

    def get_last_download_file(self):
        caminho_pasta = Path(self.current_download_path)
        if not caminho_pasta.exists():
            return None

        arquivos = [
            f
            for f in caminho_pasta.iterdir()
            if f.is_file() and not f.name.endswith((".crdownload", ".tmp", ".part"))
        ]
        if not arquivos:
            return None

        # Ordenamos pelo mtime (Modification Time)
        # No Windows e Linux, isso representa quando o download terminou de ser escrito.
        ultimo_arquivo = max(arquivos, key=lambda f: f.stat().st_mtime)

        return str(ultimo_arquivo.absolute())

    def full_screenshot(self, path):
        self.scroll_end()
        # 1. Pegar a altura total do documento via JavaScript
        total_height = self.driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        total_width = self.driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )

        self.driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": total_width,
                "height": total_height,
                "deviceScaleFactor": 1,
                "mobile": False,
            },
        )

        # 2. Redimensionar a janela para o tamanho total da página
        sleep(1)

        # 3. Tirar o print padrão
        self.driver.save_screenshot(path)

    def save_to_pdf(self, path, single_page=False):
        # O comando retorna um dicionário com os dados em Base64
        params = {"printBackground": True, "landscape": False}
        if single_page:
            # Dividimos por 96 porque o padrão de tela é 96 DPI
            dimensions = self.driver.execute_script("""
                return {
                    width: document.documentElement.offsetWidth / 96,
                    height: document.documentElement.scrollHeight / 96
                };
            """)

            params = {
                **params,
                "paperHeight": dimensions["height"],
                "marginTop": 0,
                "marginBottom": 0,
                "marginLeft": 0,
                "marginRight": 0,
                "pageRanges": "1",  # Garante que ele foque na primeira (e única) página
            }

        result = self.driver.execute_cdp_cmd("Page.printToPDF", params)

        # Salva o arquivo no diretório que você escolher agora
        with open(path, "wb") as f:
            f.write(base64.b64decode(result["data"]))

    def add_print_style(self):
        """
        Injeta regras de CSS para garantir que as cores e fundos
        sejam preservados durante a impressão/PDF.
        """
        css_code = """
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `
                @media print {
                    body, .info-bar, .container, .section h3 {
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                        color-adjust: exact !important;
                    }
                }
            `;
            document.getElementsByTagName('head')[0].appendChild(style);
        """
        self.driver.execute_script(css_code)

    def add_style(self, css_content):
        """
        Injeta um bloco de CSS dinamicamente na página atual.
        """
        script = """
            var style = document.createElement('style');
            style.type = 'text/css';
            if (style.styleSheet){
                style.styleSheet.cssText = arguments[0];
            } else {
                style.appendChild(document.createTextNode(arguments[0]));
            }
            document.getElementsByTagName('head')[0].appendChild(style);
        """
        self.driver.execute_script(script, css_content)

    def startRemoteSelenium(
        self,
        host,
        name="default",
        cust_opt=[],
        cust_prefs=[],
        remove_default_options=False,
        download_path=None,
        selenoid_browser=("chrome", "128.0"),
        profile=None,
    ) -> webdriver:
        self.default_download_path = download_path
        self.current_download_path = download_path

        # ===================== OPTIONS ==============================
        options = []
        if not remove_default_options:
            options = DEFAULT_OPTIONS
        options += cust_opt

        web_options = webdriver.ChromeOptions()
        for op in options:
            web_options.add_argument(op)

        if profile:
            web_options.add_argument(r"user-data-dir={}".format(profile))

        web_options.headless = False

        # ==================== PREFERENCES ===========================
        prefs = {
            "download.default_directory": str(Path(download_path).resolve()),
            "savefile.default_directory": str(Path(download_path).resolve()),
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": False,
            "download.directory_upgrade": True,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "plugins.always_open_pdf_externally": True,
            "profile.password_manager_leak_detection": False,
            "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],"selectedDestinationId":"Save as PDF","version":2}',
        }
        prefs = {**prefs, **cust_prefs}
        web_options.add_experimental_option("prefs", prefs)

        # ================== START BROWSER ===========================

        web_options.add_experimental_option("useAutomationExtension", False)
        web_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        CAPABILITIES["name"] = name
        CAPABILITIES["browserName"] = selenoid_browser[0]
        CAPABILITIES["version"] = selenoid_browser[1]
        web_options.set_capability(name="selenoid:options", value=CAPABILITIES)
        web_options.set_capability(
            name="browserName", value=CAPABILITIES["browserName"]
        )

        self.driver = CustomRemoteDriver(command_executor=host, options=web_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        return self.driver

    def startUC(
        self,
        version_main: int = 142,
        enable_cdp_events: bool = True,
        download_path: str = None,
        custom_prefs: dict = {},
        custom_args: list = [],
    ):
        self.default_download_path = download_path
        self.current_download_path = download_path
        options = uc.ChromeOptions()

        # PREFS padrão
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "download.default_directory": str(Path(download_path).resolve()),
        }
        prefs.update(custom_prefs)
        options.add_experimental_option("prefs", prefs)

        # ARGUMENTOS padrão
        default_args = DEFAULT_OPTIONS.copy()
        default_args.extend(custom_args)

        for arg in default_args:
            options.add_argument(arg)

        # REMOVIDO: options.add_experimental_option("detach", True)
        # Isso QUEBRA o UC e gera o erro que você recebeu.

        # start UC
        driver = uc.Chrome(
            options=options,
            enable_cdp_events=enable_cdp_events,
            version_main=version_main,
        )

        self.driver = driver
        driver.implicitly_wait(10)
        return driver

    def startChrome(
        self,
        driver_path,
        download_path: str = None,
        custom_prefs: dict = {},
        custom_options: list = [],
        remove_default_options: bool = False,
        profile: str = None,
        binary_location: str = None,
    ):
        self.default_download_path = download_path
        self.current_download_path = download_path

        # ===================== OPTIONS ==============================
        options = []
        if not remove_default_options:
            options = DEFAULT_OPTIONS
        options += custom_options

        web_options = webdriver.ChromeOptions()
        if binary_location:
            web_options.binary_location = binary_location
        web_options.set_capability("unhandledPromptBehavior", "accept")
        for op in options:
            web_options.add_argument(op)

        if profile:
            web_options.add_argument(
                r"user-data-dir={}".format(str(Path(profile).resolve()))
            )

        web_options.headless = False

        # ==================== PREFERENCES ===========================
        prefs = {
            "download.default_directory": (
                str(Path(download_path).resolve()) if download_path else None
            ),
            "savefile.default_directory": (
                str(Path(download_path).resolve()) if download_path else None
            ),
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": False,
            "download.directory_upgrade": True,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "plugins.always_open_pdf_externally": True,
            "profile.password_manager_leak_detection": False,
            "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],"selectedDestinationId":"Save as PDF","version":2}',
        }
        prefs = {**prefs, **custom_prefs}
        web_options.add_experimental_option("prefs", prefs)

        service = Service(executable_path=driver_path)
        driver = CustomChromeDriver(service=service, options=web_options)
        driver.maximize_window()

        self.driver = driver
        return driver
