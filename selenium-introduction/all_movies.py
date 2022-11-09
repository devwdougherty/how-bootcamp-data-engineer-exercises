import time
import pandas as pd

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# Chrome options to not automatically close the browser when achieve the end of script.
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)

driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
time.sleep(5)
driver.implicitly_wait(10)  # Another way to make sure that our elements are fully loaded to be 'crawled'.

filmography_table = driver.find_element('xpath', '//*[@id="mw-content-text"]/div[1]/table[2]')

df = pd.read_html('<table>' + filmography_table.get_attribute('innerHTML') + '</table>')[0]

# Screenshot
# wb -> write in bytes
with open('print.png', 'wb') as f:
    f.write(driver.find_element('xpath', '/html/body/div').screenshot_as_png)

#print(df.columns)
print(df[df['Ano'] == 1984])

df.to_csv('nicolas_cage_movies.csv', sep=';', index=False)

driver.close()
