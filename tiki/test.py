import pandas as pd
# df = pd.read_csv("data/product_review.csv")
# df_data = pd.read_csv('data/product_data.csv')
# print(df_data[df_data['id'].isin(df.id.values.tolist())][['id', 'review_text']])
# print(df.shape)
# print(df.columns)
# print(df.isnull().sum())
# print(df.sample(20))
# print(df.id.value_counts())



df0 = pd.read_csv("data/product_review0_26.csv")
df1 = pd.read_csv("data/product_review_26_226.csv")
df2 = pd.read_csv("data/product_review.csv")

df = pd.concat([df0, df1, df2], axis=0)
print(df.columns)
print(df.drop_duplicates(inplace=True))
print(df.shape)
print(df['id'].value_counts())
print(df[df['id']==33785195]['content'])
df.to_csv("data/product_review_total.csv",  index=False)