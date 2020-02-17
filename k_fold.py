from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
import statistics
from numpy import array
import random
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

#only here so that I can call it to test if the 
def run_model_standin(train_data, test_data):
	results = []
	for i in range(0, len(train_data)):
		result = random.random()
		if result > .5:
			results.append(1)
		else:
			results.append(0)
	return results
	

#performs precision on input data. should intake list of choices made by the model as well as the correct result
def perform_precision(model_choice, actual_result):
	true_positives = 0
	false_positives = 0
	for i in range(0, len(model_choice)):
		if model_choice[i] == 1:
			if actual_result[i] == 1:
				true_positives+=1
			else:
				false_positives+=1
	precision = true_positives/(false_positives+true_positives)
	return precision

#performs recall on input data. should intake list of choices made by the model as well as the correct result
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
	recall = true_positives/(true_positives+false_negatives)
	return recall

#f-score of the model, should take in the precision and recall values found prior
def perform_f_score(precision_value, recall_value):
	f_score = 2*((precision_value*recall_value)/(precision_value+recall_value))
	return f_score

#performs auc on input data. should intake list of choices made by the model as well as the correct result
def perform_AUC(model_choice, actual_result):
	auc_result = roc_auc_score(actual_result, model_choice)
	return auc_result

#should split the data into ten folds and then call all of the tests to rate the performance of the model in several different ways
#currently does not return the results but that can be added easily
def perform_cross_validation_split(data, num_splits):
	kf = KFold(n_splits = num_splits)
	

	precision_results = []
	recall_results = []
	f_score_results = []
	auc_results = []

	for train, test in kf.split(data):
		test_data = data.loc[test]
		train_data = data.loc[train]
		test_res = run_model_standin(train_data,test_data)

		actual = train_data['defect_status'].tolist()

		pres_value = perform_precision(test_res, actual)
		precision_results.append(pres_value)

		rec_value = perform_recall(test_res, actual)
		recall_results.append(rec_value)

		f_score_value = perform_f_score(pres_value, rec_value)
		f_score_results.append(f_score_value)

		auc_value = perform_AUC(test_res, actual)
		auc_results.append(auc_value)

	print(auc_results)
	print(statistics.median(auc_results))

#intakes the file of the given name and returns it as a data frame
def intake_file(filename):
	df = pd.read_csv(filename, encoding='utf-8', sep=',')
	return df

df = intake_file("IST_MIR.csv")

perform_cross_validation_split(df, 10)