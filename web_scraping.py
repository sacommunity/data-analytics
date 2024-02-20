from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from requests.utils import quote
from datetime import datetime
from threading import Semaphore, Thread
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException
import backoff
import logging

def extract_value_replacing_prefix(text_array, prefix):
    values = [t for t in text_array if t.startswith(prefix)]
    if len(values) > 0:
        return values[0].replace(prefix, '').strip()
        
    return ''

def get_chrome_options(is_headless):
    options = webdriver.ChromeOptions()
    if is_headless:
        options.add_argument("--headless=new")

    return options

def on_backoff_handler(details):
    logging.debug("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} with args {args} and kwargs {kwargs}".format(**details))

@backoff.on_exception(backoff.expo, SeleniumTimeoutException, max_tries = 3, on_backoff = on_backoff_handler)
def get_data_from_url(url: str, is_headless: 
                      bool, to_exclude: list, 
                      timeout_in_seconds: int, 
                      xpath: str):
    start_time = datetime.now()
    default_time_to_wait_in_seconds = 5
    
    options = get_chrome_options(is_headless)
    with webdriver.Chrome(options=options) as driver:
        logging.info('Fetching data from url ', url)
        driver.get(url)
        text = ''
        while True:   
            rows = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
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
        logging.info('Couldnot retrieve data. So, return None')
        return ''

    return text

# Manual retry logic. I ended up using backoff library instead. Kept here just for reference
# def get_data_from_url_with_retry(url: str, is_headless: 
#                       bool, to_exclude: list, 
#                       timeout_in_seconds: int, 
#                       xpath: str):
#     MAX_RETRY_COUNT = 3

#     for i in range(MAX_RETRY_COUNT):
#         try:
#             return get_data_from_url(url, is_headless, to_exclude, timeout_in_seconds, xpath)
#         except SeleniumTimeoutException as te:
#             print('Timeout occurred ', str(te))
#             # TODO, wait for some time and try again
#             print('Wait 3 seconds before retry. Retry count ', i)
#             time.sleep(3)
#         except Exception as ex:
#             print('General Exception ', str(ex))
#             print('Exception type ', type(ex))
#             return None
    

'''
    Finds council by address
    address: address where organization is located
    timeout_in_seconds: timeout in seconds until which the program will wait before returning None
    is_headless: if False, a chrome browser will popup, else the operation will be done in background
'''
def find_council_by_address(address, timeout_in_seconds = 600, is_headless = True):
    if address is None or address == '':
        raise Exception('address is required')
    
    address_encoded = quote(address)
    url = f'https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html?appid=db6cce7b773746b4a1d4ce544435f9da&find={address_encoded}'
    logging.info('Fetching council for ', address)
    to_exclude = ['Results:1', '', 'Loading...']
    text = get_data_from_url(url, is_headless, to_exclude, timeout_in_seconds, '//*[@id="resultsPanel"]')
    if text == '':
        return ''
    text_array = text.splitlines()

    council_name = extract_value_replacing_prefix(text_array, "Council Name")
    electoral_ward = extract_value_replacing_prefix(text_array, "Electoral Ward")

    return {'address': address, 'council_name': council_name, 'electoral_ward': electoral_ward}

# Test scripts: useful for debugging above function
# with default timeout, this generally gives data
# print('council details ', find_council_by_address("130 L'Estrange Street, Glenunga"))

# with less timeout, to check test timeout feature. Without timeout, there is possibility of infinite loop
# print(find_council_by_address("130 L'Estrange Street, Glenunga", 2))

def find_address_from_sacommunity_website(url: str, is_headless = True, timeout_in_seconds = 600):
    if url is None or url == '':
        raise Exception('url is required')
    
    return get_data_from_url(url, is_headless, [], timeout_in_seconds, '//*[@id="content-area"]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]')

# test function, useful while debugging
# url = 'https://sacommunity.org/org/208832-Burnside_Youth_Club'
# find_address_in_sacommunity(url, False)

def find_addresses_from_sacommunity_website(urls: list, is_headless = True, timeout_in_seconds = 600):
    # maximum number of concurrent requests at a time
    MAXIMUM_CONCURRENT_REQUESTS = 3
    semaphore = Semaphore(MAXIMUM_CONCURRENT_REQUESTS)

    threads = []
    def find_addr(url, all_address):
        addr = ''
        with semaphore:
            try:
                addr = find_address_from_sacommunity_website(url, is_headless, timeout_in_seconds)
            except Exception as ex:
                # simply log the exception, don't raise it further
                logging.error(ex, exc_info=True)
            
        all_address[url] = addr

    all_address = {}
    for url in urls:
        thread = Thread(target=find_addr, args=(url, all_address))
        threads.append(thread)
        thread.start()

    # print('Wait for all threads to complete ')
    for thread in threads:
        thread.join()

    return all_address