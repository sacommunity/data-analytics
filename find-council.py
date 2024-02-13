from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
import time

with webdriver.Chrome() as driver:
    url = "https://lga-sa.maps.arcgis.com/apps/instant/lookup/index.html?appid=db6cce7b773746b4a1d4ce544435f9da&find=130%20L%27Estrange%20Street%2C%20Glenunga"

    to_exclude = ['Results:1', '', 'Loading...']
    driver.get(url)
    text = ''
    while True:        
        for row in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="resultsPanel"]'))):
            time.sleep(5)
            # print('printing row text')
            # print('type of row text ',type(row.text))
            # print(row.text)
            # data = [cell.text for cell in row.find_elements(By.CSS_SELECTOR,"td")]
            text = row.text
            print('text ', text)
            # print('inside row')
            # if row.text != '' and text != 'Loading...':
            #     print('row txt is not none, we got something')
            #     break

        if text not in to_exclude:
            # print('row txt is not none, we got something ', text)
            break
    
        # try:
        #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//a[@id='xact_results_search_results_next'][.='Next']"))).click()
        #     WebDriverWait(driver,20).until(EC.staleness_of(row))
        # except Exception as err:
        #     break
            
print('end all')
print('text value ', text)
text_array = text.splitlines()
print('text array ', text_array)

def extract_value(text_array, prefix):
    values = [t for t in text_array if t.startswith(prefix)]
    if len(values) > 0:
        return values[0].replace(prefix, '')
    
    return ''

council_name = extract_value(text_array, "Council Name")
print('council name ', council_name)
electoral_ward = extract_value(text_array, "Electoral Ward")
print('electoral ward ', electoral_ward)