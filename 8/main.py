from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import re
from urllib.parse import urlparse
import quickstart

def scroll_down(driv):
    page_height = driv.execute_script("return document.body.scrollHeight")
    scroll_distance = page_height // 5
    driv.execute_script(f"window.scrollTo(0, {scroll_distance});")
    sleep(0.3)
    driv.execute_script(f"window.scrollTo({scroll_distance}, {scroll_distance * 2});")
    sleep(0.3)
    driv.execute_script(f"window.scrollTo({scroll_distance * 2}, {scroll_distance * 3});")
    sleep(0.3)
    driv.execute_script(f"window.scrollTo({scroll_distance * 3}, {scroll_distance * 4});")
    sleep(0.3)
    driv.execute_script(f"window.scrollTo({scroll_distance * 4}, {page_height});")

root_url = "https://www.123watersport.nl/catalog/"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(root_url)
sleep(5)
list_urls = []
product_list_elements = driver.find_elements(By.CSS_SELECTOR, "ul[class=\"subsubnav\"]")
hidden_elements = driver.find_elements(By.CSS_SELECTOR, "ul[class=\"subsubnav hidden\"]")
new_product_list_elements = product_list_elements + hidden_elements
print(len(new_product_list_elements))

for product_list in new_product_list_elements:
    list_urls_element = product_list.find_elements(By.TAG_NAME, 'a')
    for list_url in list_urls_element:
        list_urls.append(list_url.get_attribute('href'))
print(list_urls)
print(len(list_urls))

list_driver = webdriver.Chrome()
list_driver.maximize_window()
for url in list_urls:
    list_driver.get(url)
    sleep(2)
    product_driver = webdriver.Chrome()
    product_driver.maximize_window()
    while(True):
        scroll_down(list_driver)
        products_urls_element = list_driver.find_elements(By.CSS_SELECTOR, "a[class=\"img d-flex align-center justify-center\"]")
        for product_url_element in products_urls_element:
            product_url = product_url_element.get_attribute('href')
            product_driver.get(product_url)
            sleep(2)

            parsed_url = urlparse(url)
            path_parts = parsed_url.path.split("/")

            try:
                category_level1 = path_parts[1]
            except:
                category_level1 = ""
            try:
                category_level2 = path_parts[2]
            except:
                category_level2 = ""
            try:
                category_level3 = path_parts[3]
            except:
                category_level3 = ""
            try:
                category_level4 = path_parts[4]
            except:
                category_level4 = ""

            try:
                select_element = product_driver.find_element(By.CSS_SELECTOR, "select[id=\"product_configure_variants\"]")
                options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                length = len(options_elements)
                print(length)
            except:
                length = 1

            index = 0
            for _ in range(length):
                try:
                    select_element = product_driver.find_element(By.CSS_SELECTOR, "select[id=\"product_configure_variants\"]")
                    select_element.click()
                    sleep(0.15)
                    options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                    variant = options_elements[index].text
                    options_elements[index].click()
                except:
                    pass
                sleep(1.5)

                print(f'Category level 1: {category_level1}')
                print(f'Category level 2: {category_level2}')
                print(f'Category level 3: {category_level3}')
                print(f'Category level 4: {category_level4}')

                try:
                    title_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header[class=\"title\"]")))
                    title = title_element.find_element(By.TAG_NAME, 'h1').text
                except:
                    title = "None"
                print(f'Title: {title}')

                try:
                    brand_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"brand hide-575\"]")))
                    brand = brand_element.find_element(By.CSS_SELECTOR, 'a').text
                except:
                    brand = "None"
                print(f'Brand: {brand}')

                try:
                    price_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"for\"]")))
                    price_text = price_element.text
                    match = re.search(r'(\d+(?:\,\d+)?)', price_text)
                    price = match.group(1).replace(',', '.')
                except:
                    price = "None"
                print(f'Price: {price}')

                print(f'Variant: {variant}')
 
                article_number = "None"
                print(f'Article number: {article_number}')

                ean = "None"
                print(f'EAN: {ean}')

                try:
                    information_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"desc-wrap\"]")))
                    wrapper_element = information_element.find_element(By.CSS_SELECTOR, "div[class=\"wrapper\"]")
                    product_driver.execute_script("arguments[0].classList.add('show');", wrapper_element)
                    information_text = wrapper_element.text
                    information = information_text.replace("Toon meer", "")
                except:
                    information = "None"
                print(f'Information: {information}')

                print(f'URL: {product_driver.current_url}')

                quickstart.main()
                columnCount = quickstart.getColumnCount()
                RANGE_DATA = f'8!A{columnCount + 2}:L'

                quickstart.insert_data(RANGE_DATA,
                                        category_level1, category_level2, category_level3, category_level4, 
                                        title, brand, price, variant, article_number, ean, information, product_driver.current_url)

                index += 1
        try:
            next_url_element = WebDriverWait(list_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"next\"]")))
            next_url = next_url_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            list_driver.get(next_url)
        except:
            break
        sleep(3)

driver.quit()
print("Done!")