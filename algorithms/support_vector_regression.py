from sklearn import svm
from data_preprocessing.get_x_y_from_features import prediction_matching_data_split
from utilities.measures import calculate_mape


def train_predict():
    svr = svm.SVR()
    svr.fit(x_train, y_train)
    return svr.predict(x_test)


# default SVR implementation
x_train, x_test, y_train, y_test = prediction_matching_data_split()
predictions = train_predict()
print calculate_mape(y_test, predictions)
