import pandas as pd
import numpy as np
import csv

import sklearn.ensemble as ek
from sklearn import cross_validation, tree, linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from feature_extractor import predict_feature


def train():
    featureSet = pd.read_csv(r"C:\Users\wei04.TRN\Desktop\ml\PhishingURLDetector\data\train0.csv", index_col=0)
    X = featureSet.drop(['label'], axis=1).sort_index(axis=1).values
    X = np.delete(X, 0, 0)
    y = featureSet['label'].values
    y = np.delete(y, 0, 0)
    model = {"DecisionTree": tree.DecisionTreeClassifier(max_depth=50),
             "RandomForest": ek.RandomForestClassifier(n_estimators=10),
             "Adaboost": ek.AdaBoostClassifier(n_estimators=50),
             "GradientBoosting": ek.GradientBoostingClassifier(n_estimators=50),
             "GNB": GaussianNB(),
             "LogisticRegression": LogisticRegression()
             }
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    results = {}
    for algo in model:
        clf = model[algo]
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        print("%s : %s " % (algo, score))
        results[algo] = score
    model_selected = model['RandomForest']
    return model_selected


def test_one(url):
    featureSet = pd.read_csv(r"C:\Users\wei04.TRN\Desktop\ml\PhishingURLDetector\data\train0.csv", index_col=0)
    featureDummy = pd.DataFrame(columns=featureSet.columns).to_dict('list')
    a = predict_feature(url, featureDummy)
    formal = pd.DataFrame([a])
    formal = formal.drop(['label', 'url'], axis=1).sort_index(axis=1).values

    return train().predict(formal)

def test_many():
    featureSet = pd.read_csv(r"C:\Users\wei04.TRN\Desktop\ml\PhishingURLDetector\data\train0.csv", index_col=0)
    featureDummy = pd.DataFrame(columns=featureSet.columns).to_dict('list')



if __name__ == '__main__':
    print(test_one(url="http://www.google.com"))
