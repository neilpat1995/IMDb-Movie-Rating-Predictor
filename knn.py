# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:08:12 2017

Running KNN on Movies Dataset
@author: Sangini
"""

from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.decomposition import PCA
import numpy as np
import csv

TRAINING_CSV_FILE = 'training-movies.csv'
TESTING_CSV_FILE = 'upcoming-movies-test.csv'
PREDICTION_CSV_FILE = 'upcoming-movies-predict.csv'
OUTPUT_CSV_FILE = 'knn-predictions.csv'
TEST_OUTPUT_FILE = 'knn-estimates.csv'

PREDICTION_COLUMN = 'predicted_imdb_score'

NUM_FEATURES = 21
RATING_COLUMN_INDEX = 19
MOVIE_TITLE_INDEX = 9
IMDB_LINK_INDEX = 14

TESTING_SET_PERCENTAGE = 10
#NON_INT_FEATURES_INDEX = [0, 4, 7, 8, 9, 11, 13, 14, 15]

'''
Load training, testing, and prediction data into numpy arrays
'''
with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data) - 1

#movies_train_features = np.empty([num_rows, NUM_FEATURES-(1+len(NON_INT_FEATURES_INDEX))])
movies_train_features = np.empty([num_rows, NUM_FEATURES-3])
movies_train_labels = np.empty([num_rows, 1])

with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
 			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if (i != RATING_COLUMN_INDEX and i != MOVIE_TITLE_INDEX and i != IMDB_LINK_INDEX)]
		label = float(row[RATING_COLUMN_INDEX])
		#print(str(label) + ", " + str(row[RATING_COLUMN_INDEX]))
		  
		#Append to features and labels arrays
		movies_train_features[index-1] = features
		movies_train_labels[index-1] = label

		
with open(TESTING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data) - 1

movies_test_features = np.empty([num_rows, NUM_FEATURES-3])
movies_test_labels = np.empty([num_rows, 1])
test_out_header = []
movies_test_predictions = [['' for x in range(4)] for y in range(num_rows)] 

with open(TESTING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
 			test_out_header = [row[MOVIE_TITLE_INDEX], row[IMDB_LINK_INDEX], PREDICTION_COLUMN, row[RATING_COLUMN_INDEX]]              
 			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if (i != RATING_COLUMN_INDEX and i != MOVIE_TITLE_INDEX and i != IMDB_LINK_INDEX)]
		label = float(row[RATING_COLUMN_INDEX])
		#print(str(label) + ", " + str(row[RATING_COLUMN_INDEX]))
		info = 	[row[MOVIE_TITLE_INDEX], row[IMDB_LINK_INDEX], 0, label]
		#print (info)	
  
		#Append to features and labels arrays
		movies_test_features[index-1] = features
		movies_test_labels[index-1] = label
		movies_test_predictions[index-1] = info



with open(PREDICTION_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data) - 1

movies_predict_features = np.empty([num_rows, NUM_FEATURES-3])
predict_out_header = []
predict_output = [['' for x in range(3)] for y in range(num_rows)] 
                   
with open(PREDICTION_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
 			predict_out_header = [row[MOVIE_TITLE_INDEX], row[IMDB_LINK_INDEX], row[RATING_COLUMN_INDEX]]
 			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if (i != RATING_COLUMN_INDEX and i != MOVIE_TITLE_INDEX and i != IMDB_LINK_INDEX)]
		#print(str(label) + ", " + str(row[RATING_COLUMN_INDEX]))
		info = [row[MOVIE_TITLE_INDEX], row[IMDB_LINK_INDEX], 0]		
		#print (info)
        
		#Append to features array
		movies_predict_features[index-1] = features
		predict_output[index-1] = info
		#print (predict_output[index-1])

#Run PCA on the data to reduce dimentionality
pca = PCA(n_components = 12, whiten = True)
pca.fit(movies_train_features)
movies_train_features = pca.transform(movies_train_features)
movies_test_features = pca.transform(movies_test_features)
movies_predict_features = pca.transform(movies_predict_features)

#Run KNN on the test data and output to CSV
knn = KNN(n_neighbors = 10, weights='distance')
knn.fit(movies_train_features, movies_train_labels.ravel().astype(int))
test_output = knn.predict(movies_test_features)

output_file = open(TEST_OUTPUT_FILE, "wb")
output_writer = csv.writer(output_file)
output_writer.writerow(test_out_header)

int_test_labels = movies_test_labels.astype(int)
correct = 0.0
for i in range(len(test_output)): 
    movies_test_predictions[i][2] = test_output[i]
    #print (movies_test_predictions[i])
    #print (str(int_test_labels[i][0]) + ", " + str(test_output[i]))
    output_writer.writerow(movies_test_predictions[i])
    if int_test_labels[i][0] == test_output[i]: 
        correct += 1
print (correct / len(test_output))
output_file.close()


#Run KNN on the prediction data and output to a CSV file
output_file = open(OUTPUT_CSV_FILE, "wb")
output_writer = csv.writer(output_file)
output_writer.writerow(predict_out_header)
#print(predict_output)
predictions = knn.predict(movies_predict_features)
for i in range(len(predictions)):
    predict_output[i][2] = predictions[i]
    #print (predict_output[i])
    #print (i)
    output_writer.writerow(predict_output[i])
output_file.close()