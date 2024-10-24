from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import re
import quickstart
import getCategory

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

url = "https://www.boottotaal.nl/catalog/"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(url)
sleep(5)
product_list_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"cat with-subs\"]")
product_list_elements = product_list_elements[20:]
print(len(product_list_elements))
list_driver = webdriver.Chrome()
list_driver.maximize_window()
for product_list in product_list_elements:
    product_list_url = product_list.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print(product_list_url)
    list_driver.get(product_list_url)
    sleep(2)
    category_level1 = getCategory.get_category(product_list_url)
    category_level2 = "None"
    
    scroll_down(list_driver)
    product_driver = webdriver.Chrome()
    product_driver.maximize_window()
    while(True):
        products_urls_element = list_driver.find_elements(By.CSS_SELECTOR, "a[class=\"img d-flex align-center justify-center\"]")
        for product_url_element in products_urls_element:
            product_url = product_url_element.get_attribute('href')
            product_driver.get(product_url)
            sleep(2)
            print(f'Category level1: {category_level1}')
            print(f'Category level2: {category_level2}')
            
            try:
                select_element = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"dmws-p_24vavrh-dynamic-variant-dropdown--title\"]")
                options_parent = product_driver.find_element(By.CSS_SELECTOR, "ul[class=\"dmws-p_24vavrh-dynamic-variant-dropdown--list\"]")
                option_elements = options_parent.find_elements(By.TAG_NAME, 'li')
                length = len(option_elements)
                print(length)
            except:
                length = 1
            index = 0
            for _ in range(length):
                try:
                    select_element = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"dmws-p_24vavrh-dynamic-variant-dropdown--title\"]")
                    select_element.click()
                    sleep(0.15)
                    options_parent = product_driver.find_element(By.CSS_SELECTOR, "ul[class=\"dmws-p_24vavrh-dynamic-variant-dropdown--list\"]")
                    option_elements = options_parent.find_elements(By.TAG_NAME, 'li')
                    variant = option_elements[index].text
                    option_elements[index].click()
                except:
                    pass
                sleep(1.5)
                print(f'Category level1: {category_level1}')

                try:
                    title_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header[class=\"title\"]")))
                    title = title_element.find_element(By.TAG_NAME, 'h1').text
                except:
                    title = "None"
                print(f'Title: {title}')

                try:
                    brand_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"brand\"]")))
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

                try:
                    article_number = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="specs"]/div/dl/div[1]/dd'))).text
                except:
                    article_number = "None"
                print(f'Article number: {article_number}')

                try:
                    sku = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="specs"]/div/dl/div[2]/dd'))).text
                except:
                    sku = "None"
                print(f'SKU: {sku}')

                try:
                    information_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"desc-wrap\"]")))
                    information = information_element.text
                except:
                    information = "None"
                print(f'Information: {information}')

                print(f'URL: {product_driver.current_url}')

                quickstart.main()
                columnCount = quickstart.getColumnCount()
                RANGE_DATA = f'7!A{columnCount + 2}:J'

                quickstart.insert_data(RANGE_DATA,
                                        category_level1, "", title, brand, price, variant, article_number, sku, information, product_driver.current_url)

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