import pandas as pd
import requests
import ast

df_data = pd.read_csv('data/product_data.csv')


def process_review_text(row):
    if row == 'Chưa có đánh giá':
        return 0
    else:
        return int(row[1:-1])


df_data['review_text'] = df_data['review_text'].apply(process_review_text)
df_data = df_data.iloc[1:5, :]
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

params = {'limit': '5',
          'include': 'comments,contribute_info,attribute_vote_summary',
          'sort': 'score|desc,id|desc,stars|all',
          'page': '1',
          'spid': '25074027',
          'product_id': '25074026',
          'seller_id': 1
          }

result = []

for idx, id in enumerate(df_data['id'].values.tolist()):
    params['product_id'] = id
    if df_data[df_data['id'] == id]['review_text'].values[0] >= 5:
        seller_id = ast.literal_eval(df_data[df_data['id'] == id]['current_seller'].values[0]).get('id')
        params['seller_id'] = seller_id
        params['spid'] = id
        for i in range(df_data[df_data['id'] == id]['review_text'].values[0] // 5):
            params['page'] = i
            response = requests.get('https://tiki.vn/api/v2/reviews', headers=header, params=params, cookies=cookies)
            if response.status_code == 200:
                if (
                        response.status_code != 204 and
                        response.headers["content-type"].strip().startswith("application/json")
                ):
                    try:
                        if len(response.json().get('data')) > 0:
                            temp = response.json().get('data')[0]
                            temp['id'] = id
                            result.append(temp)
                    except ValueError:
                        print(idx, id)
                # decide how to handle a server that's misbehaving to this extent
            else:
                print('[WARNING] request failed')
    if idx % 5 == 0:
        print(idx)
        df = pd.DataFrame(result)
        df.to_csv("data/product_review.csv", index=False)
        print('saving successfully')
df = pd.DataFrame(result)
df.to_csv("data/product_review.csv", index=False)
