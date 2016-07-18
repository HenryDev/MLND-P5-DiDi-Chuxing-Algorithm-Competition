import pandas
from utilities.file_names import getAllFiles
from utilities.file_reader import read_cluster_file, read_prediction_file


def make_result_file(gaps):
    ids_and_time_slots = format_district_ids_time_slots()
    content = {
        'a': ids_and_time_slots[ids_and_time_slots.columns[0]],
        'b': ids_and_time_slots[ids_and_time_slots.columns[1]],
        'c': gaps
    }
    pandas.DataFrame(content).to_csv('results.csv', index=False, header=False)


def format_district_ids_time_slots():
    test_file_names = getAllFiles(test=True)
    district_file = read_cluster_file(test_file_names[1]['cluster']['test_cluster_data_01'])
    district_ids = district_file[district_file.columns[1]]
    time_slots = read_prediction_file(test_file_names[1]['prediction']['test_prediction_data_01'])

    ids_and_time_slots = pandas.DataFrame(index=pandas.MultiIndex.from_arrays(
            pandas.tools.util.cartesian_product([district_ids, time_slots]),
            names=['district IDs', 'time slots'])).reset_index()
    return ids_and_time_slots
