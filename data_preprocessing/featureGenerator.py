# coding: utf-8
import os
from utilities import file_reader as fr
from utilities import file_names as fn
from data_preprocessing import dataWrangler as dw
from data_preprocessing import dataBlender as db
import pandas as pd
import numpy as np
from pprint import pprint


def preProcessData(train=True,test=None):
    trainFiles,testFiles = fn.getAllFiles(train,test)
    trainData,testData = None,None
    if trainFiles:
        trainOrder = db.getOrderData(trainFiles['order'],trainFiles['cluster'])
        trainWeather = db.getWeatherData(trainFiles['weather'])
        trainTraffic = db.getTrafficData(trainFiles['traffic'],
                                         trainFiles['cluster'])
        trainPoi = db.getPoiData(trainFiles['poi'],trainFiles['cluster'])
        trainData = mergeAllData(trainOrder,trainWeather,trainTraffic,trainPoi)
        trainData.sort_values(['district_id','Time'],inplace=True)
        trainData.reset_index(inplace=True,drop=True)


    if testFiles:
        testOrder = db.getOrderData(testFiles['order'],testFiles['cluster'])
        testWeather = db.getWeatherData(testFiles['weather'])
        testTraffic = db.getTrafficData(testFiles['traffic'],
                                        testFiles['cluster'])
        testPoi = db.getPoiData(testFiles['poi'],testFiles['cluster'])
        testData = mergeAllData(testOrder,testWeather,testTraffic,testPoi)
        testData.sort_values(['district_id','Time'],inplace=True)
        testData.reset_index(inplace=True,drop=True)


    return trainData,testData

def mergeAllData(order_info,fixed_weather,fixed_traffic,fixed_poi):

    OrderPoi = order_info.merge(fixed_poi,how='left',on='district_id')
    OrderPoiWeather = OrderPoi.merge(fixed_weather,how='left',on='Time')
    OrderPoiWeatherTraffic = OrderPoiWeather.merge(fixed_traffic,
                                                   how = 'left',
                                                   left_on = ['district_id','Time'],
                                                   right_on = ['district_id','Time']
                                                  )
    return OrderPoiWeatherTraffic

def writeFileData(fileData,test=None,train=None):
    path = '../data_preprocessing/features'
    if not os.path.exists(path):
        os.makedirs(path)
    if test:
        fname = path+'/testData.csv'
        print fname
        fileData.to_csv(fname,index=False)
    if train:
        fname = path+'/trainData.csv'
        print fname
        fileData.to_csv(fname,index=False)
    else:
        pass

if __name__ == '__main__':
    trainData,testData = preProcessData(train=True,test=True)
    writeFileData(testData,test=True)
    writeFileData(trainData,train=True)
