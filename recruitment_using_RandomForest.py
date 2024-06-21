import pandas as pd

import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('dataset/recruitment_data.csv')

df = df.drop(["Age", "Gender", "DistanceFromCompany"], axis = 1)

x = df.drop("HiringDecision",axis = 1)
y = df["HiringDecision"]

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=10, train_size= .75)

forest = RandomForestClassifier()
forest.fit(x_train, y_train)
prediction = forest.predict(x_test)
print("Random Forest")
print(f'Accuracy: {accuracy_score(y_test, prediction)}')
print(confusion_matrix(y_test, prediction))
print(classification_report(y_test, prediction))

joblib.dump(forest, 'forest_model.joblib')



