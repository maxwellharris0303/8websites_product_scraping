from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import quickstart
import scrape_data

url = "https://www.nauticgear.nl/bootaccessoires.html"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(url)

total_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul[class=\"uaccordion uaccordion-style1 sideacco\"]")))
list_elements = total_element.find_elements(By.TAG_NAME, 'li')
print(len(list_elements))

list_driver = webdriver.Chrome()
list_driver.maximize_window()
for list in list_elements:
    list_url_element = list.find_element(By.CSS_SELECTOR, ":first-child")
    list_url = list_url_element.get_attribute('href')
    print(list_url)
    list_driver.get(list_url)
    sleep(2)
    try:
        product_item_elements = list_driver.find_elements(By.CSS_SELECTOR, "li[class=\"item product product-item\"]")
        products_count = len(product_item_elements)
        print(products_count)

        product_driver = webdriver.Chrome()
        product_driver.maximize_window()

        if products_count < 60:
            for product_item in product_item_elements:
                product_url = product_item.find_element(By.CSS_SELECTOR, "a[class=\"product-item-link\"]").get_attribute('href')
                product_driver.get(product_url)
                sleep(2)

                try:
                    select_element_parent = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"product-options-wrapper configurable\"]")
                    select_element = select_element_parent.find_element(By.TAG_NAME, "select")
                    options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                    length = len(options_elements)
                    print(length)
                    index = 1
                    for _ in range(length):
                        try:
                            select_element_parent = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"product-options-wrapper configurable\"]")
                            select_element = select_element_parent.find_element(By.TAG_NAME, "select")
                            select_element.click()
                            sleep(0.15)
                            options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                            variant = options_elements[index].text
                            options_elements[index].click()
                            sleep(2)
                        except:
                            variant = "None"
                            break
                        scrape_data.scrape_data(product_driver, variant)
                        index += 1
                except:
                    variant = "None"
                    scrape_data.scrape_data(product_driver, variant)

        else:
            while(True):
                product_item_elements = list_driver.find_elements(By.CSS_SELECTOR, "li[class=\"item product product-item\"]")
                for product_item in product_item_elements:
                    product_url = product_item.find_element(By.CSS_SELECTOR, "a[class=\"product-item-link\"]").get_attribute('href')
                    product_driver.get(product_url)
                    sleep(2)

                    try:
                        select_element_parent = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"product-options-wrapper configurable\"]")
                        select_element = select_element_parent.find_element(By.TAG_NAME, "select")
                        options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                        length = len(options_elements)
                        print(length)
                        index = 1
                        for _ in range(length):
                            try:
                                select_element_parent = product_driver.find_element(By.CSS_SELECTOR, "div[class=\"product-options-wrapper configurable\"]")
                                select_element = select_element_parent.find_element(By.TAG_NAME, "select")
                                select_element.click()
                                sleep(0.15)
                                options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                                variant = options_elements[index].text
                                options_elements[index].click()
                                sleep(2)
                            except:
                                variant = "None"
                                break
                            scrape_data.scrape_data(product_driver, variant)
                            index += 1
                    except:
                        variant = "None"
                        scrape_data.scrape_data(product_driver, variant)
                    
                try:
                    next_button = product_driver.find_element(By.CSS_SELECTOR, "li[class=\"item pages-item-next\"]")
                    next_button.click()
                except:
                    break
                sleep(2)      
        
    except:
        print("No")
        product_driver.quit()
        pass

list_driver.quit()
print("Done!")     
