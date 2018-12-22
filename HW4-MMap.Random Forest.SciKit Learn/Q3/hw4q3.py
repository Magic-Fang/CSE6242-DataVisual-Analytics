## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect seizure

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the paramater 'shuffle' set to true and the 'random_state' set to 100.
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.3, random_state = random_state)

# XXX


# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
linearReg = LinearRegression().fit(x_train,y_train)
# XXX

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
print("For Linear Regression:")
y_predict_train = linearReg.predict(x_train)
y_predict_train_round = [round(k) for k in y_predict_train]
train_score = accuracy_score(y_train, y_predict_train_round)
print("	Accuracy for training set: " + str(train_score))
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
y_predict_test = linearReg.predict(x_test)
y_predict_test_round = [round(k) for k in y_predict_test]
test_score = accuracy_score(y_test, y_predict_test_round)
print("	Accuracy for testing set:  " + str(test_score))
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX


# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
mlpReg = MLPClassifier().fit(x_train,y_train)
# XXX


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
print("For Multi Layer Perceptron:")
y_predict_train_mlp = mlpReg.predict(x_train)
y_predict_train_mlp_round = [round(k) for k in y_predict_train_mlp]
train_mlp_score = accuracy_score(y_train, y_predict_train_mlp_round)
print("	Accuracy for training set: " + str(train_mlp_score))
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict_test_mlp = mlpReg.predict(x_test)
y_predict_test_mlp_round = [round(k) for k in y_predict_test_mlp]
test_mlp_score = accuracy_score(y_test, y_predict_test_mlp_round)
print("	Accuracy for testing set:  " + str(test_mlp_score))
# XXX





# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
rfReg = RandomForestClassifier().fit(x_train, y_train)
# XXX


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
print("For Random Forest Classifier:")
y_predict_train_rf = rfReg.predict(x_train)
y_predict_train_rf_round = [round(k) for k in y_predict_train_rf]
train_rf_score = accuracy_score(y_train, y_predict_train_rf_round)
print("	(Default) Accuracy for training set: " + str(train_rf_score))
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict_test_rf = rfReg.predict(x_test)
y_predict_test_rf_round = [round(k) for k in y_predict_test_rf]
test_rf_score = accuracy_score(y_test, y_predict_test_rf_round)
print("	(Default) Accuracy for testing set:  " + str(test_rf_score))
# -----------------------------------------------------------------------

rfReg_best = RandomForestClassifier(n_estimators=60, max_depth=50).fit(x_train, y_train)
y_predict_train_rf_best = rfReg_best.predict(x_train)
y_predict_train_rf_round_best = [round(k) for k in y_predict_train_rf_best]
train_rf_score_best = accuracy_score(y_train, y_predict_train_rf_round_best)
print("	(Best) Accuracy for training set: " + str(train_rf_score_best))
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict_test_rf_best = rfReg_best.predict(x_test)
y_predict_test_rf_round_best = [round(k) for k in y_predict_test_rf_best]
test_rf_score_best = accuracy_score(y_test, y_predict_test_rf_round_best)
print("	(Best) Accuracy for testing set:  " + str(test_rf_score_best))
# XXX

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.

parameters_rf = {'n_estimators':[10, 20, 40, 60, 80, 100, 120, 140], 
'max_depth':[6, 8, 10, 30, 50, 75, 100]}
rfReg_tune = RandomForestClassifier()
rlf = GridSearchCV(rfReg_tune, parameters_rf, cv = 10)
rlf.fit(x_train, y_train)

print("	Best paramaters after CV:")
print("	  "+str(rlf.best_params_))
print("	  "+str(rlf.best_score_))

# XXX


# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
x_train_nor = normalize(x_train)
x_test_nor = normalize(x_test)
# TODO: Create a SVC classifier and train it.
rfReg = SVC(gamma = 'auto').fit(x_train_nor, y_train)
# XXX

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
print("For Support Vector Machine:")
y_predict_train_rf = rfReg.predict(x_train_nor)
y_predict_train_rf_round = [round(k) for k in y_predict_train_rf]
train_rf_score = accuracy_score(y_train, y_predict_train_rf_round)
print("	(Default) Accuracy for training set: " + str(train_rf_score))
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict_test_rf = rfReg.predict(x_test_nor)
y_predict_test_rf_round = [round(k) for k in y_predict_test_rf]
test_rf_score = accuracy_score(y_test, y_predict_test_rf_round)
print("	(Default) Accuracy for testing set:  " + str(test_rf_score))
# -----------------------------------------------------------

rfReg_best = SVC(gamma = 'auto', kernel='linear', C=0.001).fit(x_train_nor, y_train)
y_predict_train_rf_best = rfReg_best.predict(x_train_nor)
y_predict_train_rf_round_best = [round(k) for k in y_predict_train_rf_best]
train_rf_score_best = accuracy_score(y_train, y_predict_train_rf_round_best)
print("	(Best) Accuracy for training set: " + str(train_rf_score_best))
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict_test_rf_best = rfReg_best.predict(x_test_nor)
y_predict_test_rf_round_best = [round(k) for k in y_predict_test_rf_best]
test_rf_score_best = accuracy_score(y_test, y_predict_test_rf_round_best)
print("	(Best) Accuracy for testing set:  " + str(test_rf_score_best))
# XXX

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.

parameters_rf = {'kernel':('linear', 'rbf'), 'C':[0.001, 0.01, 0.1, 1, 10, 100]}
rfReg_tune = SVC(gamma = 'auto')
clf = GridSearchCV(rfReg_tune, parameters_rf, cv = 10, return_train_score=True)
clf.fit(x_train_nor, y_train)

print("	Best paramaters after CV:")
print("	  "+str(clf.best_params_))
print("	  "+str(clf.best_score_))

print("mean training score:")
print(clf.cv_results_['mean_train_score'])
print("mean testing score:")
print(clf.cv_results_['mean_test_score'])
print("mean fit time:")
print(clf.cv_results_['mean_fit_time'])

# XXX


