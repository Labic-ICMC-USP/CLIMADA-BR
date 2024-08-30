import pandas as pd

df = pd.read_excel('DENGUE2023.xlsx')

df = df.drop(['DT_NOTIFIC'], axis = 1)

df = df.drop_duplicates()

df = df.sort_values(by= ['ID_MUNICIP'])

df1 = pd.read_excel('DENGUE_HAZ_2023.xlsx')

df1 = df1.ffill()

num = df1['month'].max()

for n in range(1, num+1):
    dfmonth = df1.loc[df1['month'] == n]

    df = df.merge(dfmonth, on= 'ID_MUNICIP', how= 'left')

    df.rename(columns = { '0_x' : "event" + str(n-1),
                         '0_y' : "event" + str(n)}, 
                inplace = True)
    
    df = df.drop(['month'], axis=1)

df = df.fillna(0)

df = df.rename(columns = {df.columns[num] : 'event' + str(num)})

df['n_events'] = num

print(df)

df.to_excel('DENGUE_HAZ_BY_MONTH.xlsx')