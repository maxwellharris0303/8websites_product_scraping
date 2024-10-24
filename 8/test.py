from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.123watersport.nl/oogplaat-rvs-rond-met-schroefdraad.html")
sleep(2)
category_parent = driver.find_element(By.CSS_SELECTOR, "ol[class=\"d-flex hide-575\"]")
category_elements = category_parent.find_elements(By.TAG_NAME, 'a')
print(len(category_elements))
categorys = category_elements[1:]
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
sleep(1000)