from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import quickstart



def start(category1, url):

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

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)

    while(True):
        scroll_down(driver)
        product_driver = webdriver.Chrome()
        product_driver.maximize_window()
        products_urls = driver.find_elements(By.CSS_SELECTOR, "a[class=\"img d-flex align-center justify-center\"]")
        for products_element in products_urls:
            product_url = products_element.get_attribute('href')
            print(product_url)
            product_driver.get(product_url)
            #scroll_down(product_driver)
            try:
                select_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"product-configure-options-option\"]")))
            except:
                try:
                    select_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"product-configure-variants\"]")))
                except:
                    variant = "None"
                    pass
            try:
                options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                length = len(options_elements)
                print(length)
            except:
                length = 1
                pass
            index = 0
            for _ in range(length):
                try:
                    select_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"product-configure-options-option\"]")))
                except:
                    try:
                        select_element = WebDriverWait(product_driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"product-configure-variants\"]")))
                    except:
                        variant = "None"
                        pass
                try:
                    options_elements = select_element.find_elements(By.TAG_NAME, 'option')
                    select_tag = select_element.find_element(By.TAG_NAME, 'select')
                    select_tag.click()
                    sleep(0.15)
                    variant = options_elements[index].text
                    options_elements[index].click()
                except:
                    pass
                
                print(f'Category1: {category1}')
                sleep(1.5)
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
                    price_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product"]/div[1]/article/div[2]/div[1]/div[1]/span[1]')))
                    price = price_element.text
                except:
                    price = "None"
                print(f'Price: {price}')

                print(f'Variant: {variant}')

                try:
                    article_number = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="specs"]/div/dl/div[1]/dd'))).text
                except:
                    article_number = "None"
                print(f'Article number: {article_number}')

                try:
                    ean = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="specs"]/div/dl/div[2]/dd'))).text
                except:
                    ean = "None"
                print(f'EAN: {ean}')

                try:
                    information_element = WebDriverWait(product_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"desc-wrap\"]")))
                    information = information_element.text
                except:
                    information = "None"
                print(f'Information: {information}')

                print(f'URL: {product_driver.current_url}')

                quickstart.main()
                columnCount = quickstart.getColumnCount()
                RANGE_DATA = f'5!A{columnCount + 2}:J'

                quickstart.insert_data(RANGE_DATA,
                                        category1, "", title, brand, price, variant, article_number, ean, information, product_driver.current_url)
                index += 1

        product_driver.quit()
        try:
            next_url_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"next\"]")))
            next_url = next_url_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            driver.get(next_url)
        except:
            break
        sleep(3)
    print("Done!")
