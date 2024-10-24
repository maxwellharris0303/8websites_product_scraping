from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import quickstart

def scrape_data(driv, variant):
    category_parent = driv.find_element(By.CSS_SELECTOR, "ul[class=\"items\"]")
    category_elements = category_parent.find_elements(By.TAG_NAME, 'li')
    categorys = category_elements[1:-1]
    try:
        category_level1 = categorys[0].text
    except:
        category_level1 = ""
    try:
        category_level2 = categorys[1].text
    except:
        category_level2 = ""
    try:
        category_level3 = categorys[2].text
    except:
        category_level3 = ""
    try:
        category_level4 = categorys[3].text
    except:
        category_level4 = ""

    print(f'Category level 1: {category_level1}')
    print(f'Category level 2: {category_level2}')
    print(f'Category level 3: {category_level3}')
    print(f'Category level 4: {category_level4}')

    try:
        product_title = WebDriverWait(driv, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-ui-id=\"page-title-wrapper\"]"))).text
    except:
        product_title = "None"
    print(f'Product Title: {product_title}')

    try:
        brand = product_title.split()[0]
    except:
        brand = "None"
    print(f'Brand: {brand}')

    price_parent_element = driv.find_element(By.CSS_SELECTOR, "div[class=\"product-info-price\"]")
    try:
        special_price = price_parent_element.find_element(By.CSS_SELECTOR, "span[class=\"special-price\"]")
        price = special_price.find_element(By.CSS_SELECTOR, "span[class=\"price\"]").text
    except:
        try:
            simple_price = price_parent_element.find_element(By.CSS_SELECTOR, "span[class=\"simple-price\"]")
            price = simple_price.find_element(By.CSS_SELECTOR, "span[class=\"price\"]").text
        except:
            try:
                normal_price = price_parent_element.find_element(By.CSS_SELECTOR, "span[class=\"normal-price sly-normal-price\"]")
                price = normal_price.find_element(By.CSS_SELECTOR, "span[class=\"price\"]").text
            except:
                price = "None"
    print(f'Price: {price}')
    print(f'Variant: {variant}')
    article_number = "None"
    print(f'Article number: {article_number}')
    ean = "None"
    print(f'EAN: {ean}')

    try:
        information_parent = driv.find_element(By.CSS_SELECTOR, "div[class=\"product attribute overview\"]")
        information = information_parent.find_element(By.CSS_SELECTOR, "div[class=\"value\"]").text
    except:
        information = "None"
    print(f'Information: {information}')

    url = driv.current_url
    print(f'URL: {url}')

    quickstart.main()
    columnCount = quickstart.getColumnCount()
    RANGE_DATA = f'6!A{columnCount + 2}:L'

    # quickstart.insert_data(RANGE_DATA,
    #                         category_level1, category_level2, category_level3, category_level4, product_title, brand, price, variant, article_number, ean, information, url)
