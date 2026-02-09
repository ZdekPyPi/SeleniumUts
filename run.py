# TEST FILE
import sys

sys.path.append("./seleniumLib")
from seleniumUts import SeleniumUts

slib = SeleniumUts()

slib.startChrome(
    driver_path     = r"C:\chromedriver-win64\chromedriver.exe",
    #binary_location = r"C:\Program Files\Google\Chrome\Application"
    )

#slib.startRemoteSelenium(host="HOST", name="FOI HEHE")

slib.open_page("https://dec.prefeitura.sp.gov.br/login/connect.aspx")

el = slib.wait_xpath("//input[@id='cpfCnpj']")

el.delayed_send("12345678", 0.5)

slib.wait_xpath("//input[@id='password']").delayed_send("12345678", 0.5)


slib.close()

pass
