import pandas as pd
import utilities

PASS = 'PASS'
MISSING = 'MISSING'
RM_NUMBER = 'RM NUMBER'
TAGGING = 'TAGGING'
DO_NOT_TAGGING = 'DO_NOT_TAGGING'
DO_NOT_HEADERS = [RM_NUMBER, TAGGING]

import_report_df = pd.DataFrame()

def check_do_not_flags(this_import_report_df, files):
	global import_report_df
	file = files[0]
	filename = files[0].rsplit('/', 1)[1]
	import_report_df = this_import_report_df
	status = utilities.reload_statuses(import_report_df)
	status[PASS].append(filename)
	import_report_df = utilities.reload_df(status)
	csv_data_frame = pd.read_csv(file, encoding="ISO-8859-1", low_memory=False)	
	headers = [line for line in csv_data_frame]
	check_missing_data(headers, csv_data_frame, file)
	list_unique_values(headers, csv_data_frame, file)
	return import_report_df

def check_missing_data(headers, csv_data_frame, filename):
	global import_report_df
	rm_numbers = csv_data_frame['RM NUMBER'].values.tolist()
	status = utilities.reload_statuses(import_report_df)
	
	tuple_header_index = [i for i in enumerate(headers)] #creats a tuple of (column index, header name)
	for column, header in tuple_header_index:
		i = 0
		current_column = csv_data_frame[header].values.tolist()
		for data in current_column:
			if str(data) == 'nan':
				index = i + 2
				status[MISSING].append("{}: Row {}: {}".format(header.upper(), index, filename))

				if filename in status[PASS]:
					status[PASS].remove(filename)
			i += 1

	import_report_df = utilities.reload_df(status)

def list_unique_values(headers, csv_data_frame, filename):	
	# uniques = csv_data_frame.Tagging.unique() #get all unique values of the column, in this example, 'Tagging' column
	# tuple_value_counter = []
	# for unique in uniques:
	# 	print(unique)
	# 	print(csv_data_frame[unique].value_counts())
		# tuple_value_counter.append((unique, csv_data_frame[unique].value_counts()))
	# print(tuple_value_counter)
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	do_not_df = csv_data_frame.groupby('Tagging').count().applymap(str) #counts all unique values of 'Tagging' column and converts all values to str 
	do_not_df_count = do_not_df.iloc[:,0].values.tolist()
	do_not_df_index = do_not_df.index.values.tolist()
	tuple_do_not = list(zip(do_not_df_index, do_not_df_count))
	for index, count in tuple_do_not:
		status[DO_NOT_TAGGING].append("{}: {}".format(index, count))
	import_report_df = utilities.reload_df(status)


if __name__ == "__check_do_not_flags__": #allows to run only when called from another file, not during import
	check_do_not_flags(this_import_report_df, files)