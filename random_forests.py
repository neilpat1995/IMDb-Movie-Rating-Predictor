from __future__ import print_function
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import csv

INPUT_CSV_FILE = 'processed_data.csv'
NUM_FEATURES = 21
RATING_COLUMN_INDEX = 20
TESTING_SET_PERCENTAGE = 1

'''
Load training and testing data into numpy arrays
'''
with open(INPUT_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data)

movies_X = np.empty([num_rows, NUM_FEATURES-1])
movies_Y = np.empty([num_rows, 1])

with open(INPUT_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
			continue
		# if (index == 10):
		# 	break
		features = [float(row[i]) for i in range(NUM_FEATURES) if i != RATING_COLUMN_INDEX]
		label = float(row[RATING_COLUMN_INDEX])
		
		#Append to features and labels arrays
		movies_X[index] = features
		movies_Y[index] = label

		# print "movies_X[" + str(index) + "] = "
		# for i in range(NUM_FEATURES - 1):
		# 	print movies_X[index][i]
		# print "movies_Y[" + str(index) + "] = " + str(movies_Y[index][0])

training_set_size = int(((100- TESTING_SET_PERCENTAGE) / 100.0) * num_rows)

movies_X_train = movies_X[0:training_set_size, :]
#print "X_train len: " + str(len(movies_X_train))
movies_X_test = movies_X[training_set_size:, :]
#print "X_test len: " + str(len(movies_X_test))

movies_Y = np.ravel(movies_Y) #Convert column vector to expected 1D array  

movies_Y_train = movies_Y[0:training_set_size]
#print "Y_train len: " + str(len(movies_Y_train)) 
movies_Y_test = movies_Y[training_set_size:]
#print "Y_test len: " + str(len(movies_Y_test))

#Create and train classifier
rf_float_regressor = RandomForestRegressor(n_estimators=20, min_samples_split=5)
rf_float_regressor.fit(movies_X_train, movies_Y_train)

print('===== RESULTS WITH FLOATING-POINT LABELS =====')

#Get prediction accuracy
float_preds = rf_float_regressor.score(movies_X_test, movies_Y_test)	# ideally 1.0
print('Predictions with floating point labels: %.3f' % float_preds)

# Re-run model with integer labels
movies_Y_train = [int(round(label)) for label in movies_Y_train]
movies_Y_test = [int(round(label)) for label in movies_Y_test]

# Create new model
rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)

# Train new model
rf_int_classifier.fit(movies_X_train, movies_Y_train)

print('===== RESULTS WITH ROUNDED INTEGER LABELS =====')

#Get prediction accuracy
int_preds = rf_int_classifier.score(movies_X_test, movies_Y_test)
print('Predictions with integer labels: %.3f' % int_preds)