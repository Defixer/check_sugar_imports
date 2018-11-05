import pandas as pd
import re
import math
import utilities

PASS = 'PASS'
MISSING = 'MISSING'
DUPLICATE = 'DUPLICATE'
EMPTY = 'EMPTY'
CONTACT_ROLES = 'CONTACT ROLES'
USER_HEADERS = ['ADID', 'FIRST NAME', 'LAST NAME', 'FULL NAME', 'EMAIL ADDRESS', 'SUPERVISOR ADID', 'ECRM ROLE 1', 'ECRM ROLE 2', 'GROUP', 'DIVISION', 'TEAM', 'COMPANY']
REQUIRED_USER_HEADERS = ['ADID', 'SUPERVISOR ADID', 'ECRM ROLE 1']
TEAM_NAME = ['GROUP','DIVISION','TEAM','COMPANY']
UNIQUE_HEADERS = ['ADID', 'EMAIL ADDRESS', 'FULL NAME']

import_report_df = utilities.import_report_df

def check_users(files):
	global import_report_df
	filenames = [file.rsplit('/', 1)[1] for file in files]	
	import_report_df[PASS] = pd.Series(filenames)
	files_to_data_frame(files)
	return import_report_df	

def files_to_data_frame(files):
	for file in files:
		csv_data_frame = pd.read_csv(file, encoding="ISO-8859-1", low_memory=False)
		do_checks(csv_data_frame, file)

def do_checks(csv_data_frame, file):
	headers = [line.upper() for line in csv_data_frame]
	check_headers(headers, file)
	check_users_data(headers, csv_data_frame, file)

def check_headers(headers, file):
	check_missing_headers(headers, file)
	check_duplicate_headers(headers, file)

def check_missing_headers(headers, file):	
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	i = 0
	while i < len(USER_HEADERS)-1: #check if headers match the template
		if USER_HEADERS[i] not in headers:	
			filename = file.rsplit('/', 1)[1]
			status[MISSING].append("HEADER: {}: {}".format(USER_HEADERS[i], filename))
			if filename in status[PASS]:
				status[PASS].remove(filename)
		i+=1
	import_report_df = utilities.reload_df(status)

def check_duplicate_headers(headers, file):
	global import_report_df
	status = utilities.reload_statuses(import_report_df)
	duplicate_headers = {}
	tuple_header_index = [i for i in enumerate(headers)] #creats a tuple of (column index, header name)
	for column, header in tuple_header_index:		
		if re.search('(\.\d+)$', header): #searches for [header_name].X, where X is a number and it indicates it is a duplicate header
			my_header = re.sub('(\.\d+)$','', header)
			index = str(column+1).zfill(2) #pads single digits numbers with 0 to become two-digits (1 -> 01)
			duplicate_headers[index] = my_header	
	for index in duplicate_headers:
		filename = file.rsplit('/', 1)[1]
		status[DUPLICATE].append("HEADER: COLUMN {} ({}): {}".format(index, duplicate_headers[index], filename))
		if file in status[PASS]:
			status[PASS].remove(file)
	import_report_df = utilities.reload_df(status)

def check_users_data(headers, csv_data_frame, file):
	check_missing_data(headers, csv_data_frame, file)
	check_duplicate_data(headers, csv_data_frame, file)

def check_missing_data(headers, csv_data_frame, file):
	global import_report_df
	global TEAM_NAME
	required_cols = []
	team_cols = []
	data_column = []
	last_row = csv_data_frame.index[-1]+1
	status = utilities.reload_statuses(import_report_df)


	for name in TEAM_NAME: #get column index of group, division, team, company
		try:
			team_cols.append(headers.index(name))		
		except ValueError:
			continue
	i = 1
	while last_row >= i: 
		if i > 0:
			current_team = csv_data_frame.iloc[i-1:i,team_cols].values.tolist()[0] #gets a row slice from the dataframe			
		else:
			current_team = csv_data_frame.iloc[:i,team_cols].values.tolist()[0] #gets a row slice from the dataframe		
		i += 1
		j = 0
		for name in current_team:
			if type(name) == float:
				j += 1
			else:
				break
		if j == len(team_cols): #checks if all of the columns that composes the team name is empty
			index = str(i).zfill(2)
			filename = file.rsplit('/', 1)[1]
			status[MISSING].append("TEAM NAME: Row {}: {}".format(index, filename))
			if filename in status[PASS]:
				status[PASS].remove(filename)
	for required_user_header in REQUIRED_USER_HEADERS:
		try:
			required_cols.append((headers.index(required_user_header), required_user_header))
		except ValueError:
			continue
	for index, header in required_cols: #gets all empty values row index
		i = 2
		data_column = csv_data_frame.iloc[:,index].values.tolist() #gets all values of column <index>
		for data in data_column:
			if type(data)==float and math.isnan(data):
				index = str(i).zfill(2)
				filename = file.rsplit('/', 1)[1]				
				status[EMPTY].append("{}: Row {}: {}".format(header, index, filename))
				if filename in status[PASS]:
					status[PASS].remove(filename)
			i += 1
	import_report_df = utilities.reload_df(status)

def check_duplicate_data(headers, csv_data_frame, file):
	global import_report_df
	global UNIQUE_HEADERS
	unique_cols = []
	status = utilities.reload_statuses(import_report_df)
	for unique_header in UNIQUE_HEADERS:
		try:
			unique_cols.append((headers.index(unique_header), unique_header))
		except ValueError:
			continue

	for column, header in unique_cols:
		data_column = [str(data).upper() for data in csv_data_frame.iloc[:,column].values.tolist()] #gets all values of column <index>
		for data in data_column:
			if (data_column.count(str(data).upper()) > 1) and any(data in s for s in status[DUPLICATE]) == False: #gets the number of occurence for possible duplicate
				filename = file.rsplit('/', 1)[1]
				status[DUPLICATE].append("{}: {}: {}".format(header, data, filename))
				if filename in status[PASS]:
					status[PASS].remove(filename)
	import_report_df = utilities.reload_df(status)

if __name__ == "__check_users__": #allows to run only when called from another file, not during import
	check_users(files)