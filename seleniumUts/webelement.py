from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import time
from .uts import handle_stale
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
import re
from time import sleep


class CWebElement(WebElement):
    _found_by = None
    _query_path = None
    selenium_uts = None
    time = None
    custom_error = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            sleep(delay)
            self.send_keys(c)

    def focus(self):
        """
        Desc:
            Focus on the element using JavaScript.\n
        Returns: None
        """
        self.parent.execute_script("arguments[0].scrollIntoView(true);", self)
        sleep(0.5)
        self.parent.execute_script("arguments[0].focus();", self)
        return self

    @handle_stale
    def clear(self):
        """Limpa o campo e retorna a própria instância do objeto."""
        super().clear()
        return self
        
    @handle_stale
    def click(self, wait_clickable=False, timeout=10):
        end_time = time() + timeout

        try:
            # 1. Se wait_clickable for True, aguarda até o elemento estar pronto
            if wait_clickable:
                WebDriverWait(self._parent, timeout).until(
                    EC.element_to_be_clickable((self._found_by, self._query_path))
                )

            # 2. Tenta o clique original
            super().click()
            return self

        except TimeoutException:
            if wait_clickable:
                raise TimeoutException(
                    f"Elemento {self._query_path} não ficou clicável após {timeout}s"
                )
            raise
        except Exception:
            pass

    def select_by_text(self, text):
        """
        Desc:
            Select item in dropdown by visible text.\n
        Args:
            - ``text`` - The visible text of the option to be selected.
        Returns:
            - The WebElement instance.
        """
        Select(self).select_by_visible_text(text)
        return self

    def select_by_value(self, value):
        """
        Desc:
            Select item in dropdown by value.\n
        Args:
            - ``value`` - The value attribute of the option to be selected.
        Returns: None
        """
        Select(self).select_by_value(value)

    def click_js(self):
        """
        Desc:
            Click the element using JavaScript.\n
        Returns:
            - None
        """
        self.parent.execute_script("arguments[0].click();", self)

    @handle_stale
    def mark(self, color: str = "red", thickness: str = "3px", mark=True):
        """
        Aplica uma borda temporária a um elemento usando JavaScript para destacá-lo.
        Armazena o estilo original para restauração posterior.

        Args:
            color: A cor da borda (ex: 'red', 'blue', '#FF0000').
            thickness: A espessura da borda (ex: '3px', '5px').
        """
        if not mark:
            return
        # Define o novo estilo da borda
        new_style = f"{thickness} solid {color}"


        # 1. Guarda o estilo da borda original
        original_style = self.parent.execute_script(
            "return arguments[0].style.outline", self
        )

        # 2. Aplica o novo estilo da borda
        self.parent.execute_script(
            f"arguments[0].style.outline = '{new_style}'", self
        )

        # 3. Armazena o estilo original no próprio elemento (como um atributo) para que a função de remoção possa acessá-lo
        self.parent.execute_script(
            "arguments[0].setAttribute('original_outline', arguments[1]);",
            self,
            original_style,
        )

        return self

    def unmark(self):
        """
        Restaura o estilo original do elemento, removendo a borda de destaque.

        """
        try:
            # 1. Recupera o estilo original armazenado no atributo
            original_style_outline = self.parent.execute_script(
                "return arguments[0].getAttribute('original_style_outline');", self
            )

            # 2. Restaura o estilo da borda original
            self.parent.execute_script(
                "arguments[0].style.outline = arguments[1]",
                self,
                original_style_outline or "none ",
            )

            # 3. Remove o atributo auxiliar
            self.parent.execute_script(
                "arguments[0].removeAttribute('original_style_outline');", self
            )

        except WebDriverException as e:
            raise Exception(f"Erro ao remover borda: {e}")

        return self

    def wait_xpath(self, path, time=20, multiple=False, throw=True, custom_error=None,wait_visible=False):
        
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
            def check_visibility(d):
                # Tenta encontrar o(s) elemento(s) usando sua lógica customizada
                if multiple:
                    elements = self.parent.find_elements(
                        By.XPATH, path, selenium_uts=self.selenium_uts, time=time, custom_error=custom_error
                    )
                    # Filtra apenas os que estão visíveis
                    visible_elements = [el for el in elements if el.is_displayed()] if wait_visible else elements
                    return visible_elements if visible_elements else False
                else:
                    element = self.parent.find_element(
                        By.XPATH, path, selenium_uts=self.selenium_uts, time=time, custom_error=custom_error
                    )
                    # Retorna o elemento apenas se estiver visível no browser
                    return element if (element.is_displayed() if wait_visible else True) else False
            # O WebDriverWait vai repetir a função acima até retornar algo diferente de False/None
            return WebDriverWait(self.parent, time).until(check_visibility)
        except Exception:
            if throw:
                if custom_error:
                    raise Exception(custom_error)
                else:
                    raise
            return None


    def get_html_code(self):
        script_deep_copy = """
        function forceInlineStyles(el) {
            var styles = window.getComputedStyle(el);
            var cssText = "";
            
            // Lista das propriedades cruciais que costumam sumir
            var props = [
                "color", "font-family", "font-size", "font-weight", "font-style",
                "line-height", "text-align", "text-decoration", "text-transform",
                "letter-spacing", "background-color", "padding", "margin",
                "border", "border-radius", "display", "flex-direction",
                "align-items", "justify-content", "width", "height", "box-sizing"
            ];

            for (var i = 0; i < props.length; i++) {
                var prop = props[i];
                cssText += prop + ":" + styles.getPropertyValue(prop) + " !important;";
            }
            
            el.style.cssText = cssText;

            // Processa todos os filhos recursivamente
            for (var i = 0; i < el.children.length; i++) {
                forceInlineStyles(el.children[i]);
            }
        }

        // Cria um clone para não estragar a página original enquanto processamos
        var clone = arguments[0].cloneNode(true);
        clone.style.position = "fixed";
        clone.style.top = "-9999px";
        document.body.appendChild(clone);
        
        // Aplica os estilos no clone
        forceInlineStyles(clone);
        
        var finalHTML = clone.outerHTML;
        document.body.removeChild(clone);
        return finalHTML;
        """
        return self.parent.execute_script(script_deep_copy, self)

    def refresh(self, throw=True):
        """Um método bônus para re-procurar o próprio elemento"""
        if self._found_by == By.XPATH:
            el = self.selenium_uts.wait_xpath(
                self._query_path,
                time=self.time,
                custom_error=self.custom_error,
                throw=throw,
            )
        elif self._found_by == By.ID:
            el = self.selenium_uts.wait_id(
                self._query_path,
                time=self.time,
                custom_error=self.custom_error,
                throw=throw,
            )
        elif self._found_by == By.CSS_SELECTOR:
            el = self.selenium_uts.wait_css(
                self._query_path,
                time=self.time,
                custom_error=self.custom_error,
                throw=throw,
            )
        return el

    def export_as_page_pdf(
        self, file_name, css=None, single_page=True, regx_replaces=[]
    ):
        html = self.get_html_code()
        html = f"""
            </html>
                <head>
                <title>pdf_html</title>
                    <style>
                        @media print {{
                            body, .info-bar, .container, .section h3 {{
                                /* Esta linha é o segredo */
                                -webkit-print-color-adjust: exact !important;
                                print-color-adjust: exact !important;
                            }}
                        }}
                    </style>
                </head>
                <body>{html}</body>
            </html>
        """

        for regx, to in regx_replaces:
            html = html = re.sub(regx, to, html)

        self.selenium_uts.new_tab()
        self.parent.execute_script("document.write(arguments[0]);", html)
        if css:
            self.selenium_uts.add_style(css)

        self.selenium_uts.save_to_pdf(file_name, single_page)
        self.selenium_uts.close_current_tab()
        pass
    

    def wait_visible(self,time=20):
        """
        Desc:
            Wait until the element is visible.\n
        Returns:
            - The WebElement instance.
        """
        WebDriverWait(self.parent, time).until(EC.visibility_of(self))
        return self