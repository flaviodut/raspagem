import os
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Preparing script before we convert it to executable
application_path = os.path.dirname(__file__)

# get date in format YYYYMMDD
today = datetime.now().strftime("%Y%m%d")

page_url = 'https://www.vivo.com.br/para-voce'
chromedriver = '/Users/flavio/Documents/chromedriver_mac64/chromedriver'

# Headless mode
options = Options()
options.headless = False

driver_service = Service(executable_path=chromedriver)
driver = webdriver.Chrome(service=driver_service, options=options)
driver.get(page_url)

driver.find_element(By.CSS_SELECTOR, value='.search__results__list a').click()

elements = driver.find_elements(By.CSS_SELECTOR, value='.main-menu__nav-bottom a')

inner_texts = []
titles = []
links = []
for element in elements:
    inner_text = element.text
    title = element.get_attribute('title')
    link = element.get_attribute('href')
    inner_texts.append(inner_text.strip())
    titles.append(title.strip())
    links.append(link)


# Exporting data to the same folder where the executable will be located
df_headlines = pd.DataFrame({'text': inner_texts, 'title': titles, 'link': links})
report_file = os.path.join(application_path, f'extract-menu-anchors_{today}.csv')
df_headlines.to_csv(report_file)

driver.quit()
