# coding: utf-8

import dataWrangler as dw
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.decomposition import PCA

def getPoiData(**kwargs):
    if 'MySQL' in kwargs:
        try:
            connectors = kwargs.pop('MySQL')
            connect_string =("mysql+mysqldb://"+connectors[0]+":"\
                             +connectors[1]+"@localhost/"+connectors[2]+\
                             "?unix_socket = /var/run/mysqld/mysqld.sock")
            engine = create_engine(connect_string)
            con = engine.connect()
            return pd.read_sql_table("poi_info",con=con)
        except:
            print ("Database connection error,\nrequires"\
                   "\t{'MySQL':['user','password','database']}")
            return None
    elif 'infile' in kwargs:
        try:
            poifile = kwargs.pop('infile')
            rawPoiData = dw.readPoiData(poifile)
            distfile = ("/".join(poifile.split("/")[:-2]
                                 +['cluster_map','cluster_map']))
            dist_info = getDistInfo(infile=distfile)
            return rawPoiData.merge(dist_info,how='left',on='district_hash')
        except:
            print "File read exception, check poi_info file_location string"
            return None
    else:
        print ("Nothing provided as input,\nrequires:"\
               "\n{'MySQL':['user','password','database']} \n"\
               "\t or \n{'infile':'**file_location**'}")

def getDistInfo(**kwargs):
    try:
        distfile = kwargs.pop('infile')
        return pd.read_table(distfile,header=None,
                             names=['district_hash','district_id'])
    except:
        print "File read exception, check district_info file_location string"
        return None

def compressPoiData(poiData,pca):
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
    return pd.DataFrame(pois_pca),var


if __name__=='__main__':
    poiData = getPoiData(infile=('../Didi-Chuxing/season_1/'\
                                 'training_data/poi_data/poi_data')).fillna(0)
    pca = PCA(n_components=1)
    pois,var = compressPoiData(poiData,pca)
