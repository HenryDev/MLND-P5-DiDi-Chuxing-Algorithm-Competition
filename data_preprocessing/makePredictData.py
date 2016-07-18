import pandas as pd
from data_preprocessing import getData as gd
import os
import numpy as np


def load_training_data(file_path='./features/trainData.csv'):
    if file_path is None:
        file_path = 'features/allData'
    return pd.read_csv(file_path, parse_dates=[0], index_col=['Time'])


def makeFeatures(df):
    feats = df.fillna(0)
    #unImportant = ['totalNullPrice', 'completedOrders', 'totalCompletedPrice', 'totalOrders']
    #feats = fixnandf.drop(unImportant, axis=1).fillna(0)
    feats.reset_index(inplace=True)
    return feats


def removePois(df):
    return df[[col for col in df.columns if not col.startswith('poi')]]


def splitTrainTestDays(df, testDays=None):
    if testDays:
        val = testDays * 144 * 66
    else:
        val = 2 * 144 * 66
    daysdf = df.sort_values(['Time', 'district_id'])
    daysdf.reset_index(inplace=True, drop=True)
    traindays, testdays = daysdf.iloc[:-val], daysdf.iloc[-val:]
    traindf = traindays.sort_values(['district_id', 'Time']).reset_index(drop=True)
    testdf = testdays.sort_values(['district_id', 'Time']).reset_index(drop=True)
    return traindf, testdf


def timeShift(df, lag=1, X=None, y=None):
    if X:
        ldf = df[[col for col in df.columns if col != 'district_id']]
        districts = df['district_id'].shift(lag).drop(range(lag))
        odf = df.drop(['district_id', 'Time'], axis=1)
        for l in range(lag):
            ldf = ldf.shift()
            ldf.columns = [col + '_t-' + str(l + 1) for col in ldf.columns]
            ldf = pd.concat([ldf, odf], axis=1)
        tdf = ldf.drop(range(lag))
        ndf = tdf.drop(odf.columns, axis=1)
        ndf['district_id'] = districts
        return ndf
    if y:
        ldf = df
        for l in range(lag):
            ldf = ldf.shift(-1)
            tdf = ldf.iloc[:-lag]
        return tdf


def getEstimatorDf(train, test=None, lag=None):
    train['Time'] = train['Time'].astype(np.int64).astype(np.float64) / 10e18
    test['Time'] = test['Time'].astype(np.int64).astype(np.float64) / 10e18
    if not lag:
        X_train = train.drop('nullOrders', axis=1)
        y_train = train['nullOrders']
        X_test = test.drop('nullOrders', axis=1)
        y_test = test['nullOrders']
        return X_train, y_train, X_test, y_test
    else:
        X_train = timeShift(train, lag, X=True)
        y_train = timeShift(train['nullOrders'], lag, y=True)
        X_test = timeShift(test, lag, X=True)
        y_test = timeShift(test['nullOrders'], lag, y=True)
        return X_train, y_train, X_test, y_test


def makeArray(df, X=False, y=False):
    if X:
        return df.values
    elif y:
        return df.values.ravel()
    else:
        return df


def wrapper(file_path=None, testDays=None, lag=None, includePoi=False):
    df = load_training_data(file_path)
    feats = makeFeatures(df)
    nonPois = removePois(feats)
    train, test = splitTrainTestDays(nonPois, testDays)
    X_train, y_train, X_test, y_test = getEstimatorDf(train, test, lag)
    if includePoi:
        poicols = [col for col in feats.columns if col.startswith('poi')]
        poicols.append('district_id')
        X_train = addPois(X_train, feats[poicols])
        X_test = addPois(X_test, feats[poicols])
    X_train = makeArray(X_train, X=True)
    y_train = makeArray(y_train, y=True)
    X_test = makeArray(X_test, X=True)
    y_test = makeArray(y_test, y=True)
    return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    X_train, y_train, X_test, y_test = wrapper(file_path='./features/trainData.csv',
                                               testDays=2, lag=2, includePoi=False)

    print 'X_train' + '-' * 10 + ' shape = {}'.format(X_train.shape)
    print X_train[-1]
    print 'y_train' + '-' * 10 + ' shape = {}'.format(y_train.shape)
    print y_train[-1]
    print 'X_test' + '-' * 10 + ' shape = {}'.format(X_test.shape)
    print X_test[-1]
    print 'y_test' + '-' * 10 + ' shape = {}'.format(y_test.shape)
    print y_test[-1]
