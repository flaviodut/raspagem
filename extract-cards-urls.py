import os
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

page_domain = 'https://www.vivo.com.br'
pages_path = [
    '/para-voce/produtos-e-servicos/para-casa/internet',
    '/para-voce/produtos-e-servicos/para-casa/tv',
    '/para-voce/produtos-e-servicos/para-o-celular/planos-pos-pago',
]

application_path = os.path.dirname(__file__)
today = datetime.now().strftime("%y%m%d_%H%M")
buttons_info = []
is_bussolado = False

chromedriver = '/Users/flavio/Documents/dev/chromedriver_mac64/chromedriver'
options = Options()
options.add_argument('--incognito')
options.headless = False
driver_service = Service(executable_path=chromedriver)
driver = webdriver.Chrome(service=driver_service, options=options)

for page_path in pages_path:
    driver.get(page_domain + page_path)

    # Bussola
    if not is_bussolado:
        sleep(2)
        bussola_cities = driver.find_elements(By.CSS_SELECTOR, value='.search__results__list a')
        print(f'Bussola | Quantidade de cidades: {len(bussola_cities)}')

        if len(bussola_cities) > 0:
            is_bussolado = True
            bussola_cities[0].click()

    # Cards buttons
    sleep(2)
    cards_buttons = driver.find_elements(By.CSS_SELECTOR, value='a.btn-orange')
    print(f'Página | Quantidade de botões: {len(cards_buttons)}')

    if len(cards_buttons) > 0:
        for button in cards_buttons:
            button_info = {
                'page_path': page_path,
                'inner_text': button.get_attribute('innerHTML').strip(),
                'attr_class': button.get_attribute('class').strip(),
                'attr_url': button.get_attribute('href'),
            }

            if button_info not in buttons_info:
                buttons_info.append(button_info)


folder_dist = os.path.join(application_path, 'dist')
# folder_dist_exist = os.path.exists(folder_dist)
# if not folder_dist_exist:
os.makedirs(folder_dist, exist_ok=True)
file_report = os.path.join(folder_dist, f'extract-cards-urls-{today}.csv')

df_headlines = pd.DataFrame(buttons_info)
df_headlines.to_csv(file_report)

driver.quit()
