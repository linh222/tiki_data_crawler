import json

import requests
import pandas as pd

cookies = {'_trackity': 'f42ea536-5842-867f-587e-1a47852be7b4',
           'TOKENS': '{%22access_token%22:%22kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9%22%2C%22expires_in%22:157680000%2C'
                     '%22expires_at%22:1829937876436%2C%22guest_token%22:%22kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9%22}',
           '_ga': 'GA1.2.1017622613.1672257935',
           'gid': 'GA1.2.656675261.1672257935',
           'tiki_client_id': '1017622613.1672257935',
           '_gat': '1'
           }
header = {'accept': 'application/json, text/plain, */*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'vi-VN,vi,;q=0.8,en-US,en;q=0.6',
          'referer': 'https://tiki.vn/sua-rua-mat-danh-cho-da-mun-innisfree-bija-trouble-facial-foam-150ml-131171093'
                     '-p25074026.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing'
                     '-v1_202212270600_MD_batched_PID.25074027&itm_medium=CPC&itm_source=tiki-reco&spid=25074027',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/108.0.0.0 Safari/537.36',
          'x-guest-token': 'kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9',
          'TE': 'Trailers',
          }

params = {'platform': 'web',
          'spid': '25074027'
          }


def parser_prod_data(json):
    d = dict()
    d['id'] = json.get('id')
    d['sold'] = json.get('all_time_quantity_sold')
    d['brand'] = json.get('brand').get('name')
    d['category'] = json.get('categories').get('name')
    d['seller'] = json.get('current_seller').get('name')
    d['day_since_created'] = json.get('day_ago_created')
    d['discount_rate'] = json.get('discount_rate')
    d['list_price'] = json.get('list_price')
    d['name'] = json.get('name')
    d['original_price'] = json.get('original_price')
    d['promotions'] = json.get('promotions')
    d['rating_avg'] = json.get('rating_average')
    d['num_review'] = json.get('review_count')
    d['review_text'] = json.get('review_text')
    d['short_description'] = json.get('short_description')
    spec = json.get('specifications')[0].get('attributes')
    for i in spec:
        d[i.get('name')] = i.get('value')

    return d

df_id = pd.read_csv("data/product_id.csv")
list_id = df_id['id'].values.tolist()
result = []

for idx, id in enumerate(list_id):
    response = requests.get('https://tiki.vn/api/v2/products/' + str(id), headers=header, params=params,
                            cookies=cookies)
    if response.status_code == 200:
        if (
                response.status_code != 204 and
                response.headers["content-type"].strip().startswith("application/json")
        ):
            try:
                result.append(response.json())
            except ValueError:
                print(idx, id)
        # decide how to handle a server that's misbehaving to this extent
    else:
        print('[WARNING] request failed')
    if idx % 5 == 0:
        print(idx)
        df = pd.DataFrame(result)
        df.to_csv("data/product_data.csv")
        print('saving successfully')
df = pd.DataFrame(result)
df.to_csv("data/product_data.csv")
