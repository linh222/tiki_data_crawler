import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

df_link = pd.read_csv('/Users/linhtran/PycharmProject/cleaner_crawl/tiki_data_crawler/shopee/data/product_id.csv')
list_link = []
list_prod_id = []
list_shop_id = []
for product_index in range(df_link.shape[0]):
    shop_id, product_id = df_link.loc[product_index, 'shop_id'], df_link.loc[product_index, 'product_id']
    print('Collect data for product: ', df_link.loc[product_index, 'product_name'])
    link = 'https://shopee.vn' + str(df_link.loc[product_index, 'link'])
    driver = webdriver.Chrome(
        executable_path='/Users/linhtran/PycharmProject/cleaner_crawl/tiki_data_crawler/shopee/chromedriver')
    driver.get(link)
    time.sleep(10)
    page_source = BeautifulSoup(driver.page_source, features="html.parser")

    try:
        data = page_source.find('div', class_='VWiifV qO2bZw')
        link = data.get('style').split(' ')[1][5:-3]
    except:
        try:
            data = page_source.find('video', class_='_82gzM6')
            link = data.get('src')
        except:
            print('No image for product ', df_link.loc[product_index, 'product_name'])
            link = 'nan'
    list_link.append(link)
    list_shop_id.append(shop_id)
    list_prod_id.append(product_id)
    if product_index % 20 == 0:
        df = pd.DataFrame()
        df['image_link'] = list_link
        df['product_id'] = list_prod_id
        df['shop_id'] = list_shop_id
        df.to_csv('/Users/linhtran/PycharmProject/cleaner_crawl/tiki_data_crawler/shopee/data/image_prod.csv',
                  index=False)
        print('Saving successfully at index ', product_index)
    driver.close()
    driver.quit()

df = pd.DataFrame()
df['image_link'] = list_link
df['product_id'] = list_prod_id
df['shop_id'] = list_shop_id
df.to_csv('/Users/linhtran/PycharmProject/cleaner_crawl/tiki_data_crawler/shopee/data/image_prod.csv',
          index=False)
print('Saving successfully')

    # import requests
    #
    # with open('pic1.jpg', 'wb') as handle:
    #     response = requests.get('https://cf.shopee.vn/file/sg-11134201-22120-f4lfl3wihvkv3d', stream=True)
    #
    #     if not response.ok:
    #         print(response)
    #
    #     for block in response.iter_content(1024):
    #         if not block:
    #             break
    #
    #         handle.write(block)