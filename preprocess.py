import csv

NUM_CATEGORIAL_FEATURES = 21	#TOTAL number of columns, including score label
INPUT_CSV_FILE = '15k-dataset-raw.csv'
OUTPUT_CSV_FILE = 'processed_data.csv'

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
'''

def vectorize(csv_row, output_writer):
	numerical_row = [] # Well-formed datum to return	
	for feature_index in range(NUM_CATEGORIAL_FEATURES):
		csv_row[feature_index].strip().lower()
		if is_number(csv_row[feature_index]):
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
with open(INPUT_CSV_FILE, 'rb') as data_file:
	data_reader = csv.reader(data_file)
	output_file = open(OUTPUT_CSV_FILE, "wb")
	output_writer = csv.writer(output_file)
	first_row_raw = next(data_reader)
	# print "First row type: " + str(type(first_row))
	# print "First row contents: "
	# for i in range(len(first_row)):
	# 	print first_row[i]
	first_row_clean = [feature for feature in first_row_raw]

	output_writer.writerow(first_row_clean)	# Write header row immediately to output file

	row_i = 1

	for row in data_reader:
		print 'row_i = ' + str(row_i)
		vectorize(row, output_writer)
		row_i += 1
	output_file.close()
