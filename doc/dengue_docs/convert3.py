import pandas as pd

df = pd.read_excel('DENGUE_HAZ_BY_MONTH.xlsx')

df1 = pd.read_csv('municipios.csv')

df1 = df1.drop(["uf_code" ,"mesoregion","microregion","rgint","rgi",
                "osm_relation_id","wikidata_id","is_capital","wikipedia_pt","no_accents",
                "slug_name","alternative_names"], axis=1)

df1["ID_MUNICIP"] = df1["municipio"].apply(lambda x: int(x/10))

df = df.merge(df1, on="ID_MUNICIP", how="inner")

df = df.drop(["uf", "name", "ID_MUNICIP", "municipio", "Unnamed: 0"], axis=1)

df["haz_type"] = "DN"

num = df['n_events'].values[0]

for n in range(0, num):
    df['event' + str(n+1)] = df['event' + str(n+1)].astype(float)

for n in range(0, num):
    df['event'+str(n+1)] = df['event'+str(n+1)] / df['pop_21']

print(df)

df.to_excel("TabelaDengueCoordMonth.xlsx")