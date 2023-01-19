import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def crawl_data(key_dict, output_dict):
    for list_key in output_dict.keys():
        if list_key in ['list_product_id', 'list_shop_id', 'list_product_name']:
            continue

        elif list_key in ['list_variation',  'list_rating']:
            try:
                temp_list = page_source.find('div', class_=key_dict[list_key])
                try:
                    data_temp = []
                    if len(temp_list) > 1:
                        for temp in temp_list:
                            data_temp.append(temp.text)
                        output_dict[list_key].append(data_temp)
                    else:
                        output_dict[list_key].append(temp_list.text)
                except:
                    output_dict[list_key].append(temp_list.text)
            except:
                print('[WARNING] cannot crawl {} for product {}'.format(list_key,
                                                                        df_link.loc[product_index, 'product_name']))
                output_dict[list_key].append('Null')

        elif list_key == 'list_product_attribute':
            try:
                temp_list = page_source.find('div', class_=key_dict[list_key])
                try:
                    data_temp = {}
                    for tem in temp_list:
                        name_temp = ''
                        for index, te in enumerate(tem):
                            if index == 0:
                                data_temp[te.text] = ''
                                name_temp = te.text
                            elif index == 1:
                                data_temp[name_temp] = te.text
                            else:
                                data_temp[name_temp] = ''
                    output_dict[list_key].append(data_temp)
                except:
                    output_dict[list_key].append(temp_list.text)
            except:
                print('[WARNING] cannot crawl {} for product {}'.format(list_key,
                                                                        df_link.loc[product_index, 'product_name']))
                output_dict[list_key].append('Null')

        else:
            try:
                temp = page_source.find('div', class_=key_dict[list_key])
                output_dict[list_key].append(temp.text)
            except:
                print('[WARNING] cannot crawl {} for product {}'.format(list_key,
                                                                        df_link.loc[product_index, 'product_name']))
                output_dict[list_key].append('Null')
    return output_dict


data_dict = {
    'list_star': [],
    'list_num_rating': [],
    'list_sold_time': [],
    'list_price': [],
    'list_variation': [],
    'list_description': [],
    'list_product_attribute': [],
    'list_rating': [],
    'list_product_id': [],
    'list_shop_id': [],
    'list_product_name': []
}
key_dict = {
    'list_star': 'yz-vZm _2qXJwX',
    'list_num_rating': 'yz-vZm',
    'list_sold_time': 'yiMptB',
    'list_price': 'X0xUb5',
    'list_variation': 'flex items-center HiGScj',
    'list_product_attribute': 'EZi7D0',
    'list_description': 'sJarux',
    'list_rating': 'product-rating-overview__filters'
}

# số sao, lượt đánh gia, lượt bán, giá, variation, chi tiết sản phẩm, mô tả sản phẩm, rating
df_link = pd.read_csv("C:/Users/admin/PycharmProjects/tiki_data_crawler/shopee/data/product_id1.csv")
df_link = df_link.iloc[500:, :]
df_link.reset_index(drop=True, inplace=True)
for product_index in range(df_link.shape[0]):
    shop_id, product_id = df_link.loc[product_index, 'shop_id'], df_link.loc[product_index, 'product_id']
    print('Collect data for product: ', df_link.loc[product_index, 'product_name'])
    link = 'https://shopee.vn' + str(df_link.loc[product_index, 'link'])
    driver = webdriver.Chrome(
        executable_path='C:/Users/admin/PycharmProjects/tiki_data_crawler/shopee/chromedriver.exe')
    driver.get(link)
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(5)
    page_source = BeautifulSoup(driver.page_source, features="html.parser")

    data_dict = crawl_data(key_dict, data_dict)
    data_dict['list_shop_id'].append(shop_id)
    data_dict['list_product_id'].append(product_id)
    data_dict['list_product_name'].append(df_link.loc[product_index, 'product_name'])

    if product_index % 20 == 0:
        df = pd.DataFrame(data_dict)
        df.to_csv('C:/Users/admin/PycharmProjects/tiki_data_crawler/shopee/data/product_data_batch1.csv')
        print('Saving successfully at index ', product_index)
    driver.close()
    driver.quit()

df = pd.DataFrame(data_dict)
df.to_csv('C:/Users/admin/PycharmProjects/tiki_data_crawler/shopee/data/product_data_batch1.csv')
