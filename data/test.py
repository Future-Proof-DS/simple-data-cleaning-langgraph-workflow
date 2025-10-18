import pandas as pd

df = pd.read_csv("../data/missing.csv")
# print(df.describe())
# print(df.info())
print(df.isnull().sum())

