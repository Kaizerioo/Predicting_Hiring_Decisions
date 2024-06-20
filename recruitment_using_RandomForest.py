import pandas as pd

import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('dataset/recruitment_data.csv')

df = df.drop(["Age", "Gender", "DistanceFromCompany"], axis = 1)

x = df.drop("HiringDecision",axis = 1)
y = df["HiringDecision"]

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=10, train_size= .75)
x_train = x_train / 255
x_test = x_test / 255

forest = RandomForestClassifier()
forest.fit(x_train, y_train)

joblib.dump(forest, 'forest_model.joblib')



