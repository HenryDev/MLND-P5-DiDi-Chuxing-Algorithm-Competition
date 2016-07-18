import pandas as pd
from glob import glob
import os
def makeData(file_loc,file_name):
    files = glob(file_loc+'feature*')
    df = pd.DataFrame()
    for data in files:
        df = pd.concat([df,pd.read_csv(data,parse_dates=[0])],axis=0)
    df.sort_values(['district_id','Time'],inplace=True)
    df.set_index('Time',inplace=True,drop=True)
    df.to_csv(file_name,encoding='utf-8')
    return None


def rmData(file_name):
    os.remove(file_name)
#
# if __name__=='__main__':
#     file_loc = "./features/"
#     file_name = "allData"
#     makeData(file_loc,file_name)
#     raw_input("Press enter to continue to delete the file")
#     rmData("allData")
