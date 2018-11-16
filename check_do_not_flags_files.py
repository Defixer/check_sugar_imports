import pandas as pd
import utilities

PASS = 'PASS'
MISSING = 'MISSING'
DO_NOT_HEADERS = ['RM NUMBER', 'TAGGING']

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
	return import_report_df

def check_missing_data(headers, csv_data_frame, file):
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
				filename = file.rsplit('/', 1)[1]
				status[MISSING].append("{}: Row {}: {}".format(header.upper(), index, filename))

				if filename in status[PASS]:
					status[PASS].remove(filename)
			i += 1

	import_report_df = utilities.reload_df(status)

if __name__ == "__check_do_not_flags__": #allows to run only when called from another file, not during import
	check_do_not_flags(this_import_report_df, files)