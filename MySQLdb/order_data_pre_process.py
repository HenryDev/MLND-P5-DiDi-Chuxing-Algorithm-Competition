# coding: utf-8
"""
Requirements:
    pandas
    sqlalchemy
    mysql
    di_di db in mysql
    user and passsword with access to di_di db in mysql


Script:
    Loads data from files into pandas,
    Merges the data with the clusters information,
    creates and loads data into mysql table in chunks of 10000 for persistence
"""


import pandas as pd
from sqlalchemy import create_engine

#Create a connection with the db.
engine = create_engine("mysql+mysqldb://user:password@localhost/di_di?unix_socket=/var/run/mysqld/mysqld.sock")
con = engine.connect()


#Generate file location string to access all files iteratively.
file_loc = "../season_1/training_data/order_data/order_data_2016-01-"

#Iteratively create the list of files.
fs = []
for i in range(1,22):
    if i < 10:
        fs.append(''.join([file_loc,'0',str(i)]))
    else:
        fs.append(''.join([file_loc,str(i)]))

#location string of the cluster map file.
f2 = "../season_1/training_data/cluster_map/cluster_map"

#column map for files and table.
f1_cols = ['order_id','driver_id','passenger_id','start_district_hash',
           'dest_district_hash','Price','Time']
f2_cols = ['start_district_hash','start_dist_no']


# Read order_info file, load into pandas, merge with custer_map and load into
# database table order_info.

for i in fs:
    df_order_info = pd.read_table(i,header=None,names=f1_cols,parse_dates=[-1])
    df_dist_info = pd.read_table(f2,header=None,names=f2_cols)
    df=pd.merge(df_order_info,df_dist_info,how='inner',on='start_district_hash',
             left_index=False,right_index=False,sort=False,copy=True)
    df.to_sql('order_info',con=con,flavor='mysql',if_exists='append',
              index=False,chunksize=10000)
