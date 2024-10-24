from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep

url = "https://www.boottotaal.nl/bootuitrusting-opbergen-inspectie-en-ventilatie-ve.html"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(url)
sleep(3)

product_list_elements = driver.find_element(By.CSS_SELECTOR, "ol[class=\"d-flex hide-575\"]")
print(product_list_elements)

sleep(1000)