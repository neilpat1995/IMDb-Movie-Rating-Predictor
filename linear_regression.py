from __future__ import print_function
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import csv

INPUT_CSV_FILE = 'processed_data.csv'
NUM_FEATURES = 28
RATING_COLUMN_INDEX = 25
TESTING_SET_PERCENTAGE = 25

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

movies_Y_train = movies_Y[0:training_set_size]
#print "Y_train len: " + str(len(movies_Y_train)) 
movies_Y_test = movies_Y[training_set_size:]
#print "Y_test len: " + str(len(movies_Y_test))

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

# predicted_labels = regr_model.predict(movies_X_test)
# print('predicted_labels:')
# for i in range(25):
# 	print(predicted_labels[i])

# Re-run logistic regression model with integer labels
movies_Y_train = [int(round(label)) for label in movies_Y_train]
movies_Y_test = [int(round(label)) for label in movies_Y_test]

# Create new model
regr_model_int_labels = linear_model.LinearRegression()

# Train new model
regr_model_int_labels.fit(movies_X_train, movies_Y_train)

print('===== RESULTS WITH ROUNDED INTEGER LABELS =====')
# The coefficients
print('Coefficients: \n', regr_model_int_labels.coef_)
# The mean squared error
print("Mean squared error: %.3f"
      % np.mean((regr_model_int_labels.predict(movies_X_test) - movies_Y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.3f' % regr_model_int_labels.score(movies_X_test, movies_Y_test))

# predicted_labels = regr_model_int_labels.predict(movies_X_test)
# print('predicted_labels:')
# for i in range(25):
# 	print(predicted_labels[i])


# Plot outputs
# plt.scatter(movies_X_test, movies_Y_test,  color='black')
# plt.plot(movies_X_test, regr_model.predict(movies_X_test), color='blue',
#          linewidth=3)

# plt.xticks(())
# plt.yticks(())

# plt.show()