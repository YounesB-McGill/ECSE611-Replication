import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

# Random Forest (RF)
def random_forest(x_train, y_train, x_test):
	clf = RandomForestClassifier(max_depth=2, random_state=0)
	clf.fit(x_train, y_train)
	predicted = clf.predict(x_test)
	return predicted

# Naive Bayes (NB)
def naive_bayes(x_train, y_train, x_test):
	gnb = GaussianNB()
	gnb.fit(x_train, y_train)
	predicted = gnb.predict(x_test)
	return predicted

# Logistic Regression (LR)
def logistic_regression(x_train, y_train, x_test):
	lr = LogisticRegression(max_iter=400) # 400 is the only value that does not throw a warning
	lr.fit(x_train, y_train)
	predicted = lr.predict(x_test)
	return predicted

# KNearestNeighbor(KNN)
def knn(x_train, y_train, x_test):
	neigh = KNeighborsClassifier(n_neighbors=3)
	neigh.fit(x_train, y_train)
	predicted = neigh.predict(x_test)
	return predicted

# Classification and Regression Tree (CART)
def cart(x_train, y_train, x_test):
	model = DecisionTreeClassifier()
	model.fit(x_train, y_train)
	predicted = model.predict(x_test)
	return predicted