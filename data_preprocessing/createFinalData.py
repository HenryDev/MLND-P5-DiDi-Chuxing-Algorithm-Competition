# coding: utf-8

import dataWrangler as dw
import compressPoiData as cp
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.decomposition import PCA

def getAllData(poi_pca,con):
    order_info = pd.read_sql_table('compressed_districts',con=con)
    weather_info = pd.read_sql_table('weather_info',con=con)
    cluster_map = pd.read_sql_table('district_info',con=con)
    traffic_info = pd.read_sql_table('traffic_info',con=con)
    poi_info = pd.read_sql_table('poi_info',con=con)
    fixed_weather = dw.fixWeatherData(weather_info)
    fixed_traffic = dw.fixTrafficData(traffic_info,cluster_map)
    fixed_poi,expected_var = cp.compressPoiData(poi_info.fillna(0),poi_pca)
    return order_info,fixed_poi,fixed_weather,fixed_traffic

def mergeAllData((order_info,fixed_poi,fixed_weather,fixed_traffic)):
    
    OrderPoi = order_info.merge(fixed_poi,how='left',on='district_id')
    OrderPoiWeather = OrderPoi.merge(fixed_weather,how='left',on='Time')
    OrderPoiWeatherTraffic = OrderPoiWeather.merge(fixed_traffic,
                                                   how = 'left',
                                                   left_on = ['district_id','Time'],
                                                   right_on = ['district_id','Time']
                                                  )
    return OrderPoiWeatherTraffic

def createFinalData(OrderPoiWeatherTraffic): 
    filter_cols = [cols for cols in OrderPoiWeatherTraffic.columns 
                   if cols.startswith('district_hash')]
    finalData = OrderPoiWeatherTraffic.drop(filter_cols,axis=1)
    Ordered_columns = ['district_id', 'Time', 'totalOrders', 'totalNullPrice',
                       'completedOrders', 'totalCompletedPrice', 'Weather', 'temperature',
                       'pm25', 'traffic_level_1', 'traffic_level_2', 'traffic_level_3',
                       'traffic_level_4', 'poi_1', 'poi_2', 'poi_3', 'poi_4', 'poi_5','poi_6',
                       'poi_7', 'poi_8', 'poi_9', 'poi_10', 'poi_11', 'poi_12', 'poi_13',
                       'poi_14', 'poi_15', 'poi_16', 'poi_17', 'poi_18', 'poi_19', 'poi_20',
                       'poi_21', 'poi_22', 'poi_23', 'poi_24', 'poi_25','nullOrders']
    finalData = finalData[Ordered_columns].sort_values(['Time','district_id'])
    fileData = finalData.set_index('Time')
    return fileData

def writeFinalData(all_data=True,days_data=False,districts_data=False,pca_components=1,con=None):
    poi_pca = PCA(n_components=pca_components)
    fileData = createFinalData(mergeAllData(getAllData(poi_pca,con)))
    
    if all_data:
        fileData.to_csv('./final_order_info.csv',index_label='Time')
    
    elif days_data:
        for i in range(1,22):
            if i < 10:
                df = fileData.loc['2016-01-0'+str(i)]
                df.to_csv('./2016-01-0'+str(i)+'.csv',index_label='Time')
            else:
                df = fileData.loc['2016-01-'+str(i)]
                df.to_csv('./2016-01-'+str(i)+'.csv',index_label='Time')
    elif districts_data:
        for i in range(1,66):
            if i < 10:
                df = fileData[fileData['district_id']==i]
                df.to_csv('./District_0'+str(i)+'.csv',index_label='Time')
            else:
                df = fileData[fileData['district_id']==i]
                df.to_csv('./District__'+str(i)+'.csv',index_label='Time')


if __name__ == '__main__':
    engine = create_engine("mysql+mysqldb://bharat:bharat@localhost"
                           "/di_di?unix_socket=/var/run/mysqld/mysqld.sock")
    con = engine.connect()
    writeFinalData(all_data=True,districts_data=False,con=con)