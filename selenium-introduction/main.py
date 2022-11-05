from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome options to not automatically close the browser when achieve the end of script.
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome('.\src\chromedriver.exe', options=chrome_options)
driver.get('https://howedu.com.br/')

# 05/11 Flow Black Week 'Confira Agora!'
driver.find_element('xpath', '//*[@id="post-11648"]/div/div/section[3]/div/div[2]/div/div[4]/div/div/a').click()
driver.find_element('xpath', '//*[@id="content"]/div/div/section[2]/div/div[2]/div/div[4]/div/div/a').click()
driver.find_element('xpath', '//*[@id="ofertas"]/div/div[1]/div/section[2]/div/div/div/div[7]/div/div/a').click()