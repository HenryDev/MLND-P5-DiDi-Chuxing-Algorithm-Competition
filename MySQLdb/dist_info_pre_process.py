import pandas as pd
from sqlalchemy import create_engine

#Create a connection with the db.
engine = \
create_engine("mysql+mysqldb://bharat:bharat@localhost/di_di?unix_socket=/var/run/mysqld/mysqld.sock")
con = engine.connect()

#location string of the cluster map file.
f2 = "../season_1/training_data/cluster_map/cluster_map"

f2_cols = ['district_hash','district_id']

df_dist_info = pd.read_table(f2,header=None,names=f2_cols)

df_dist_info.to_sql('dist_info',con=con,flavor='mysql',if_exists='append',
                        index=False,chunksize=10000)
