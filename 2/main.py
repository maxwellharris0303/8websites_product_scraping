from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
from bs4 import BeautifulSoup

url = "https://www.bootland.nl"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(url)
sleep(3)
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
ul_element = soup.find('ul', class_='menu-items')
li_elements = ul_element.find_all('a', class_='nav-link')
# print(li_elements)
# print(len(li_elements))
product_list_driver = webdriver.Chrome()
product_list_driver.maximize_window()
for list in li_elements:
    soup = BeautifulSoup(str(list), 'html.parser')
    a_tag = soup.find('a')
    href = a_tag.get('href')
    list_url = url + href
    print(list_url)
    product_list_driver.get(list_url)

    # write scrape code


    sleep(3)

sleep(1000)