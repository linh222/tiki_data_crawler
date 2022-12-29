import pandas as pd
df = pd.read_csv("data/product_review.csv")
df_data = pd.read_csv('data/product_data.csv')
print(df_data[df_data['id'].isin(df.id.values.tolist())][['id', 'review_text']])
print(df.shape)
print(df.columns)
print(df.isnull().sum())
print(df.sample(20))
print(df.id.value_counts())