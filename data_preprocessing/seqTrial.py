# coding: utf-8
import pandas as pd
import numpy as np
from data_preprocessing import makePredictData as mp
from sklearn.tree import DecisionTreeRegressor
from utilities import measures


def getDistrictNulls(orders_df):
    nullsdf = orders_df[['district_id', 'nullOrders']].fillna(0)
    ddf = pd.DataFrame()
    for did in nullsdf['district_id'].unique():
        dnulls = nullsdf[nullsdf['district_id'] == did]['nullOrders']
        dnulls.name = 'district_' + str(int(did))
        ddf = pd.concat([ddf, dnulls], axis=1)
    return ddf


def makeseq(ddf, col, seq=3):
    samples = []
    labels = []
    for i in range(0, len(ddf) - seq):
        samples.append(ddf[col].iloc[i:i + seq].values.ravel())
        labels.append(ddf[col].iloc[i + seq])
    d = pd.DataFrame(np.array(samples))
    d['y'] = labels
    return d


def getSeq(ddf, seq=3):
    sdf = pd.DataFrame()
    districts = np.array([np.ones(len(ddf) - seq) * int(col.split("_")[-1]) for col in ddf.columns]).ravel()
    for col in ddf.columns:
        sdf = pd.concat([sdf, makeseq(ddf, col, seq)])
    sdf['district_id'] = districts
    return sdf.reset_index(drop=True)


def makeTrainTest(allseqdata, days=2):
    traindf = pd.DataFrame()
    testdf = pd.DataFrame()
    slots = days * 144
    for i in allseqdata['district_id'].unique():
        alldist = allseqdata[allseqdata['district_id'] == i]
        traindist = alldist.iloc[:-slots]
        testdist = alldist.iloc[-slots:]
        traindf = pd.concat([traindf, traindist])
        testdf = pd.concat([testdf, traindist])
    traindf.reset_index(inplace=True, drop=True)
    testdf.reset_index(inplace=True, drop=True)
    return traindf, testdf


def makeTrainTestArrays(traindf, testdf=None):
    X_train = traindf.drop(['y'], axis=1).values
    y_train = traindf['y'].values
    if testdf:
        X_test = testdf.drop(['y'], axis=1).values
        y_test = testdf['y'].values
        return X_train, y_train, X_test, y_test
    else:
        return X_train,y_train


def wrapper(fname,cv=None,lag=3):
    orders_df = mp.load_training_data(fname)
    ddf = getDistrictNulls(orders_df)
    allseqdata = getSeq(ddf,seq=lag)
    if not cv:
        return makeTrainTestArrays(allseqdata)
    else:
        traindf, testdf = makeTrainTest(allseqdata, days=1)
        X_train, y_train, X_test, y_test = makeTrainTestArrays(traindf, testdf)
        return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    X_train, y_train = wrapper('./features/trainData.csv',lag=1)
    X_test,y_test = wrapper('./features/testData.csv',lag=1)
    """
    print X_train[:10]
    print
    print y_train[:10]
    print
    print X_test[:10]
    print
    print y_test[:10]
    """
    reg = DecisionTreeRegressor()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    y_pred = y_pred.reshape(1, y_pred.shape[0])
    y_test = y_test.reshape(1, y_test.shape[0])
    score = measures.getMapeScore(y_test, y_pred)
    print "MAPE score = {}".format(score)
    for i,j in zip(y_pred.ravel(),y_test.ravel()):
        print i,j
