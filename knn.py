# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:08:12 2017

Running KNN on Movies Dataset
@author: Sangini
"""

from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier as KNN
import matplotlib.pyplot as plt
import numpy as np
import csv

INPUT_CSV_FILE = 'processed_data.csv'
NUM_FEATURES = 21
RATING_COLUMN_INDEX = 19
TESTING_SET_PERCENTAGE = 25
#NON_INT_FEATURES_INDEX = [0, 4, 7, 8, 9, 11, 13, 14, 15]

'''
Load training and testing data into numpy arrays
'''
with open(INPUT_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data)

#movies_train_features = np.empty([num_rows, NUM_FEATURES-(1+len(NON_INT_FEATURES_INDEX))])
movies_train_features = np.empty([num_rows, NUM_FEATURES-1])
movies_train_labels = np.empty([num_rows, 1])

with open(INPUT_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
			continue
		# if (index == 10):
		# 	break
        #features = [float(row[i]) for i in range(NUM_FEATURES) if (i != RATING_COLUMN_INDEX and not (i in NON_INT_FEATURES_INDEX))]
		features = [float(row[i]) for i in range(NUM_FEATURES) if (i != RATING_COLUMN_INDEX)]
        label = float(row[RATING_COLUMN_INDEX])
		
		#Append to features and labels arrays
        movies_train_features[index] = features
        movies_train_labels[index] = label

		# print "movies_X[" + str(index) + "] = "
		# for i in range(NUM_FEATURES - 1):
		# 	print movies_X[index][i]
		# print "movies_Y[" + str(index) + "] = " + str(movies_Y[index][0])

#Take subsets of the training set to use for testing
#Will adjust this later once actual test data is available
training_set_size = int(((100- TESTING_SET_PERCENTAGE) / 100.0) * num_rows)

movies_features_train = movies_train_features[0:training_set_size, :]
#print ("X_train len: " + str(len(movies_X_train)))
movies_features_test = movies_train_features[training_set_size:, :]
#print ("X_test len: " + str(len(movies_X_test)))

movies_labels_train = movies_train_labels[0:training_set_size]
#print ("Y_train len: " + str(len(movies_Y_train))) 
movies_labels_test = movies_train_labels[training_set_size:]
#print ("Y_test len: " + str(len(movies_Y_test)))

#Run KNN on the data using 3 as the closest neighbors
knn = KNN(n_neighbors = 10, weights='distance')
knn.fit(movies_features_train, movies_labels_train.ravel().astype(int))

output = knn.predict(movies_features_test)

int_test_labels = movies_labels_test.astype(int)
correct = 0.0
for i in range(len(output)): 
    if int_test_labels[i][0] == output[i]: 
        correct += 1
print (correct / len(output))
