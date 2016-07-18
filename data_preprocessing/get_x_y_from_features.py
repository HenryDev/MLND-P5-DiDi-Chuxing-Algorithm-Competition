import pandas
from sklearn import cross_validation

from data_preprocessing.time_slot_converter import datetimes_to_time_slots, get_day_from_time_stamp, \
    datetime_to_time_slot, get_day_and_slot_from_time_slot
from utilities.file_reader import read_feature_file
from utilities.result_file_generator import format_district_ids_time_slots


def prepare_data(file_path, feature_columns):
    data = read_feature_file('../' + file_path)
    data = data.dropna(subset=['nullOrders'])
    time_df = pandas.DataFrame(data['Time'])
    data['Time'] = datetimes_to_time_slots(time_df)
    x = data[feature_columns]
    y = data['nullOrders']
    return x, y


def split_data(input_file, feature_columns):
    x, y = prepare_data(input_file, feature_columns)
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y)
    return x_train, x_test, y_train, y_test


def prediction_matching_data_split():
    training_data = pandas.read_csv('../data_preprocessing/features/trainData.csv')
    test_data = pandas.read_csv('../data_preprocessing/features/testData.csv')
    all_the_data = pandas.concat([training_data, test_data])

    # use only time, null orders, and district ID columns that have data in them
    transitioning_df = all_the_data[['Time', 'nullOrders', 'district_id']].dropna()
    # get the day of the month from the timestamp
    transitioning_df['day of month'] = transitioning_df['Time'].apply(get_day_from_time_stamp)
    # get the time of the day from the timestamp
    transitioning_df['time of day'] = transitioning_df['Time'].apply(datetime_to_time_slot)

    # the original timestamp column is no longer needed
    prediction_matching_df = transitioning_df.drop('Time', 1)
    x = prediction_matching_df[['district_id', 'day of month', 'time of day']]
    y = prediction_matching_df['nullOrders']
    # 75/25 data split
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y)
    return x_train, x_test, y_train, y_test


def get_y_from_prediction():
    ids_and_time_slots = format_district_ids_time_slots()
    time_slots = ids_and_time_slots['time slots']
    days_slots = time_slots.apply(get_day_and_slot_from_time_slot)

    days_slots_df = pandas.DataFrame(days_slots.tolist(), columns=['day of month', 'time of day'])
    days_slots_df['district IDs'] = ids_and_time_slots['district IDs']
    days_slots_df = days_slots_df[['district IDs', 'day of month', 'time of day']]
    return days_slots_df
