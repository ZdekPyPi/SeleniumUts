# SeleniumUts

Uma biblioteca Python que encapsula algumas funcionalidades do Selenium WebDriver, facilitando a automação de navegadores para testes e raspagem de dados. A biblioteca suporta o uso do `undetected_chromedriver` e integra-se facilmente com o Selenoid para execução de testes em ambientes distribuídos.

## Uso

### Importando a Biblioteca

```python
from seleniumUts import SeleniumUts
```

### Criando uma Instância de `SeleniumUts`

```python
selenium_lib = SeleniumUts()
```

### Exemplos de Uso

#### Configurando o Selenium com ChromeDriver

```python
# Configure o Selenium sem usar o Selenoid
selenium_lib.setupSelenium(host=None, use_selenoid=False)

# Abrir uma página web
driver = selenium_lib.open_page('https://www.example.com')

# Fechar o navegador
selenium_lib.close()
```

#### Configurando o Selenium com Selenoid

```python
# Configure o Selenium usando o Selenoid
selenoid_host = 'http://your-selenoid-server.com/wd/hub'
selenium_lib.setupSelenium(host=selenoid_host, use_selenoid=True)

# Abrir uma página web
driver = selenium_lib.open_page('https://www.example.com')

# Fechar o navegador
selenium_lib.close()
```

#### Aguardando a Visibilidade de um Elemento

```python
# Configure o Selenium
selenium_lib.setupSelenium(host=None, use_selenoid=False)

# Abrir uma página web
selenium_lib.open_page('https://www.example.com')

# Esperar até que o elemento esteja visível
element = selenium_lib.wait_xpath('//button[@id="submit"]', time=10)
element.click()

# Fechar o navegador
selenium_lib.close()
```

#### Envio de Texto com Atraso entre Caracteres

```python
# Configure o Selenium
selenium_lib.setupSelenium(host=None, use_selenoid=False)

# Abrir uma página web
selenium_lib.open_page('https://www.example.com')

# Encontrar o campo de texto e enviar texto com atraso
element = selenium_lib.wait_xpath('//input[@id="search-box"]')
element.delayed_send('Python Selenium', delay=0.2)

# Fechar o navegador
selenium_lib.close()
```

#### Rolagem até o Fim da Página

```python
# Configure o Selenium
selenium_lib.setupSelenium(host=None, use_selenoid=False)

# Abrir uma página web
selenium_lib.open_page('https://www.example.com')

# Rolagem até o fim da página
selenium_lib.scroll_end()

# Fechar o navegador
selenium_lib.close()
```

## Métodos Disponíveis

- **`setupSelenium(host, name="default", use_selenoid=False, cust_opt=[], remove_default_options=False, download_path=None, selenoid_browser=("chrome","110.0"))`**: Configura o WebDriver do Selenium com opções personalizadas e preferências para o ChromeDriver. Suporta configuração para Selenoid.
- **`open_page(page)`**: Abre uma página web e espera até que ela seja totalmente carregada.
- **`wait_xpath(path, time=20, throw=True)`**: Aguarda até que um elemento, identificado por um caminho XPath, esteja visível no DOM.
- **`<el>.delayed_send(word, delay)`**: Envia texto para um elemento, inserindo um atraso especificado entre cada caractere.
- **`scroll_end()`**: Rola até o final da página atual.
- **`close()`**: Fecha o navegador e encerra a sessão do WebDriver.

## Contribuição

Contribuições são bem-vindas! Por favor, envie um pull request ou abra uma issue para quaisquer problemas ou melhorias.

## Licença

Este projeto está licenciado sob a licença MIT.
