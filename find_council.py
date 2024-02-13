from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from requests.utils import quote
from datetime import datetime

def extract_value_replacing_prefix(text_array, prefix):
    values = [t for t in text_array if t.startswith(prefix)]
    if len(values) > 0:
        return values[0].replace(prefix, '').strip()
        
    return ''

'''
    Finds council by address
    address: address where organization is located
    timeout_in_seconds: timeout in seconds until which the program will wait before returning None
    is_headless: if False, a chrome browser will popup, else the operation will be done in background
'''
def find_council_by_address(address, timeout_in_seconds = 600, is_headless = True):
    if address is None or address == '':
        raise Exception('address is required')
    start_time = datetime.now()
    default_time_to_wait_in_seconds = 5
    options = webdriver.ChromeOptions()
    if is_headless:
        options.add_argument("--headless=new")
        
    with webdriver.Chrome(options=options) as driver:
        address_encoded = quote(address)
        url = f'https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html?appid=db6cce7b773746b4a1d4ce544435f9da&find={address_encoded}'
        print('Fetching council for ', address)
        to_exclude = ['Results:1', '', 'Loading...']
        driver.get(url)
        text = ''
        while True:   
            rows = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="resultsPanel"]')))
            if len(rows) > 0:
                text = rows[0].text
            # wait some seconds before next try
            time_to_sleep_in_seconds = default_time_to_wait_in_seconds if timeout_in_seconds > default_time_to_wait_in_seconds else timeout_in_seconds
            time.sleep(time_to_sleep_in_seconds)
            if text not in to_exclude:
                break

            # if we couldnot find data in timeout, then simply ignore it, else there is possibility of infinite loop
            difference_time = datetime.now() - start_time
            if difference_time.total_seconds() > timeout_in_seconds:
                print(f'Wait Timeout of {timeout_in_seconds} seconds exceeded')
                break

    if text == '':
        print('Couldnot retrieve data. So, return None')
        return None
    
    print('text value ', text)
    text_array = text.splitlines()

    council_name = extract_value_replacing_prefix(text_array, "Council Name")
    electoral_ward = extract_value_replacing_prefix(text_array, "Electoral Ward")

    return {'address': address, 'council_name': council_name, 'electoral_ward': electoral_ward}

# Test scripts: useful for debugging above function
# with default timeout, this generally gives data
# print('council details ', find_council_by_address("130 L'Estrange Street, Glenunga"))

# with less timeout, to check test timeout feature. Without timeout, there is possibility of infinite loop
# print(find_council_by_address("130 L'Estrange Street, Glenunga", 2))