from data_preprocessing import dataWrangler as dw
import pandas as pd


def read_weather_file(file_path):
    cols = ['Time', 'Weather', 'Temperature', 'Pollution']
    weather_data = pd.read_table(file_path, header=None,
                                 names=cols, parse_dates=[0])
    return weather_data


def read_order_file(file_path):
    cols = ['order_id', 'driver_id', 'passenger_id', 'start_district_hash',
            'dest_district_hash', 'Price', 'Time']
    return pd.read_table(file_path, header=None,
                         names=cols, parse_dates=[-1])


def read_poi_file(file_path):
    return dw.readPoiData(file_path, fillna=True)


def read_traffic_file(file_path):
    cols = ['district_hash', 'traffic_level_1', 'traffic_level_2',
            'traffic_level_3', 'traffic_level_4', 'Time']
    traffic_cols = ['traffic_level_1', 'traffic_level_2',
                    'traffic_level_3', 'traffic_level_4']
    df_traffic_info = pd.read_table(file_path, header=None, names=cols, parse_dates=[-1])
    df_traffic_info[traffic_cols] = df_traffic_info[traffic_cols].applymap(dw.getTrafficLevels)
    return df_traffic_info


def read_prediction_file(file_path):
    return pd.read_table(file_path, header=None, names=['time slots'], skiprows=1)


def read_cluster_file(file_path):
    cols = ['district_hash', 'district_id']
    return pd.read_table(file_path, header=None, names=cols)


def read_feature_file(file_path):
    return pd.read_csv(file_path)
