import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.utils import check_array


def getMapeScore(y_true, y_pred):
    y_true = np.nan_to_num(y_true)
    y_pred = np.nan_to_num(y_pred)
    y_true = check_array(y_true)
    y_pred = check_array(y_pred)
    idx = np.nonzero(y_true)
    y_true, y_pred = y_true[idx], y_pred[idx]
    return np.mean(np.abs((y_true - y_pred) / y_true))


def getMaeScore(y_true, y_pred):
    y_true = np.nan_to_num(y_true)
    y_pred = np.nan_to_num(y_pred)
    y_true = check_array(y_true)
    y_pred = check_array(y_pred)
    idx = np.nonzero(y_true)
    y_true, y_pred = y_true[idx], y_pred[idx]
    return mean_absolute_error(y_true, y_pred)


def getMseScore(y_true, y_pred):
    y_true = np.nan_to_num(y_true)
    y_pred = np.nan_to_num(y_pred)
    y_true = check_array(y_true)
    y_pred = check_array(y_pred)
    idx = np.nonzero(y_true)
    y_true, y_pred = y_true[idx], y_pred[idx]
    return mean_squared_error(y_true, y_pred)


def calculate_mape(gaps, predictions):
    ape = 0.
    for gap, prediction in zip(gaps, predictions):
        if gap > 0:
            gap = float(gap)
            prediction = float(prediction)
            ape += abs((gap - prediction) / gap)
    ape /= 43
    return ape / 66
