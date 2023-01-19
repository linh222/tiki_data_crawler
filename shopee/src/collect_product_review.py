import requests
import pandas as pd
from datetime import datetime
import time

def main(df_link):
    df_full = pd.DataFrame()
    s = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={product_id}&limit=20&offset={" \
        "offset}&shopid={shop_id}&type=0"
    for product_index in range(df_link.shape[0]):
        start_time = time.time()
        shop_id, product_id = df_link.iloc[product_index, 2], df_link.iloc[product_index, 3]
        offset = 0
        ratings_url = s
        comment_data = {"user_id": [], "username": [], "product_id": [], "rating": [], "comment": [],
                        "product_name": [],
                        "cmt_date": [], "shop_id": [], "variation": [], 'detailed_rating': [], 'rating_star': []}
        rating_data = {'product_id': [], 'shop_id': [], 'rating_total': [], 'rating_count': []}
        print('collect reviews for product ' + str(df_link.iloc[product_index, 0]))
        while True:
            data = requests.get(
                ratings_url.format(shop_id=shop_id, product_id=product_id, offset=offset)
            ).json()

            rating_data['product_id'].append(product_id)
            rating_data['shop_id'].append(shop_id)
            rating_data['rating_total'].append(data["data"]['item_rating_summary']['rating_total'])
            rating_data['rating_count'].append(data["data"]['item_rating_summary']['rating_count'])

            try:
                if data["data"] is None or data['data']['ratings'] is None:
                    break
            except:
                break

            i = 1
            for i, rating in enumerate(data["data"]["ratings"], 1):
                if rating["comment"] == '':
                    continue
                else:
                    comment_data["user_id"].append(rating["userid"])
                    comment_data["username"].append(rating["author_username"])
                    comment_data["product_id"].append(rating["itemid"])
                    comment_data["rating"].append(rating["rating_star"])
                    comment_data["comment"].append(rating["comment"])
                    comment_data["cmt_date"].append(datetime.fromtimestamp(rating["ctime"]))
                    comment_data["shop_id"].append(rating["shopid"])
                    comment_data['rating_star'].append(rating['rating_star'])
                    comment_data["product_name"].append(df_link.iloc[product_index, 0])
                    try:
                        comment_data["detailed_rating"].append(rating['detailed_rating'])
                    except:
                        comment_data["detailed_rating"].append('NULL')
                    try:
                        comment_data["variation"].append(rating["product_items"][0]["model_name"])
                    except:
                        comment_data["variation"].append("NULL")

            if offset >= 3000:
                break
            offset += 20
        df_full = pd.concat([df_full, pd.DataFrame(comment_data)])
        end_time = time.time()
        print('Running time for {} is {} minutes'.format(df_link.iloc[product_index, 0], (end_time-start_time)/60))

        if product_index % 20 == 0:
            print(product_index)
            df_full.reset_index(drop=True, inplace=True)
            df_full.to_csv('shopee/data/product_review.csv',index=False)
            print('Saving successfully')

    df_full.reset_index(drop=True, inplace=True)
    df_full.to_csv("shopee/data/product_review.csv", index=False)


if __name__ == '__main__':
    df_link = pd.read_csv('shopee/data/product_id.csv')
    main(df_link)
