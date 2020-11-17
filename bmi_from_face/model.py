import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from utility import get_face_encoding


def model_eval(model, X_test, y_test, predictor_log=True):
    # Make predictions using the testing set
    y_pred = model.predict(X_test)
    y_true = y_test
    if predictor_log:
        y_true = np.log(y_test)
    # The coefficients
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(y_true, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_true, y_pred))

    errors = abs(y_pred - y_true)
    mape = 100 * np.mean(errors / y_true)
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f}'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))


def train_height_model(X_train, y_height_train, X_test, y_height_test):
    model_height = RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100)
    model_height = model_height.fit(X_train, np.log(y_height_train))

    print(model_eval(model_height, X_test, y_height_test))
    return model_height


def train_weight_model(X_train, y_weight_train, X_test, y_weight_test):
    model_weight = RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100)
    model_weight = model_weight.fit(X_train, np.log(y_weight_train))

    print(model_eval(model_weight, X_test, y_weight_test))
    return model_weight


def train_bmi_model(X_train, y_bmi_train, X_test, y_bmi_test):
    model_bmi = RandomForestRegressor(max_depth=2, random_state=0,
                                      n_estimators=100)
    model_bmi = model_bmi.fit(X_train, np.log(y_bmi_train))

    print(model_eval(model_bmi, X_test, y_bmi_test))
    return model_bmi


def predict_bmi(prediction_image, model):
    pred_array = np.expand_dims(np.array(get_face_encoding(prediction_image)),axis=0)
    img = np.exp(model.predict(pred_array))
    bmi = img.item()
    return {'bmi': bmi}


def train_test_splits(X, height, weight, bmi):
    X_train, X_test, y_height_train, y_height_test, y_weight_train, y_weight_test, y_bmi_train, y_bmi_test = \
        train_test_split(X, height, weight, bmi, random_state=1)
    return X_train, X_test, y_height_train, y_height_test, y_weight_train, y_weight_test, y_bmi_train, y_bmi_test


