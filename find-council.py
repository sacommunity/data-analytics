from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
import time
from requests.utils import quote

def find_council_by_address(address):

    with webdriver.Chrome() as driver:
        address_encoded = quote(address)
        url = f'https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html?appid=db6cce7b773746b4a1d4ce544435f9da&find={address_encoded}'
        print('Fetching council for ', address)
        to_exclude = ['Results:1', '', 'Loading...']
        driver.get(url)
        text = ''
        while True:        
            for row in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="resultsPanel"]'))):
                time.sleep(5)
                text = row.text
                print('text ', text)

            if text not in to_exclude:
                break
                
    print('text value ', text)
    text_array = text.splitlines()
    print('text array ', text_array)

    def extract_value(text_array, prefix):
        values = [t for t in text_array if t.startswith(prefix)]
        if len(values) > 0:
            return values[0].replace(prefix, '').strip()
        
        return ''

    council_name = extract_value(text_array, "Council Name")
    electoral_ward = extract_value(text_array, "Electoral Ward")

    return {'address': address, 'council_name': council_name, 'electoral_ward': electoral_ward}

council_details = find_council_by_address("130 L'Estrange Street, Glenunga")
print('council details ', council_details)