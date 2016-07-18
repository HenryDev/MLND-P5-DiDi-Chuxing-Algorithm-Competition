import pandas as pd
from sqlalchemy import create_engine

#Create a connection with the db.
engine = \
create_engine("mysql+mysqldb://bharat:bharat@localhost/di_di?unix_socket=/var/run/mysqld/mysqld.sock")
con = engine.connect()

#location string of the cluster map file.
file_loc = "../season_1/training_data/traffic_data/traffic_data_2016-01-"

fs = []
for i in range(1,22):
    if i<10:
        fs.append(''.join([file_loc,'0',str(i)]))
    else:
        fs.append(''.join([file_loc,str(i)]))

f_cols = ['district_hash','traffic_level_1','traffic_level_2',
          'traffic_level_3','traffic_level_4','Time']

def boogie(level):
    try:
        level = int(level.split(":")[1])
        return level
    except:
        return level

for f in fs:
    df_traffic_info = pd.read_table(f,header=None,names=f_cols,parse_dates=[-1])
    df_traffic_info[['traffic_level_1','traffic_level_2',
                     'traffic_level_3','traffic_level_4']] =\
    df_traffic_info[['traffic_level_1','traffic_level_2',
                    'traffic_level_3','traffic_level_4']].applymap(boogie)
    df_traffic_info.to_sql('traffic_info',con=con,flavor='mysql',if_exists='append',
                           index=False,chunksize=10000)