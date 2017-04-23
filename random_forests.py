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

NUM_FEATURES = 21 	#Number of features for each sample, INCLUDING rating label. 
RATING_COLUMN_INDEX = 20

'''
Load training data into numpy arrays.
'''
with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	data = list(data_file_reader)
	num_rows = len(data)

train_movies_X = np.empty([num_rows, NUM_FEATURES-1])
train_movies_Y = np.empty([num_rows, 1])

with open(TRAINING_CSV_FILE, 'rb') as data_file:
	data_file_reader = csv.reader(data_file)
	for index, row in enumerate(data_file_reader):
		if (index == 0):	#Skip header row
			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if i != RATING_COLUMN_INDEX]
		label = float(row[RATING_COLUMN_INDEX])
		
		#Append to training features and labels arrays
		train_movies_X[index] = features
		train_movies_Y[index] = label

# movies_X_train = movies_X[0:training_set_size, :]
# #print "X_train len: " + str(len(movies_X_train))
# movies_X_test = movies_X[training_set_size:, :]
# #print "X_test len: " + str(len(movies_X_test))

'''
Load testing dataset in numpy arrays.
'''
with open(TESTING_CSV_FILE, 'rb') as test_file:
	test_data_reader = csv.reader(test_file)
	test_data = list(test_data_reader)
	num_test_samples = len(test_data)

test_movies_X = np.empty([num_test_samples, NUM_FEATURES-1])
test_movies_Y = np.empty([num_test_samples, 1])

with open(TESTING_CSV_FILE, 'rb') as test_file:
	test_data_reader = csv.reader(test_file)
	for index, row in enumerate(test_data_reader):
		if (index == 0):
			continue
		features = [float(row[i]) for i in range(NUM_FEATURES) if i != RATING_COLUMN_INDEX]
		label = float(row[RATING_COLUMN_INDEX])

		#Append to testing features and labels arrays
		test_movies_X[index] = features
		test_movies_Y[index] = label

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
cv_float_preds = cross_val_score(cv_rf_float_regressor, movies_X, movies_Y, cv=5)
print("Prediction accuracy (cross-validation): %0.2f (+/- %0.2f)" % (cv_float_preds.mean(), cv_float_preds.std() * 2))
'''



print('===== RESULTS WITH ROUNDED INTEGER LABELS =====')
#Compute rounded label values
train_movies_Y = [int(round(label)) for label in train_movies_Y]
test_movies_Y = [int(round(label)) for label in test_movies_Y]

# Create new model (regular and CV classifiers)
rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
#cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)

# Regular model
rf_int_classifier.fit(train_movies_X, train_movies_Y)
int_preds = rf_int_classifier.score(test_movies_X, test_movies_Y)
print('Testing prediction accuracy (no cross-validation): %.3f' % int_preds)

# CV model
# movies_Y = [int(round(label)) for label in movies_Y] # Round entire label set
#cv_int = ShuffleSplit(n_splits=3, test_size=TESTING_SET_DECIMAL, random_state=0)


'''
GridSearchCV implementation
'''
'''
parameters = {'n_estimators':[n for n in range(20,24,5)], 'min_samples_split':[m for m in range(5,6)]}
rf_grid_model = RandomForestClassifier()
rf_best_grid_model = GridSearchCV(rf_grid_model, parameters)
rf_best_grid_model.fit(movies_X_train, movies_Y_train)
print('Prediction accuracy for GridSearchCV optimum model: %.3f' %rf_best_grid_model.score(movies_X_test, movies_Y_test))
'''

'''
#StratifiedShuffleSplit implementation
sss = StratifiedShuffleSplit(n_splits=5, test_size=TESTING_SET_DECIMAL)
movies_X = np.asarray(movies_X)
movies_Y = np.asarray(movies_Y)
for train_index, test_index in sss.split(movies_X, movies_Y):
	X_train, X_test = movies_X[train_index], movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = movies_Y[train_index], movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy: %.3f" %best_score)	
'''

'''
StratifiedKFold implementation
skf = StratifiedKFold(n_splits = 5, shuffle=True)
for train_index, test_index in skf.split(movies_X, movies_Y):
	X_train, X_test = movies_X[train_index], movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = movies_Y[train_index], movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy: %.3f" %best_score)
'''

best_model = None	# Maintain a model and score for the best fold
best_score = 0.0

'''
KFold implementation
'''
'''

kf = KFold(n_splits=2, shuffle=True)
movies_X = np.asarray(movies_X)
movies_Y = np.asarray(movies_Y)
for train_index, test_index in kf.split(movies_X, movies_Y):
	X_train, X_test = movies_X[train_index], movies_X[test_index]	# Get training and testing subsets
	Y_train, Y_test = movies_Y[train_index], movies_Y[test_index]

	cv_rf_int_classifier = RandomForestClassifier(n_estimators=20, min_samples_split=5, n_jobs=3)
	cv_rf_int_classifier.fit(X_train, Y_train)
	cv_int_preds = cv_rf_int_classifier.score(X_test, Y_test)

	if (cv_int_preds > best_score):
		best_model = cv_rf_int_classifier
		best_score = cv_int_preds

print("Best-fitting model accuracy: %.3f" %best_score)


'''
#cv_int_preds = cross_val_score(cv_rf_int_classifier, movies_X, movies_Y, cv=5)

'''

print("Prediction accuracy (cross-validation): %0.2f (+/- %0.2f)" % (cv_int_preds.max(), cv_int_preds.std() * 2))
test_start_index = int(round((1.0 - TESTING_SET_DECIMAL) * num_rows))
print("Test start index: %d" %test_start_index)

print("cv_int_preds length: %d" %len(cv_int_preds))

cv_int_pred_labels = cv_int_preds[-test_start_index:]
print(cv_int_pred_labels.shape)

'''