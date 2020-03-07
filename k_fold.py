from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
import statistics
from numpy import array
import random
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import classifiers
import numpy as np
from sklearn.metrics import mean_absolute_error

precision_results_cart = []
recall_results_cart = []
f_score_results_cart = []
auc_results_cart = []

precision_results_knn = []
recall_results_knn = []
f_score_results_knn = []
auc_results_knn = []

precision_results_lr = []
recall_results_lr = []
f_score_results_lr = []
auc_results_lr = []

precision_results_nb = []
recall_results_nb = []
f_score_results_nb = []
auc_results_nb = []

precision_results_rf = []
recall_results_rf = []
f_score_results_rf = []
auc_results_rf = []

# performs precision on input data. should intake list of choices made by the model as well as the correct result
def perform_precision(model_choice, actual_result):
	true_positives = 0
	false_positives = 0
	for i in range(0, len(model_choice)):
		if model_choice[i] == 1:
			if actual_result[i] == 1:
				true_positives+=1
			else:
				false_positives+=1
	if (false_positives+true_positives == 0):
		precision = 0
	else:
		precision = true_positives/(false_positives+true_positives)
	return precision

# performs recall on input data. should intake list of choices made by the model as well as the correct result
def perform_recall(model_choice, actual_result):
	true_positives = 0
	false_negatives = 0
	for i in range(0, len(model_choice)):
		if model_choice[i] == 1:
			if actual_result[i] == 1:
				true_positives+=1
		else:
			if actual_result[i] == 1:
				false_negatives+=1
	if (true_positives+false_negatives == 0):
		recall = 0
	else:
		recall = true_positives/(true_positives+false_negatives)
	return recall

# f-score of the model, should take in the precision and recall values found prior
def perform_f_score(precision_value, recall_value):
	if (precision_value+recall_value == 0):
		f_score = 0
	else:
		f_score = 2*((precision_value*recall_value)/(precision_value+recall_value))
	return f_score

# performs auc on input data. should intake list of choices made by the model as well as the correct result
def perform_AUC(model_choice, actual_result):
	try:
		auc_result = roc_auc_score(actual_result, model_choice)
	except ValueError:
		auc_result = 0
	return auc_result

def calculate_metrics(prediction, actual, classifier):
	pres_value = perform_precision(prediction, actual)
	rec_value = perform_recall(prediction, actual)
	f_score_value = perform_f_score(pres_value, rec_value)
	auc_value = perform_AUC(prediction, actual)

	if classifier == "cart":
		precision_results_cart.append(pres_value)
		recall_results_cart.append(rec_value)
		f_score_results_cart.append(f_score_value)
		auc_results_cart.append(auc_value)

	if classifier == "knn":
		precision_results_knn.append(pres_value)
		recall_results_knn.append(rec_value)
		f_score_results_knn.append(f_score_value)
		auc_results_knn.append(auc_value)

	if classifier == "lr":
		precision_results_lr.append(pres_value)
		recall_results_lr.append(rec_value)
		f_score_results_lr.append(f_score_value)
		auc_results_lr.append(auc_value)

	if classifier == "nb":
		precision_results_nb.append(pres_value)
		recall_results_nb.append(rec_value)
		f_score_results_nb.append(f_score_value)
		auc_results_nb.append(auc_value)

	if classifier == "rf":
		precision_results_rf.append(pres_value)
		recall_results_rf.append(rec_value)
		f_score_results_rf.append(f_score_value)
		auc_results_rf.append(auc_value)

def calculate_mean_metrics(precision_results, recall_results, f_score_results, auc_results):
	precision = statistics.median(precision_results)
	recall = statistics.median(recall_results)
	f_score = statistics.median(f_score_results)
	auc = statistics.median(auc_results)
	return precision, recall, f_score, auc

def save_results(precision, recall, f_score, auc, system, classifier):
	output = "results.csv"
	with open(output, "a+") as f:
		f.write("%s;%s;%s;%s;%s;%s\n" % (system, classifier, "{0:.2f}".format(precision), r"{0:.2f}".format(recall), "{0:.2f}".format(f_score), round(auc,2)))

# should split the data into ten folds and then call all of the tests to rate the performance of the model in several different ways
# currently does not return the results but that can be added easily
def perform_cross_validation_split(data, num_splits, filename):
	y = data['defect_status']
	del data["defect_status"]		# removing defect answer for training
	X = data.to_numpy() 	 		# remove defects
	
	# performing cross-validation
	kf = KFold(n_splits = num_splits)

	for train, test in kf.split(X):
		X_train, X_test = X[train], X[test]
		y_train, y_test = y[train], y[test]
		actual = y_test.tolist()

		# Classification and Regression Tree (CART) 
		prediction = classifiers.cart(X_train, y_train, X_test)
		calculate_metrics(prediction, actual, "cart")

		# KNearestNeighbor(KNN)
		prediction = classifiers.knn(X_train, y_train, X_test)
		calculate_metrics(prediction, actual, "knn")

		# Logistic Regression (LR)
		prediction = classifiers.logistic_regression(X_train, y_train, X_test)
		calculate_metrics(prediction, actual, "lr")

		# Naive Bayes (NB)
		prediction = classifiers.naive_bayes(X_train, y_train, X_test)
		calculate_metrics(prediction, actual, "nb")

		# Random Forest (RF)
		prediction = classifiers.random_forest(X_train, y_train, X_test)
		calculate_metrics(prediction, actual, "rf")
	
	print("\nCalculate mean metrics...")
	#filename = filename.split("IST_")[1].split(".csv")[0]
	filename = filename.split("PM_")[1].split(".csv")[0]

	precision, recall, f_score, auc = calculate_mean_metrics(precision_results_cart, recall_results_cart, f_score_results_cart, auc_results_cart)
	save_results(precision, recall, f_score, auc, filename, "CART")

	precision, recall, f_score, auc = calculate_mean_metrics(precision_results_knn, recall_results_knn, f_score_results_knn, auc_results_knn)
	save_results(precision, recall, f_score, auc, filename, "KNN")

	precision, recall, f_score, auc = calculate_mean_metrics(precision_results_lr, recall_results_lr, f_score_results_lr, auc_results_lr)
	save_results(precision, recall, f_score, auc, filename, "LR")

	precision, recall, f_score, auc = calculate_mean_metrics(precision_results_nb, recall_results_nb, f_score_results_nb, auc_results_nb)
	save_results(precision, recall, f_score, auc, filename, "NB")

	precision, recall, f_score, auc = calculate_mean_metrics(precision_results_rf, recall_results_rf, f_score_results_rf, auc_results_rf)
	save_results(precision, recall, f_score, auc, filename, "RF")

# intakes the file of the given name and returns it as a data frame
def intake_file(filename):
	df = pd.read_csv(filename, encoding='utf-8', sep=',')
	# Deleting columns not useful for the model
	del df["org"]
	del df["file_"]
	return df

if __name__ == '__main__':
	#INPUT_FILES = ["data/IST_MIR.csv", "data/IST_MOZ.csv", "data/IST_OST.csv", "data/IST_WIK.csv"]
	INPUT_FILES = ["data/filtered_process_metrics_csv/PM_MIR.csv", "data/filtered_process_metrics_csv/PM_MOZ.csv",
	               "data/filtered_process_metrics_csv/PM_OST.csv", "data/filtered_process_metrics_csv/PM_WIK.csv"]

	for file in INPUT_FILES:
		print("file: ", file)
		df = intake_file(file)
		precision_results_cart = []

		recall_results_cart = []
		f_score_results_cart = []
		auc_results_cart = []

		precision_results_knn = []
		recall_results_knn = []
		f_score_results_knn = []
		auc_results_knn = []

		precision_results_lr = []
		recall_results_lr = []
		f_score_results_lr = []
		auc_results_lr = []

		precision_results_nb = []
		recall_results_nb = []
		f_score_results_nb = []
		auc_results_nb = []

		precision_results_rf = []
		recall_results_rf = []
		f_score_results_rf = []
		auc_results_rf = []

		perform_cross_validation_split(df, 10, file)