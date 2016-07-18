from sklearn.ensemble import RandomForestRegressor

from data_preprocessing import makePredictData as md
from utilities import measures as me
from utilities.file_names import all_training_data


def main():
    clf = RandomForestRegressor(n_jobs=-1)
    X_train, y_train, X_test, y_test = md.wrapper('../' + all_training_data, testDays=2, lag=2)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    preds = preds.reshape(1, preds.shape[0])
    y_test = y_test.reshape(1, y_test.shape[0])
    maeScore = me.getMaeScore(y_test, preds)
    mapeScore = me.getMapeScore(y_test, preds)
    mseScore = me.getMseScore(y_test, preds)
    print "MAPE Score = {}".format(mapeScore)
    print "MAE Score = {}".format(maeScore)
    print "MSE Score = {}".format(mseScore)


if __name__ == '__main__':
    main()
