import requests
import time
import pandas as pd
import random

cookies = {'_trackity':'f42ea536-5842-867f-587e-1a47852be7b4',
           'TOKENS':'{%22access_token%22:%22kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1829937876436%2C%22guest_token%22:%22kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9%22}',
           '_ga':'GA1.2.1017622613.1672257935',
           'gid': 'GA1.2.656675261.1672257935',
           'tiki_client_id': '1017622613.1672257935',
           '_gat': '1'
}
header = {'accept': 'application/json, text/plain, */*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'vi-VN,vi,;q=0.8,en-US,en;q=0.6',
          'referer': 'https://tiki.vn/sua-rua-mat/c1583',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
          'x-guest-token': 'kax4WoQfzPUY2mhKri1sFbCJVDe0X8w9',
          'TE': 'Trailers',
          }

params = {'limit': '40',
          'include': 'advertisement',
          'aggregations': '2',
          'trackity_id': 'f42ea536-5842-867f-587e-1a47852be7b4',
          'category': '1583',
          'page': '1',
          'urlKey': 'sua-rua-mat'
          }

prod_id = []
for i in range(1, 41):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=header, params=params)
    if response.status_code == 200:
        print('[INFO] request success...')
        for record in response.json().get('data'):
            prod_id.append({'id': record.get('id'),
                            'name': record.get('name')})
    time.sleep(random.randrange(3, 10))
    if i % 5 ==0:
        df = pd.DataFrame(prod_id)
        df.to_csv("data/product_id.csv")

df = pd.DataFrame(prod_id)
df.to_csv("data/product_id.csv")