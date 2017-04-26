from __future__ import print_function
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold, StratifiedKFold, StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV

# Files holding training, testing (Jan-Mar 2017 movies), and upcoming movie (Apr-Dec 2017) data.
TRAINING_CSV_FILE = 'training-movies.csv'
TESTING_CSV_FILE = 'upcoming-movies-test.csv'
PREDICTION_CSV_FILE = 'upcoming-movies-predict.csv'
MODEL_PREDICTIONS_FILE = 'upcoming-movies-forests-predictions.csv'
MODEL_TEST_PREDICTIONS_FILE = 'upcoming-movies-forests-test-predictions.csv'

MOVIE_TITLE_INDEX = 9
MOVIE_LINK_INDEX = 14

NUM_FEATURES = 21 	#Number of features for each sample, INCLUDING rating label. 
RATING_COLUMN_INDEX = 19

'''
Load training data into numpy arrays.
'''
with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data)

train_movies_X = np.empty([num_rows-1, NUM_FEATURES-3])
train_movies_Y = np.empty([num_rows-1, 1])

# train_csv = np.genfromtxt(TRAINING_CSV_FILE, delimiter=",", dtype=None)
# labels = train_csv[:,RATING_COLUMN_INDEX]
# print("TRAINING LABELS: ")
# for label in np.nditer(labels):
# 	print(label)

with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):	#Skip header row
			continue
		features = [row[i] for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}]
		label = row[RATING_COLUMN_INDEX]

		#Append to training features and labels arrays
		train_movies_X[index-1] = features
		train_movies_Y[index-1] = label

'''
Load testing dataset in numpy arrays.
'''
with open(TESTING_CSV_FILE, 'rb') as test_file:
	test_data_reader = csv.reader(test_file)
	test_data = list(test_data_reader)
	num_test_samples = len(test_data)-1

test_movies_X = np.empty([num_test_samples, NUM_FEATURES-3])
test_movies_Y = np.empty([num_test_samples, 1])
prediction_test_output = [['' for header_feature in range(4)] for prediction in range(num_test_samples)] #Final output to write to CSV
output_test_header = [] # Header for testing data output


with open(TESTING_CSV_FILE, 'rb') as test_file:
	test_data_reader = csv.reader(test_file)
	for index, row in enumerate(test_data_reader):
		if (index == 0):
			output_test_header = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], row[RATING_COLUMN_INDEX], "rating_actual"]
			continue
		features = [row[i] for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_LINK_INDEX, MOVIE_TITLE_INDEX}]
		label = row[RATING_COLUMN_INDEX]
		header_info_test = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], 0, row[RATING_COLUMN_INDEX]]

		#Append to testing features and labels arrays
		test_movies_X[index-1] = features
		test_movies_Y[index-1] = label
		prediction_test_output[index-1] = header_info_test

'''
Load predicting dataset in numpy arrays.
'''
with open(PREDICTION_CSV_FILE, 'rb') as predict_file:
	predict_data_reader = csv.reader(predict_file)
	predict_data = list(predict_data_reader)
	num_predict_samples = len(predict_data)-1

predict_movies_X = np.empty([num_predict_samples, NUM_FEATURES-3])
prediction_output = [['' for header_feature in range(3)] for prediction in range(num_predict_samples)] #Final output to write to CSV

output_header = []

with open(PREDICTION_CSV_FILE, 'rb') as predict_file:
	predict_data_reader = csv.reader(predict_file)
	for index, row in enumerate(predict_data_reader):
		if (index == 0):
			output_header = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], row[RATING_COLUMN_INDEX]]
			continue
		features = [row[i] for i in range(NUM_FEATURES) if i not in {RATING_COLUMN_INDEX, MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}]
		predict_movies_X[index-1] = features
		header_info = [row[MOVIE_TITLE_INDEX], row[MOVIE_LINK_INDEX], 0]
		prediction_output[index-1] = header_info

'''
Prepare writer to write to predictions output file.
Currently writes predictions for non-CV classifier ONLY 
'''
predictions_output_file = open(MODEL_PREDICTIONS_FILE, "wb")
pred_out_writer = csv.writer(predictions_output_file)
test_predictions_output_file = open(MODEL_TEST_PREDICTIONS_FILE, "wb")
test_pred_out_writer = csv.writer(test_predictions_output_file)

# Convert column vectors of labels to expected 1D array 
train_movies_Y = np.ravel(train_movies_Y)  
test_movies_Y = np.ravel(test_movies_Y)

#Create and train classifier
rf_float_regressor = RandomForestRegressor(n_estimators=20, min_samples_split=5)
rf_float_regressor.fit(train_movies_X, train_movies_Y)

print('===== RESULTS WITH FLOATING-POINT LABELS =====')
#Get prediction accuracy
float_preds = rf_float_regressor.score(test_movies_X, test_movies_Y)
print('Testing prediction accuracy (no cross-validation): %.3f' % float_preds)



'''
cv_rf_float_regressor = RandomForestRegressor(n_estimators=20, min_samples_split=5)
cv_float_preds = cross_val_score(cv_rf_float_regressor, train_movies_X, train_movies_Y, cv=5)
print("Prediction accuracy (cross-validation): %0.2f (+/- %0.2f)" % (cv_float_preds.mean(), cv_float_preds.std() * 2))
'''

print('===== RESULTS WITH ROUNDED INTEGER LABELS =====')
#Compute rounded label 


train_movies_Y = [int(round(label)) for label in train_movies_Y]
test_movies_Y = [int(round(label)) for label in test_movies_Y]

# Create new model (regular and CV classifiers)
rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
#cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)

# Regular model
rf_int_classifier.fit(train_movies_X, train_movies_Y)
int_preds = rf_int_classifier.score(test_movies_X, test_movies_Y)
print('Testing prediction accuracy (no cross-validation): %.3f' % int_preds)
int_test_preds = rf_int_classifier.predict(test_movies_X)


pred_out_writer.writerow(output_header)

pred_labels = rf_int_classifier.predict(predict_movies_X)
for i in range(len(pred_labels)):
	prediction_output[i][2] = pred_labels[i]
	pred_out_writer.writerow(prediction_output[i])

# Write to test CSV output file.
test_pred_out_writer.writerow(output_test_header)
for i in range(len(int_test_preds)):
	prediction_test_output[i][2] = int_test_preds[i]
	test_pred_out_writer.writerow(prediction_test_output[i])


# CV model
# movies_Y = [int(round(label)) for label in movies_Y] # Round entire label set
#cv_int = ShuffleSplit(n_splits=3, test_size=TESTING_SET_DECIMAL, random_state=0)


'''
GridSearchCV implementation-> 38.6-39%
'''

'''

parameters = {'n_estimators':[n for n in range(25,46,5)], 'min_samples_split':[m for m in range(3,8) if m != 5]}
rf_grid_model = RandomForestClassifier()
rf_best_grid_model = GridSearchCV(rf_grid_model, parameters)
rf_best_grid_model.fit(train_movies_X, train_movies_Y)
print('Prediction accuracy for GridSearchCV optimum model: %.3f' %rf_best_grid_model.score(test_movies_X, test_movies_Y))

'''

best_model = None	# Maintain a model and score for the best fold
best_score = 0.0
'''
StratifiedShuffleSplit implementation -> 36.9% on testing, 85.6% on validation
train_movies_Y = np.array(train_movies_Y) # Convert movie label sets back to numpy arrays 
test_movies_Y = np.array(test_movies_Y)

sss = StratifiedShuffleSplit(n_splits=5, test_size=num_test_samples-1)
for train_index, test_index in sss.split(train_movies_X, train_movies_Y):
	X_train, X_test = train_movies_X[train_index], train_movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = train_movies_Y[train_index], train_movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy from StratifiedShuffleSplit on validation data: %.3f" %best_score)	
print("Best-fitting model accuracy from StratifiedShuffleSplit on testing data: %.3f" %best_model.score(test_movies_X, test_movies_Y))
'''

'''
StratifiedKFold implementation -> 34.7% on testing, 79.1% on validation
skf = StratifiedKFold(n_splits = 5, shuffle=True)
train_movies_Y = np.array(train_movies_Y) # Convert movie label sets back to numpy arrays 
test_movies_Y = np.array(test_movies_Y)
for train_index, test_index in skf.split(train_movies_X, train_movies_Y):
	X_train, X_test = train_movies_X[train_index], train_movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = train_movies_Y[train_index], train_movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy on validation data from StratifiedKFold: %.3f" %best_score)
print("Best-fitting model accuracy on test data from StratifiedKFold: %.3f" %best_model.score(test_movies_X, test_movies_Y))
'''

'''
KFold implementation -> 34.7% on testing, 83.5% on validation
'''
'''

kf = KFold(n_splits=10, shuffle=True)
train_movies_Y = np.array(train_movies_Y) # Convert movie label sets back to numpy arrays 
test_movies_Y = np.array(test_movies_Y)
for train_index, test_index in kf.split(train_movies_X, train_movies_Y):
	X_train, X_test = train_movies_X[train_index], train_movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = train_movies_Y[train_index], train_movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5, n_jobs=3)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy on validation data from KFold: %.3f" %best_score)
print("Best-fitting model accuracy on testing data from KFold: %.3f" %best_model.score(test_movies_X, test_movies_Y))

'''
'''

# cross_val_score implementation
n_estimators = [est_sample for est_sample in range(20,41,5)]
min_samples_split = [min_split_sample for min_split_sample in range(3,9)]

best_model = None
best_score = 0.0

for n_est in n_estimators:
	for min_sample in min_samples_split:
		cv_rf_int_classifier = RandomForestClassifier(n_estimators=n_est, min_samples_split=min_sample)
		cv_int_preds = cross_val_score(cv_rf_int_classifier, train_movies_X, train_movies_Y, cv=5)
		if (cv_int_preds.mean() > best_score):
			best_model = cv_rf_int_classifier
			best_score = cv_int_preds.mean()

print("Prediction accuracy (CV with cross_val_score using parameter sets): %.2f" %best_model.score(test_movies_X, test_movies_Y))
test_preds = cross_val_score.predict(test_movies_X)
'''

'''

print("Prediction accuracy (cross-validation): %0.2f (+/- %0.2f)" % (cv_int_preds.max(), cv_int_preds.std() * 2))

'''