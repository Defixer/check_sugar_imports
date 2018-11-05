import pandas as pd
from pandas.compat import StringIO
import utilities
from datetime import datetime

CONTACT_ROLES = 'CONTACT_ROLES'

import_report_df = pd.DataFrame()

def check_contact_roles(this_import_report_df, files):
	global import_report_df
	import_report_df = this_import_report_df
	file = files[0]
	current_date = datetime.today().strftime('%Y%m%d')	
	csv_data_frame = pd.read_csv(file, encoding="ISO-8859-1", low_memory=False)	
	csv_data_frame = remove_empty_columns(csv_data_frame)
	headers = [line for line in csv_data_frame]
	headers = remove_carriage_return(headers)
	headers = trim_spaces(headers)	
	csv_data_frame.columns = headers
	output_file = "{}_UPDATED_{}.csv".format(file.rsplit('.',1)[0], current_date)
	utilities.df_to_csv(csv_data_frame,output_file)
	return import_report_df

def remove_empty_columns(csv_data_frame):	
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	my_csv_data_frame = csv_data_frame.dropna(how='all', axis=1)
	status[CONTACT_ROLES].append("REMOVED EMPTY COLUMNS")
	import_report_df = utilities.reload_df(status)
	return my_csv_data_frame

def remove_carriage_return(items):
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	my_items = [item.replace('\r','') for item in items]
	status[CONTACT_ROLES].append("REMOVED CARRIAGE RETURN")
	import_report_df = utilities.reload_df(status)
	return my_items

def trim_spaces(items):
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	my_items = [item.strip() for item in items]
	status[CONTACT_ROLES].append("TRIMMED SPACES")
	import_report_df = utilities.reload_df(status)
	return my_items

if __name__ == "__check_contact_roles__": #allows to run only when called from another file, not during import
	check_contact_roles(this_import_report_df, files)