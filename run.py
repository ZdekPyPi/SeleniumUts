#TEST FILE
import sys
sys.path.append("./seleniumLib")
from seleniumUts import SeleniumUts,CWebElement
import os


slib = SeleniumUts()

slib.setupSelenium(host="http://72.60.159.109:4444/wd/hub",name="FOI HEHE",use_selenoid=True)


slib.open_page("https://dec.prefeitura.sp.gov.br/login/connect.aspx")

el = slib.wait_xpath("//input[@id='cpfCnpj']").delayed_send("12345678",0.5)

slib.wait_xpath("//input[@id='password']").delayed_send("12345678",0.5)


slib.close()

pass



