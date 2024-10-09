import pandas as pd
from datetime import datetime
from climada.util import *
import os

class Conversor():

    def convert_datasus_data(file_name = 'DENGUE2023.xlsx',by_month_only = True, max_month = 12, end_file_name = "HazardDatasus.csv"):

        file_path = os.path.join(SYSTEM_DIR, file_name)

        df = pd.read_excel(file_path)

        df["month"] = df["DT_NOTIFIC"].dt.month

        df = df.drop(["DT_NOTIFIC"], axis=1)

        dff = df.drop(["month"], axis=1)

        df = df.groupby(['ID_MUNICIP', 'month']).size().reset_index()

        print(df)

        # -----

        dff = dff.drop_duplicates()

        dff = dff.sort_values(by= ['ID_MUNICIP'])

        if(by_month_only):
            num = df['month'].max()

            if(num > max_month):
                num = max_month
        else:
            num = len(df)

        for n in range(1, num+1):
            if(by_month_only):
                dfmonth = df.loc[df['month'] == n]
            else:
                print("Loop 1 : ", n-1)

                dfmonth = df.iloc[[n-1]]

            dff = dff.merge(dfmonth, on= 'ID_MUNICIP', how= 'left')

            dff.rename(columns = { '0_x' : "event" + str(n-1),
                                '0_y' : "event" + str(n)}, 
                        inplace = True)
            
            dff = dff.drop(['month'], axis=1)

        dff = dff.fillna(0)

        if(num % 2 == 1):
            dff = dff.rename(columns = {0 : 'event' + str(num)})

        dff['n_events'] = num

        print(dff)

        # -----

        file_path_2 = os.path.join(SYSTEM_DIR, 'municipios.csv')

        df1 = pd.read_csv(file_path_2)

        df1 = df1.drop(["uf_code" ,"mesoregion","microregion","rgint","rgi",
                        "osm_relation_id","wikidata_id","is_capital","wikipedia_pt","no_accents",
                        "slug_name","alternative_names"], axis=1)

        df1["ID_MUNICIP"] = df1["municipio"].apply(lambda x: int(x/10))

        dff = dff.merge(df1, on="ID_MUNICIP", how="inner")

        dff = dff.drop(["uf", "name", "ID_MUNICIP", "municipio"], axis=1)

        dff["haz_type"] = "DN"

        num = dff['n_events'].values[0]

        for n in range(0, num):
            dff['event' + str(n+1)] = dff['event' + str(n+1)].astype(float)

        for n in range(0, num):
            dff['event'+str(n+1)] = dff['event'+str(n+1)] / dff['pop_21']

        print(dff)

        file_path_final = os.path.join(SYSTEM_DIR, end_file_name)
        dff.to_csv(file_path_final)

    def convert_news_data(file_name = 'dengue_hazzards_news.xlsx', severity_threshold = 0, by_month_only = True, max_month = 12, end_file_name = "HazardNews.csv"):

        file_path = os.path.join(SYSTEM_DIR, file_name)

        df = pd.read_excel(file_path)

        df1 = df['event_main_location'].str.split(',', expand=True)

        df['lat'] = df1[0].apply(lambda x: float(x))
        df['lon'] = df1[1].apply(lambda x: float(x))

        df['date'] = df['event_main_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

        df['month'] = df['date'].dt.month

        df = df.drop(df[df['Severity of Event'] <= severity_threshold].index)

        df = df.drop(["SOURCEURL", "title", "text", "media", "Unnamed: 0", "Unnamed: 0.1",
                    "crawler_topic", "event_main_location", "event_main_date_str", "event_main_date",
                        "date", "Description of Hazard", "Type of Hazard", "Severity of Event"], axis=1)

        df_alt = df.drop(["lat", "lon"], axis=1)

        df1 = df_alt.groupby(['event_places', 'month']).mean().reset_index()

        dfinal = df.drop(['Intensity of Event', 'month'], axis=1)
        dfinal = dfinal.drop_duplicates()
        dfinal['haz_type'] = 'DN'

        if(by_month_only):
            num = df['month'].max()
            if(num > max_month):
                num = max_month
        else:
            num = len(df1)

        for n in range(1, num+1):
            if(by_month_only):
                dfmonth = df1.loc[df1['month'] == n]
            else:
                dfmonth = df1.iloc[[n-1]]

            dfinal = dfinal.merge(dfmonth, on= 'event_places', how= 'left')

            dfinal.rename(columns = { 'Intensity of Event_x' : "event" + str(n-1),
                                'Intensity of Event_y' : "event" + str(n)}, 
                        inplace = True)
            
            dfinal = dfinal.drop(['month'], axis=1)

        dfinal = dfinal.fillna(0)

        if(num % 2 == 1):
            dfinal = dfinal.rename(columns = {'Intensity of Event' : 'event' + str(num)})

        dfinal['n_events'] = num

        print(dfinal)


        file_path_final = os.path.join(SYSTEM_DIR, end_file_name)
        dfinal.to_csv(file_path_final)