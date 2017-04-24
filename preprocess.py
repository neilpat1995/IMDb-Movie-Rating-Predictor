import csv

NUM_CATEGORIAL_FEATURES = 21	#TOTAL number of columns, including score label
TRAIN_INPUT_CSV_FILE = 'training-movies-raw.csv'
TRAIN_OUTPUT_CSV_FILE = 'training-movies.csv'
TEST_INPUT_CSV_FILE = 'upcoming-movies-test-raw.csv'
TEST_OUTPUT_CSV_FILE = 'upcoming-movies-test.csv'
PREDICT_INPUT_CSV_FILE = 'upcoming-movies-predict-raw.csv'
PREDICT_OUTPUT_CSV_FILE = 'upcoming-movies-predict.csv'

MOVIE_TITLE_INDEX = 9
MOVIE_LINK_INDEX = 14

feature_index_vector = [0] * NUM_CATEGORIAL_FEATURES
feature_dict_vector = [{} for index in range(NUM_CATEGORIAL_FEATURES)]

'''
Helper function to test if a string represents a number 
'''
def is_number(s):
    try:
    	int(s)
    	return True
    except ValueError:
    	pass

    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

	return False

'''
Convert movie datum (row from input file) to a well-formed datum, i.e. convert categorical data to numerical data
Note: Movie name and IMDb link are preserved for display on web application.
'''

def vectorize(csv_row, output_writer):
	numerical_row = [] # Well-formed datum to return
	for feature_index in range(NUM_CATEGORIAL_FEATURES):
		csv_row[feature_index].strip().lower()
		if (is_number(csv_row[feature_index]) or feature_index in {MOVIE_TITLE_INDEX, MOVIE_LINK_INDEX}):
			numerical_row.append(csv_row[feature_index])
		
		else:
			# Categorical data found -> check if the dictionary currently contains it
			#print csv_row[feature_index]
			#print feature_dict_vector[feature_index]
			#print 'feature index is: ' + str(feature_index)
			if csv_row[feature_index] in feature_dict_vector[feature_index]:
				numerical_row.append(feature_dict_vector[feature_index][csv_row[feature_index]]) # Use current mapping value

			else:
				# Dictionary does not contain this value -> add it
				mapped_val = feature_index_vector[feature_index]	#Fetch the current mapping value
				feature_index_vector[feature_index] += 1 	#Increment mapping value for next row

				feature_dict_vector[feature_index][csv_row[feature_index]] = mapped_val # Add new entry to this feature's dict

				numerical_row.append(mapped_val)

	output_writer.writerow(numerical_row) # Write cleaned datum to output file

'''
Driver that creates CSV writer objects and calls vectorize()
'''
with open(TRAIN_INPUT_CSV_FILE, 'rb') as data_file:
	data_reader = csv.reader(data_file)
	output_file = open(TRAIN_OUTPUT_CSV_FILE, "wb")
	output_writer = csv.writer(output_file)
	first_row_raw = next(data_reader)
	first_row_clean = [feature for feature in first_row_raw]
	output_writer.writerow(first_row_clean)	# Write header row to output file

	row_i = 1

	for row in data_reader:
		print 'TRAINING row = ' + str(row_i)
		vectorize(row, output_writer)
		row_i += 1
	output_file.close()

with open(TEST_INPUT_CSV_FILE, 'rb') as test_input_file:
	test_data_reader = csv.reader(test_input_file)
	test_output_file = open(TEST_OUTPUT_CSV_FILE, "wb")
	test_output_writer = csv.writer(test_output_file)
	first_row_raw = next(test_data_reader)
	first_row_clean = [feature for feature in first_row_raw]
	test_output_writer.writerow(first_row_clean)	# Write header row to output file

	row_i = 1

	for row in test_data_reader:
		print 'TESTING row = ' + str(row_i)
		vectorize(row, test_output_writer)
		row_i += 1
	test_output_file.close()

with open(PREDICT_INPUT_CSV_FILE, 'rb') as predict_input_file:
	predict_data_reader = csv.reader(predict_input_file)
	predict_output_file = open(PREDICT_OUTPUT_CSV_FILE, "wb")
	predict_output_writer = csv.writer(predict_output_file)
	first_row_raw = next(predict_data_reader)
	first_row_clean = [feature for feature in first_row_raw]
	predict_output_writer.writerow(first_row_clean)	# Write header row to output file

	row_i = 1

	for row in predict_data_reader:
		print 'PREDICTING row = ' + str(row_i)
		vectorize(row, predict_output_writer)
		row_i += 1
	predict_output_file.close()