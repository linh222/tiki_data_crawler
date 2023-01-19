import time
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
link = 'https://shopee.vn/search?keyword=s%E1%BB%AFa%20r%E1%BB%ADa%20m%E1%BA%B7t&trackingId=searchhint-1672692548-e71d01b4-8ade-11ed-af58-f4ee0816d18c'
driver = webdriver.Chrome(
    executable_path='shopee/chromedriver.exe')
driver.get(link)
time.sleep(2)
# load page

list_name = []
list_link = []
list_shopid = []
list_prod_id = []
count=0
for i in range(50):
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    page_source = BeautifulSoup(driver.page_source, features="html.parser")
    names = page_source.find_all('div', class_='ie3A+n bM+7UW Cve6sh')
    print("parsing success")
    for name in names:
        list_name.append(name.text)

    links = page_source.find_all('a', attrs={"data-sqe": "link"})
    for link in links:
        list_link.append(link.get('href'))
        r = re.search(r"i\.(\d+)\.(\d+)", link.get('href'))
        shop_id, item_id = r[1], r[2]
        list_shopid.append(shop_id)
        list_prod_id.append((item_id))

    button = driver.find_element(By.XPATH, "//button[@class='shopee-icon-button shopee-icon-button--right ']")
    current_last_button = driver.find_elements(By.XPATH,
                                               "//button[@class='shopee-button-no-outline shopee-button-no-outline--non-click']")
    if len(current_last_button) == 1:
        count += 1
        if count == 50:
            break
    button.click()
    if i % 1 ==0:
        df_link = pd.DataFrame()
        df_link['product_name'] = list_name
        df_link['link'] = list_link
        df_link['shop_id'] = list_shopid
        df_link['product_id'] = list_prod_id
        df_link.to_csv('shopee/data/product_id.csv', index=False)
        print("[INFO] Saving successfully at {} with {} products".format(i, len(list_shopid)))
driver.close()
driver.quit()

df_link = pd.DataFrame()
df_link['product_name'] = list_name
df_link['link'] = list_link
df_link['shop_id'] = list_shopid
df_link['product_id'] = list_prod_id
df_link.to_csv('shopee/data/product_id.csv', index=False)