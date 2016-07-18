# coding: utf-8

import pandas as pd
import numpy as np

def timer(df,time):
    dates = df[time].map(lambda t: t.date()).unique()
    start = pd.to_datetime(dates.min())
    end = pd.to_datetime(dates.max()) + pd.Timedelta('1 days') - pd.Timedelta('10 Min')
    timer = pd.date_range(start,end,freq='10T')
    return pd.DataFrame(timer,columns=[time])

def fixTimeData(df):
    types = df.dtypes
    time = types[types == np.dtype('<M8[ns]')].index[0]
    timed_df = timer(df,time)
    tdf = df.set_index(time)
    tdf = tdf.groupby(pd.TimeGrouper(freq='10Min')).mean()
    tdf.reset_index(inplace=True)
    fdf = timed_df.merge(tdf,left_on=time,
                         right_on=time,how='left').fillna(method='bfill')
    return fdf

def fixWeatherData(weather_df):
    try:
        fixed_weather_df = fixTimeData(weather_df)
        return fixed_weather_df
    except:
        return None

def fixTrafficData(traffic_df,district_df):
    if 'district_id' in list(traffic_df.columns):
        traffic_df.drop('district_hash',axis=1,inplace=True)
    else:
        traffic_df = traffic_df.merge(district_df,how='left',
                                      left_on='district_hash',
                                      right_on='district_hash')
        traffic_df.drop('district_hash',axis=1,inplace=True)

    fixedTraffic_df = pd.DataFrame(columns=traffic_df.columns)
    for idx in traffic_df.district_id.sort_values().unique():
        fixedTraffic_df = fixedTraffic_df.append(fixTimeData(
            traffic_df[traffic_df['district_id']==idx]),ignore_index=True)
    return fixedTraffic_df.merge(district_df,
                                 how='left',left_on='district_id',
                                 right_on='district_id')

def parsePoiLine(line):
    l = {}
    record = line.split("\t")
    for i in record[1:]:
        if "#" in i:
            a = i.split("#")
            b = a[-1].split(":")
            l['poi_'+'#'.join(a[0:1]+b[0:1])] = int(b[1])
        else:
            a = i.split(":")
            a.insert(1,'0')
            l['poi_'+"#".join(a[:-1])] = int(a[-1])
        l['district_hash'] = record[0]
        df = pd.Series(l).reset_index().T.reset_index(drop=True)
        df.columns = df.iloc[0]
        df.drop(0,axis=0,inplace=True)
    return df

def readPoiData(infile,fillna=False):
    df = pd.DataFrame()
    with open(infile,'r') as poi_data:
        for line in poi_data:
            df = pd.concat([df,parsePoiLine(line)])
    df.reset_index(inplace=True,drop=True)
    for col in df.columns:
        try:
            df[col] = df[col].astype('float64')
        except:
            pass
    if type(fillna)==bool and fillna==True:
        df = df.fillna(0)
    elif fillna:
        df = df.fillna(fillna)
    else:
        pass
    return df

def getTrafficLevels(level):
    try:
        level = int(level.split(":")[1])
        return level
    except:
        return level


def compressPoiData(poiData,cluster_map,pca):
    poiData = poiData.merge(cluster_map,how='left',on='district_hash')
    var = {}
    pois = {}
    pois_pca = {}
    for i in range(1,26):
        cols = [col for col in poiData.columns if 'poi_'+str(i)+'#' in col]
        if len(cols)>1:
            pois[i] = poiData[cols]
        else:
            pois_pca[i] = poiData[cols].values
            pois_pca[i] = pois_pca[i].reshape(66)
            var[i] = 1.0

    for i in pois:
        X = pois[i].values
        pca.fit(X)
        var[i] = pca.explained_variance_[0]
        pois_pca[i] = pca.transform(X)
        pois_pca[i] = pois_pca[i].reshape(66)
    compressed_poi = pd.DataFrame(pois_pca)
    compressed_poi[['district_hash','district_id']] = poiData[['district_hash'
                                                               ,'district_id']]
    compressed_poi.columns = ['poi_'+str(col) for col in 
                              compressed_poi.columns if col 
                              not in ['district_hash',
                                      'district_id']]+['district_hash',
                                                       'district_id']
    return compressed_poi,var

def fixOrderData(orderdf,clusterdf):
    orderMap = orderdf.merge(clusterdf,how='left',
                             left_on='start_district_hash',
                             right_on='district_hash')

    notImp = ['order_id','start_district_hash','dest_district_hash',
          'district_hash','passenger_id','Price']

    impOrders = orderMap.drop(notImp,axis = 1)
    impOrders.set_index(['Time'],inplace=True,drop=True)
    impOrders['nullOrders'] = impOrders['driver_id'].isnull().apply(
        lambda x: 0 if x else 1)

    nullOrders = impOrders[impOrders['nullOrders']==0].drop('driver_id',axis=1)
    groupedImp = nullOrders.groupby(['district_id',
                                 pd.TimeGrouper(freq='10Min',level='Time')])
    gapOrders = groupedImp.count().reset_index('Time')
    timedf = timer(gapOrders,'Time')
    fixedOrders = pd.DataFrame()
    for i in gapOrders.index.unique():
        tempdf = pd.DataFrame()
        timedf['district_id'] = i
        tempdf = tempdf.append(pd.DataFrame(gapOrders.loc[[i]]))
        fixedOrders = pd.concat([fixedOrders,tempdf.merge(timedf,
                                                          how='right',
                                                          left_on='Time',
                                                          right_on='Time')]
                                ,axis=0)
    return fixedOrders
