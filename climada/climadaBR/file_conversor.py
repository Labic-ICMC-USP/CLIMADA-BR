import pandas as pd
from datetime import datetime
from climada.util import *
import os

class Conversor():

    def convert_datasus_data(df, by_month_only = True, max_month = 12):

        # Reading the dataframe

        #file_path = os.path.join(SYSTEM_DIR, file_name)

        #df = pd.read_excel(file_path)

        # Taking the year for said cases

        year = df.loc[1, "DT_NOTIFIC"].year

        # Gruping by month to calculate number of cases in said month in each city

        df["month"] = df["DT_NOTIFIC"].dt.month

        df = df.drop(["DT_NOTIFIC"], axis=1)

        dff = df.drop(["month"], axis=1) # Saving in the dff the previous df to use the locations later

        df = df.groupby(['ID_MUNICIP', 'month']).size().reset_index()

        print(df)

        # Organizing dff to have the locations without duplicates

        dff = dff.drop_duplicates()

        dff = dff.sort_values(by= ['ID_MUNICIP'])

        # Taking out events from months above max_month

        df = df.drop(df[df['month'] > max_month].index)

        if(by_month_only):
            num = df['month'].max()
        else:
            num = len(df)

        df_date = pd.DataFrame()

        # Creating events and adding them to the dff dataframe

        for n in range(1, num+1):
            # Taking a single event and putting it in the dfmonth

            if(by_month_only):
                dfmonth = df.loc[df['month'] == n]
            else:
                print("Loop 1 : ", n-1)

                dfmonth = df.iloc[[n-1]]

            # Merge the event into dff

            dff = dff.merge(dfmonth, on= 'ID_MUNICIP', how= 'left')

            dff.rename(columns = { '0_x' : "event" + str(n-1),
                                '0_y' : "event" + str(n)}, 
                        inplace = True)
            
            # Taking hte date of hte current event
            
            df_date.loc[n-1, 'date'] = datetime(year, int(dff['month'].loc[dff['month'].first_valid_index()]), 15)
            
            dff = dff.drop(['month'], axis=1)

        dff = dff.fillna(0)

        if(num % 2 == 1):
            dff = dff.rename(columns = {0 : 'event' + str(num)})

        # Addind number of evens to the dff datafram

        dff['n_events'] = num

        # Joining the dates wiht the dff dataframe

        if(len(df_date) > len(dff)):
            dff = dff.join(df_date['date'], how='right')
        else:
            dff = dff.join(df_date['date'], how='left')

        print(dff)

        # Reading municipios.csv file into a dataframe to take population size data

        file_path_2 = os.path.join(SYSTEM_DIR, 'municipios.csv')

        df1 = pd.read_csv(file_path_2)

        df1 = df1.drop(["uf_code" ,"mesoregion","microregion","rgint","rgi",
                        "osm_relation_id","wikidata_id","is_capital","wikipedia_pt","no_accents",
                        "slug_name","alternative_names"], axis=1)
        
        # Adequating ID of the location form the two dataframes (dff and df1)

        df1["ID_MUNICIP"] = df1["municipio"].apply(lambda x: int(x/10))

        # Merging dataframes

        dff = dff.merge(df1, on="ID_MUNICIP", how="inner")

        dff = dff.drop(["uf", "name", "ID_MUNICIP", "municipio"], axis=1)

        # Adding hazard type to the dff dataframe

        dff["haz_type"] = "DN"

        # Dividing number of cases by population size to obtain percentage of affected population, which will be our Intensity value

        num = dff['n_events'].values[0]

        for n in range(0, num):
            dff['event' + str(n+1)] = dff['event' + str(n+1)].astype(float)

        for n in range(0, num):
            dff['event'+str(n+1)] = dff['event'+str(n+1)] / dff['pop_21']

        #print(dff)

        return(dff)

    def convert_news_data(df, use_severity_threshold = False, severity_threshold = 0.1, by_month_only = True, max_month = 12, regulated = False):

        # Reading the dataframe from a file

        #file_path = os.path.join(SYSTEM_DIR, file_name)

        #df = pd.read_excel(file_path)

        # Separating the latitude and longitude values

        df1 = df['event_main_location'].str.split(',', expand=True)

        df['lat'] = df1[0].apply(lambda x: float(x))
        df['lon'] = df1[1].apply(lambda x: float(x))

        # Taking month and year from the date string

        df['date'] = df['event_main_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

        df['month'] = df['date'].dt.month

        year = df.loc[1, "date"].year

        # This comment below was for dropping events below the severity threshold

        if(use_severity_threshold):
            df = df.drop(df[df['Severity of Event'] <= severity_threshold].index)
        else:
            # Calculating new intensity by multiplying intensity and severity

            if(regulated):
                df['Intensity of Event'] = df['Intensity of Event'] * df['gcn_scores']
            else:
                df['Intensity of Event'] = df['Intensity of Event'] * df['Severity of Event']

        # Dropping unneeded colums

        df = df.drop(["SOURCEURL", "title", "text", "media", "Unnamed: 0", "Unnamed: 0.1",
                    "crawler_topic", "event_main_location", "event_main_date_str", "event_main_date",
                        "date", "Description of Hazard", "Type of Hazard", "Severity of Event"], axis=1)
        
        if(regulated):
            df = df.drop(["gcn_scores", "features"], axis=1)
        
        # Taking the average intensity by taking events from the same place and same month

        df_alt = df.drop(["lat", "lon"], axis=1)

        df1 = df_alt.groupby(['event_places', 'month']).mean().reset_index()

        # Creating dfinal which are the locations at this moment

        dfinal = df.drop(['Intensity of Event', 'month'], axis=1)

        dfinal = dfinal.drop_duplicates()

        # Adding hazard type to the dataframe

        dfinal['haz_type'] = 'DN'

        # Dropping events form months greater than max_month

        df1 = df1.drop(df1[df1['month'] > max_month].index)

        if(by_month_only):
            num = df1['month'].max()
        else:
            num = len(df1)

        df_date = pd.DataFrame()

        # Creating events and adding them to the dfinal dataframe

        for n in range(1, num+1):
            # Creating the event and putting it into dfmonth

            if(by_month_only):
                dfmonth = df1.loc[df1['month'] == n]
            else:
                dfmonth = df1.iloc[[n-1]]

            # Merging dfinal and dfmonth

            dfinal = dfinal.merge(dfmonth, on= 'event_places', how= 'left')

            dfinal.rename(columns = { 'Intensity of Event_x' : "event" + str(n-1),
                                'Intensity of Event_y' : "event" + str(n)}, 
                        inplace = True)
            
            # Taking the date of the current event
            
            df_date.loc[n-1, 'date'] = datetime(year, int(dfinal['month'].loc[dfinal['month'].first_valid_index()]), 15)
            
            dfinal = dfinal.drop(['month'], axis=1)

        dfinal = dfinal.fillna(0)

        # Joining date with the dfinal dataframe

        if(len(df_date) > len(dfinal)):
            dfinal = dfinal.join(df_date['date'], how='right')
        else:
            dfinal = dfinal.join(df_date['date'], how='left')

        if(num % 2 == 1):
            dfinal = dfinal.rename(columns = {'Intensity of Event' : 'event' + str(num)})

        # Adding number of events to the dfinal dataframe

        dfinal['n_events'] = num

        #print(dfinal)

        return(dfinal)