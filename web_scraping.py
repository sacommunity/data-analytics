'''
    Web scraping
'''
import re
import logging
import time
from datetime import datetime
from threading import Semaphore, Thread
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException
from requests.utils import quote
import backoff
import requests
from bs4 import BeautifulSoup
from helpers.settings_helper import get_maximum_concurrent_requests, get_default_timeout_in_seconds

web_scraping_logger = logging.getLogger(__name__)

def extract_value_replacing_prefix(text_array, prefix):
    '''
    Extract only the value by removing the prefix
    '''
    values = [t for t in text_array if t.startswith(prefix)]
    if len(values) > 0:
        return values[0].replace(prefix, '').strip()

    return ''


def get_chrome_options(is_headless):
    '''
    Get all the chrome options required for selenium
    '''
    options = webdriver.ChromeOptions()
    if is_headless:
        options.add_argument("--headless=new")

    return options


def on_backoff_handler(details):
    '''
    Handler function when the backoff occurs. It simply logs the message
    '''
    web_scraping_logger.debug(details)
    # web_scraping_logger.debug(
    #     f"Backing off {details.get('wait'):0.1f}
    #     seconds after {details.get('tries')}
    #     tries calling function {details.get('target')} with args {details.get('args')}
    #     and kwargs {details.get('kwargs')}")

# backoff reference: https://pypi.org/project/backoff/
# TODO, if the url is no longer valid, and the page redirects,
    # it will raise Timeout exception, because the element by xpath is not available
# So, gracefully handle such scenario


@backoff.on_exception(backoff.expo,
                      SeleniumTimeoutException,
                      max_tries=3,
                      on_backoff=on_backoff_handler)
def get_data_from_url(url: str,
                      is_headless: bool,
                      to_exclude: list,
                      timeout_in_seconds: int,
                      xpath: str):
    '''
    Get data from url. This is especially for javascript enabled websites.
    If we need data from static websites, simply use requests.get()
    '''
    if url is None or url == '':
        raise ValueError('url is required')
    start_time = datetime.now()
    default_wait_secs = 5

    options = get_chrome_options(is_headless)
    with webdriver.Chrome(options=options) as driver:
        web_scraping_logger.info('Fetching data from url %s', url)
        driver.get(url)
        text = ''
        while True:
            rows = WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath)))
            if len(rows) > 0:
                text = rows[0].text
            # wait some seconds before next try
            sleep_timeout = default_wait_secs if timeout_in_seconds > default_wait_secs \
                else timeout_in_seconds
            time.sleep(sleep_timeout)
            if text not in to_exclude:
                break

            # if we couldnot find data in timeout,
            # then simply ignore it, else there is possibility of infinite loop
            difference_time = datetime.now() - start_time
            if difference_time.total_seconds() > timeout_in_seconds:
                print(f'Wait Timeout of {timeout_in_seconds} seconds exceeded')
                break

    if text == '':
        web_scraping_logger.info('Couldnot retrieve data. So, return None')
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


def find_council_by_address(address:str, timeout_in_seconds=600, is_headless=True):
    '''
    Finds council by address
    address: address where organization is located
    timeout_in_seconds: timeout in seconds until which the program will wait before returning None
    is_headless: if False, a chrome browser will popup, 
    else the operation will be done in background
    '''
    if address is None or address == '':
        raise ValueError('address is required')

    address_encoded = quote(address)
    app_id = 'db6cce7b773746b4a1d4ce544435f9da'
    base_url = 'https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html'
    url = f'{base_url}?appid={app_id}&find={address_encoded}'
    web_scraping_logger.info('Fetching council for %s', address)
    to_exclude = ['Results:1', '', 'Loading...']
    text = get_data_from_url(url, is_headless, to_exclude,
                             timeout_in_seconds, '//*[@id="resultsPanel"]')
    if text == '':
        return ''
    text_array = text.splitlines()

    council_name = extract_value_replacing_prefix(text_array, "Council Name")
    electoral_ward = extract_value_replacing_prefix(
        text_array, "Electoral Ward")

    return {'address': address, 'council_name': council_name, 'electoral_ward': electoral_ward}


def find_councils_by_addresses(addresses: list, is_headless=True, timeout_in_seconds=600):
    '''
    Find councils by addresses in parallel
    Example: 
    # with less timeout, to check test timeout feature. 
    # Without timeout, there is possibility of infinite loop
    # print(find_council_by_address("130 L'Estrange Street, Glenunga", 2))

    # with default timeout, this generally gives data
    # print('council details ', find_council_by_address("130 L'Estrange Street, Glenunga"))
    '''
    # maximum number of concurrent requests at a time
    semaphore = Semaphore(get_maximum_concurrent_requests())

    threads = []

    def find_council(address, all_councils):
        with semaphore:
            try:
                council = find_council_by_address(
                    address, timeout_in_seconds, is_headless)
                all_councils.append(council)
            except Exception as ex:
                # simply log the exception, don't raise it further
                web_scraping_logger.error(ex, exc_info=True)
                raise ex

    all_councils = []
    for address in addresses:
        thread = Thread(target=find_council, args=(address, all_councils))
        threads.append(thread)
        thread.start()

    # print('Wait for all threads to complete ')
    for thread in threads:
        thread.join()

    return all_councils


def find_address_from_sacommunity_website(url: str, is_headless=True, timeout_in_seconds=600):
    '''
    Find address from sa community website
    '''
    xpath = '//*[@id="content-area"]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]'
    return get_data_from_url(url,
                             is_headless,
                             [],
                             timeout_in_seconds,
                             xpath)

# getting council name from sacommunity website based on xpath is not achievable,
# because the xpath differs based on the contents
# As the time of this writing, this urls https://sacommunity.org/org/208832-Burnside_Youth_Club and
# https://sacommunity.org/org/196519-Sturt_Badminton_Club_Inc. has xpath of
# //*[@id="content-area"]/div/div[4]
# //*[@id="content-area"]/div/div[5]
# So it's okay for now to get the council name based on regular expression, thus used beautiful soup


def get_council_from_sacommunity_website(url):
    '''
    Get council from sacommunity website
    '''
    url_response = requests.get(url, timeout=get_default_timeout_in_seconds())
    soup = BeautifulSoup(url_response.content)
    council_identifier = "Council:"
    council_text = soup.find("div", string=re.compile(council_identifier))
    # print('council text ', council_text)
    council_name = ''
    if council_text is not None:
        council_text = str(council_text)
        start_index = council_text.index(council_identifier)
        council_name = council_text[start_index:].replace(
            council_identifier, '').replace("</div>", "").strip()

    return council_name


# test function, useful while debugging
# url = 'https://sacommunity.org/org/208832-Burnside_Youth_Club'
# find_address_in_sacommunity(url, False)


def find_addresses_from_sacommunity_website(urls: list, is_headless=True, timeout_in_seconds=600):
    '''
    Retrieves addresses from the sa-community website for given lists of urls in parallel
    '''
    semaphore = Semaphore(get_maximum_concurrent_requests())

    threads = []

    def find_addr(url, all_address):
        with semaphore:
            try:
                addr = find_address_from_sacommunity_website(
                    url, is_headless, timeout_in_seconds)
                council = get_council_from_sacommunity_website(url)
                all_address.append(
                    {'url': url, 'address': addr, 'council_in_sacommunity_website': council})
            except Exception as ex:
                web_scraping_logger.error(ex, exc_info=True)
                raise ex

    all_address = []
    for url in urls:
        thread = Thread(target=find_addr, args=(url, all_address))
        threads.append(thread)
        thread.start()

    # print('Wait for all threads to complete ')
    for thread in threads:
        thread.join()

    return all_address
