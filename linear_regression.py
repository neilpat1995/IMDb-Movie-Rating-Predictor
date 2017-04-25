from __future__ import print_function
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import csv

TRAINING_CSV_FILE = 'training-movies.csv'
TESTING_CSV_FILE = 'upcoming-movies-test.csv'
PREDICTION_CSV_FILE = 'upcoming-movies-predict.csv'
LOG_REG_PRED_MODEL_PREDICTIONS_FILE = 'upcoming-movies-pred-model-predictions-logistic-regression.csv'
LOG_REG_TEST_MODEL_PREDICTIONS_FILE = 'upcoming-movies-test-model-predictions-logistic-regression.csv'
LIN_REG_PRED_MODEL_PREDICTIONS_FILE = 'upcoming-movies-pred-model-predictions-linear-regression.csv'
LIN_REG_TEST_MODEL_PREDICTIONS_FILE = 'upcoming-movies-test-model-predictions-linear-regression.csv'

NUM_FEATURES = 21
RATING_COLUMN_INDEX = 19
MOVIE_TITLE_INDEX = 9
MOVIE_LINK_INDEX = 14

'''
Load training and testing data into numpy arrays
'''
with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data)

movies_X_train = np.empty([num_rows, NUM_FEATURES-3])
movies_Y_train = np.empty([num_rows, 1])

with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}]
		label = float(row[RATING_COLUMN_INDEX])
		
		#Append to features and labels arrays
		movies_X_train[index] = features
		movies_Y_train[index] = label

with open(TESTING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_test_rows = len(data)-1

movies_X_test = np.empty([num_test_rows, NUM_FEATURES-3])
movies_Y_test = np.empty([num_test_rows, 1])
test_output = [['' for col in range(4)] for sample in range(num_test_rows)]
test_header = []

with open(TESTING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
			test_header = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], row[RATING_COLUMN_INDEX], "rating_actual"]
			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}]
		label = float(row[RATING_COLUMN_INDEX])
		sample_info = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], 0, row[RATING_COLUMN_INDEX]]

		#Append to features and labels arrays
		movies_X_test[index-1] = features
		movies_Y_test[index-1] = label
		test_output[index-1] = sample_info


with open(PREDICTION_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_predict_rows = len(data)-1

movies_X_predict = np.empty([num_predict_rows, NUM_FEATURES-3])
pred_output = [['' for col in range(3)] for sample in range(num_predict_rows)]
pred_header = []

with open(PREDICTION_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):
			pred_header = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], row[RATING_COLUMN_INDEX]]
			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}]
		sample_info = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], 0]

		#Append to features and labels arrays
		movies_X_predict[index-1] = features
		pred_output[index-1] = sample_info

# Create linear regression model
regr_model = linear_model.LinearRegression()

# Train model
regr_model.fit(movies_X_train, movies_Y_train)

print('===== RESULTS WITH FLOATING-POINT LABELS =====')

# The coefficients
print('Coefficients: \n', regr_model.coef_)
# The mean squared error
print("Mean squared error: %.3f"
      % np.mean((regr_model.predict(movies_X_test) - movies_Y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.3f' % regr_model.score(movies_X_test, movies_Y_test))
lin_test_preds = regr_model.predict(movies_X_test)
lin_pred_preds = regr_model.predict(movies_X_predict)

for i in range(len(lin_test_preds)):
	test_output[i][2] = lin_test_preds[i]

for i in range(len(lin_pred_preds)):
	pred_output[i][2] = lin_pred_preds[i]

#Write preds to output files
lin_test_output_file = open(LIN_REG_TEST_MODEL_PREDICTIONS_FILE, "wb")
writer = csv.writer(lin_test_output_file)

writer.writerow(test_header)
for i in range(len(test_output)):
	writer.writerow(test_output[i])

lin_pred_output_file = open(LIN_REG_PRED_MODEL_PREDICTIONS_FILE, "wb")
writer = csv.writer(lin_pred_output_file)

writer.writerow(pred_header)
for i in range(len(pred_output)):
	writer.writerow(pred_output[i])



# Re-run model with integer labels
movies_Y_train = [int(round(label)) for label in movies_Y_train]
movies_Y_test = [int(round(label)) for label in movies_Y_test]

# Create new model (logistic)
log_reg_model = linear_model.LogisticRegression(solver='sag', multi_class='multinomial')

# Train new model
log_reg_model.fit(movies_X_train, movies_Y_train)

print('===== RESULTS WITH ROUNDED INTEGER LABELS =====')
print('%.3f' % log_reg_model.score(movies_X_test, movies_Y_test))
log_test_preds = log_reg_model.predict(movies_X_test)
log_pred_preds = log_reg_model.predict(movies_X_predict)

for i in range(len(log_test_preds)):
	test_output[i][2] = log_test_preds[i]

for i in range(len(log_pred_preds)):
	pred_output[i][2] = log_pred_preds[i]

# Write preds to output files
log_test_output_file = open(LOG_REG_TEST_MODEL_PREDICTIONS_FILE, "wb")
writer = csv.writer(log_test_output_file)

writer.writerow(test_header)
for i in range(len(test_output)):
	writer.writerow(test_output[i])

log_pred_output_file = open(LOG_REG_PRED_MODEL_PREDICTIONS_FILE, "wb")
writer = csv.writer(log_pred_output_file)

writer.writerow(pred_header)
for i in range(len(pred_output)):
	writer.writerow(pred_output[i])