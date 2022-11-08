import sys

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

cep = sys.argv[1]

if not cep:
    sys.exit("invalid cep")

# Chrome options to not automatically close the browser when achieve the end of script.
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)

# 05/11 Flow Black Week 'Confira Agora!'
#driver.get('https://howedu.com.br/')
#driver.find_element('xpath', '//*[@id="post-11648"]/div/div/section[3]/div/div[2]/div/div[4]/div/div/a').click()
#driver.find_element('xpath', '//*[@id="content"]/div/div/section[2]/div/div[2]/div/div[4]/div/div/a').click()
#driver.find_element('xpath', '//*[@id="ofertas"]/div/div[1]/div/section[2]/div/div/div/div[7]/div/div/a').click()

driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php')
#cep_element = driver.find_element('xpath', '//*[@id="endereco"]')
cep_element = driver.find_element('name', 'endereco')
cep_element.clear()
cep_element.send_keys(cep)

cep_combo_box_element = driver.find_element('name', 'tipoCEP')
# open combo cep_combo_box_element
cep_combo_box_element.click()
driver.find_element('xpath', '//*[@id="tipoCEP"]/optgroup/option[1]').click()
driver.find_element('id', 'btn_pesquisar').click()

logradouro = (WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[1]')))).text

#logradouro = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[1]').text
bairro = driver.find_element('xpath', '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[2]').text
localidade = driver.find_element('xpath', '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[3]').text

driver.close()

print(
    """
    For CEP {} we have:
    Address: {}
    Neighbourhood: {}
    City: {}
    """.format(
    cep,
    logradouro,
    bairro,
    localidade
))
