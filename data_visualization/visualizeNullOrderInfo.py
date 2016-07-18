# coding: utf-8

from matplotlib import pylab as py
from matplotlib.dates import MinuteLocator
from pylab import rcParams
import pandas as pd
import datetime as dt

def getfileName(i):
    if i<10:
        return 'features_2016-01-0'+str(i)
    else:
        return 'features_2016-01-'+str(i)


def getNullData(file_loc,file_name):
    return pd.read_csv(file_loc+file_name, parse_dates=[0])[['Time','nullOrders']]


def plotNullOrders(district,df):
    date = pd.Timestamp.date(df['Time'].iloc[0])
    py.figure(figsize=(20,10))
    py.plot(df['Time'],df['nullOrders'])
    py.xlabel('Time')
    py.ylabel('nullOrders')
    py.grid()
    py.title('Null orders across time in District {0} on {1}'.format(str(district),str(date)))
    py.show()
    return None

def plotDistrictNullOrders(file_loc,district_id,df):
    df2 = df[df['district_id']==district_id]
    plotNullOrders(district_id,df2[['Time','nullOrders']])
    return Nonw

def plotDistrictsInDay(df,agg=None,avg=None):
    if agg:
        timedf = timedf = df[['Time','nullOrders']]
        nullsdf = timedf.groupby('Time').sum()
        nullsdf.reset_index(inplace=True)
        return py.plot(nullsdf.Time.apply(lambda x: pd.Timestamp.time(x)),nullsdf.nullOrders)
    elif avg:
        timedf = timedf = df[['Time','nullOrders']]
        nullsdf = timedf.groupby('Time').mean()
        nullsdf.reset_index(inplace=True)
        return py.plot(nullsdf.Time.apply(lambda x: pd.Timestamp.time(x)),nullsdf.nullOrders)
    else:
        return py.plot(df.Time.apply(lambda x: pd.Timestamp.time(x)),df.nullOrders)

def plotDistrictsInAllDays(file_loc,agg=None,avg=None):
    py.figure(figsize=(20,10))
    for i in range(1,22):
        file_name = getfileName(i)
        df = getNullData(file_loc,file_name)
        plt = plotDistrictsInDay(df,agg,avg)
    py.grid()
    py.show()


def aggregateDaysandDistricts(file_loc,agg=None,avg=None):
    wholeSum = pd.DataFrame()
    for i in range(1,22):
        file_name = getfileName(i)
        daily = getNullData(file_loc,file_name)
        daily['Time'] = daily['Time'].apply(lambda x: pd.Timestamp.time(x))
        dailySum = daily.groupby('Time').sum()
        wholeSum = pd.concat([wholeSum,dailySum],axis=1)
    if agg:
        return wholeSum.sum(axis=1)
    elif avg:
        return wholeSum.mean(axis=1)

def plotAggregates(file_loc,agg=None,avg=None):
    aggs = aggregateDaysandDistricts(file_loc,agg,avg)
    py.figure(figsize=(15,10))
    py.plot(aggs.index,aggs)
    py.grid()
    py.xlabel("Time")
    if agg:
        py.ylabel("Sum of Nulls")
        py.title("Total Null Orders per timesolt")
    elif avg:
        py.ylabel("Mean of Nulls")
        py.title("Mean of Null orders per timeslot")
    py.show()
    return None


if __name__ == '__main__':
    file_loc = '../data_preprocessing/features/'
    plotAggregates(file_loc,avg=True)
