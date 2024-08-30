import pandas as pd

df = pd.read_excel('DENGUE2023.xlsx')

df["month"] = df["DT_NOTIFIC"].dt.month

df = df.drop(["DT_NOTIFIC"], axis=1)

df = df.groupby(['ID_MUNICIP', 'month']).size()

print(df)

df.to_excel("DENGUE_HAZ_2023.xlsx")