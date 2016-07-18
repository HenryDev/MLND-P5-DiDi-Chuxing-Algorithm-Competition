# coding: utf-8
from utilities import file_names as fn
from utilities import file_reader as fr
from data_preprocessing import dataWrangler as dw
import pandas as pd

def getOrderData(orderFiles,clusterFiles):
    clusterFile = clusterFiles.values()[0]
    clusters = fr.read_cluster_file(clusterFile)
    orderInfo = pd.DataFrame()
    for v in orderFiles.itervalues():
        rawOrders = fr.read_order_file(v)
        orderInfo = pd.concat([orderInfo,dw.fixOrderData(rawOrders,clusters)])
    orderInfo.reset_index(inplace=True,drop=True)
    return orderInfo.sort_values(['district_id','Time'])

def getWeatherData(weatherFiles):
    weatherInfo = pd.DataFrame()
    for v in weatherFiles.itervalues():
        rawWeather = fr.read_weather_file(v)
        weatherInfo = pd.concat([weatherInfo,dw.fixWeatherData(rawWeather)])
    weatherInfo.reset_index(inplace=True,drop=True)
    return weatherInfo.sort_values(['Time'])

def getTrafficData(trafficFiles,clusterFiles):
    clusterFile = clusterFiles.values()[0]
    clusters = fr.read_cluster_file(clusterFile)
    trafficInfo = pd.DataFrame()
    for v in trafficFiles.itervalues():
        rawTraffic = fr.read_traffic_file(v)
        trafficInfo = pd.concat([trafficInfo,
                                 dw.fixTrafficData(rawTraffic,clusters)])
    trafficInfo.reset_index(inplace=True,drop=True)
    trafficInfo.drop('district_hash',axis=1,inplace=True)
    return trafficInfo.sort_values(['district_id','Time'])

def getPoiData(poiFiles,clusterFiles):
    clusterFile = clusterFiles.values()[0]
    clusters = fr.read_cluster_file(clusterFile)
    poiFile = poiFiles.values()[0]
    rawPoi = fr.read_poi_file(poiFile)
    poiInfo = rawPoi.merge(clusters,
                           on='district_hash').drop('district_hash',axis=1)
    return poiInfo.sort_values(['district_id'])


if __name__ == '__main__':
    allFiles = getAllFiles()
    trainOrders,testOrders = allFiles['order']
    trainClusters,testClusters = allFiles['cluster']
    orders = getOrderData(testOrders,testClusters)

    print orders.head()
    print orders.shape
