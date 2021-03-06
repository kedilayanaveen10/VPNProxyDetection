# -*- coding: utf-8 -*-
""" 
    The program when run, detects the use of anonymizing services in a test dataset
    
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""VPNDetection_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18hGXpmYJ8wONEhs8M1D0D34le1iKdRBT
"""

#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split #for splitting dataset into train and test data
from sklearn.preprocessing import StandardScaler #for scaling the dataset
from sklearn.neighbors import KNeighborsClassifier #KNN classifier
from sklearn.metrics import accuracy_score #to find accuracy of model
from sklearn.tree import DecisionTreeClassifier #Decision Tree Classifier
from sklearn.neural_network import MLPClassifier #MLP Classifier
from sklearn.metrics import f1_score #to find F1 score of model

#load datasets
vpnData = pd.read_csv('vpnDataset.csv')
testData = pd.read_csv('NormalCapture.csv')

#drop irrelevant columns
drop_cols = ['Version', 'Protocol', 'SrcAddress', 'DestAddress']

vpnData = vpnData.drop(drop_cols,1)
testData = testData.drop(drop_cols,1)

#Drop duplicates in training dataset
vpnData = vpnData.drop_duplicates()

X = vpnData.iloc[:,:-1]
y = vpnData.iloc[:,-1]

X_testSet = testData.iloc[:,:]

#Using One Hot encoding to encode string data to numerical data
oneHotFeatures = ['Flag','Service']

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)
    return(res) 

frames = [X, X_testSet]
temp = pd.concat(frames)

for feature in oneHotFeatures:
    temp = encode_and_bind(temp, feature)

X = temp.iloc[0:len(X),:]
X_testSet = temp.iloc[-len(X_testSet):,:]

#split data into train and test set
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

#Scaling the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_testSet = scaler.transform(X_testSet)

#KNN - Classifier
knn = KNeighborsClassifier(n_neighbors=15,metric='minkowski',p=2)
knn.fit(X_train,y_train)
y_pred = knn.predict(X_test)
y_predTest = knn.predict(X_testSet)

print('\n------------------------')
print('KNN-Classifier')

print("Accuracy of model on training dataset: ", accuracy_score(y_test,y_pred))

print("Probability that VPN was used: ", (sum(y_predTest)/len(y_predTest)))

#Decision Tree Classifier
DTC = DecisionTreeClassifier(random_state=0)
model = DTC.fit(X_train,y_train)
y_pred = model.predict(X_test)
y_predTest = model.predict(X_testSet)

print('\n------------------------')
print('Decision Tree Classifier')

print("Accuracy of model on training dataset: ", accuracy_score(y_test,y_pred))

print("Probability that VPN was used: ", (sum(y_predTest)/len(y_predTest)))

#MLP Classifier
clf = MLPClassifier(max_iter=1500,random_state=1)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
y_predTest = clf.predict(X_testSet)

print('\n------------------------')
print('MLP Classifier')

print("Model F1 score: ", f1_score(y_test,y_pred))

print("Probability that VPN was used: ", (sum(y_predTest)/len(y_predTest)))

