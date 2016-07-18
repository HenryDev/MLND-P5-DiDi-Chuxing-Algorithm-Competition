from sklearn import metrics, tree, grid_search
import pylab
import numpy

from data_preprocessing.get_x_y_from_features import prediction_matching_data_split
from utilities.measures import calculate_mape


# default implementation for initial model
def train_predict():
    dtr = tree.DecisionTreeRegressor()
    dtr.fit(x_train, y_train)
    return dtr.predict(x_test)


# show learning curve graph
def learning_curve_graph(sizes, training_error, test_error):
    pylab.title('Decision Trees: Performance vs Training Size')
    pylab.plot(sizes, test_error, label='test error')
    pylab.plot(sizes, training_error, label='training error')
    pylab.legend()
    pylab.xlabel('Training Size')
    pylab.ylabel('Error')
    pylab.show()


# shows the learning curve graph for each depth
def learning_curves(max_depths):
    lin_space = numpy.linspace(1, len(x_train))
    sizes = []
    for i in range(len(lin_space)):
        sizes.append(numpy.rint(lin_space[i]).astype(int))
    training_error = numpy.zeros(len(sizes))
    test_error = numpy.zeros(len(sizes))

    for max_depth in max_depths:
        for i, s in enumerate(sizes):
            dtr = tree.DecisionTreeRegressor(max_depth=max_depth)
            dtr.fit(x_train[:s], y_train[:s])
            training_error[i] = metrics.mean_absolute_error(y_train[:s], dtr.predict(x_train[:s]))
            test_error[i] = metrics.mean_absolute_error(y_test, dtr.predict(x_test))
        learning_curve_graph(sizes, training_error, test_error)


# use grid search to find the best depth
def find_best_depth(max_depths):
    scorer = metrics.make_scorer(calculate_mape, greater_is_better=False)
    model = grid_search.GridSearchCV(tree.DecisionTreeRegressor(), {'max_depth': max_depths}, scorer, n_jobs=-1, cv=30)
    model.fit(x_train, y_train)
    return {'prediction': model.predict(x_test), 'best_depth': model.best_params_['max_depth']}


# split data into 75/25 percent sizes
x_train, x_test, y_train, y_test = prediction_matching_data_split()
# use grid search to get prediction results
gs_result = find_best_depth([d for d in range(10, 30)])
print 'best depth', gs_result['best_depth']
predictions = gs_result['prediction']
# use MAPE calculator to find the model performance
print 'MAPE: ', calculate_mape(y_test, predictions)
