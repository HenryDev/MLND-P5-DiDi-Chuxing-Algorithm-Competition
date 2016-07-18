
# coding: utf-8

from data_preprocessing import dataWrangler as dw
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def roundIt(t):
    delta=6*10e10
    return pd.DatetimeIndex(((t.astype('int64')//delta)*delta))

def districtOrders(order_df):
    time_df = dw.timer(order_df,'Time')
    driver_df = order_df[['driver_id','Time']]
    price = order_df[['driver_id','Time','Price']]

    driver_df['Time'] = roundIt(driver_df['Time'])
    driver_df.set_index('Time',inplace=True,drop=True)

    price.set_index('Time',inplace=True,drop=True)
    null_price = price[price['driver_id'].isnull()]
    completed_price = price[price['driver_id'].isnull()==False]

    null_drivers = price[price['driver_id'].isnull()]
    null_drivers = null_drivers.groupby(pd.TimeGrouper(freq='10Min')).count()
    null_drivers.drop('driver_id',axis=1,inplace=True)
    null_drivers.columns = ['nullOrders']

    completed_orders = driver_df[driver_df['driver_id'].isnull()==False]
    completed_orders = completed_orders.groupby(pd.TimeGrouper(freq='10Min')).count()
    completed_orders.columns = ['completedOrders']

    orders = order_df[['order_id','Time']]
    orders.set_index('Time',inplace=True,drop=True)
    orders = orders.groupby(pd.TimeGrouper(freq='10Min')).count()
    orders.columns = ['totalOrders']

    null_price = null_price.groupby(pd.TimeGrouper(freq='10Min')).sum()
    null_price.columns = ['totalNullPrice']

    completed_price = completed_price.groupby(pd.TimeGrouper(freq='10Min')).sum()
    completed_price.columns = ['totalCompletedPrice']

    dfs = [orders,null_drivers,null_price,completed_orders,completed_price]
    compressed_df = pd.concat(dfs,axis=1).reset_index()
    return time_df.merge(compressed_df,how='left',on='Time')

def compressDistrictData(order_data,cluster_data):
    order_data = mapOrderCluster(order_data,cluster_data)
    order_data.drop(['passenger_id','start_district_hash','dest_district_hash'],axis=1,inplace=True)
    newOrderData = pd.DataFrame()
    for i in cluster_data['district_id']:
        district_data = order_data[order_data['district_id']==i]
        district_data.drop('district_id',axis=1,inplace=True)
        district_id = pd.Series(np.ones(144)*i)
        newDistrictData = pd.concat([district_id,districtOrders(district_data)],axis=1)
        newDistrictData.rename(columns = {0:'district_id'},inplace=True)
        newOrderData = pd.concat([newOrderData,newDistrictData])
    return newOrderData

def mapOrderCluster(order_data,cluster_data):
    order_data = order_data.merge(cluster_data,how='left',
                                  left_on='start_district_hash',
                                  right_on='district_hash')
    order_data.drop('district_hash',axis=1,inplace=True)
    return order_data