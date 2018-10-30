import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import os
from glob import glob
import pandas as pd
from datetime import datetime
import re
import math

PASS = 'PASS'
MISSING = 'MISSING'
DUPLICATE = 'DUPLICATE'
EMPTY = 'EMPTY'
WARNING = 'WARNING'
USER_HEADERS = ['ADID', 'FIRST NAME', 'LAST NAME', 'FULL NAME', 'EMAIL ADDRESS', 'SUPERVISOR ADID', 'ECRM ROLE 1', 'ECRM ROLE 2', 'GROUP', 'DIVISION', 'TEAM', 'COMPANY']
REQUIRED_USER_HEADERS = ['ADID', 'SUPERVISOR ADID', 'ECRM ROLE 1']
TEAM_NAME = ['GROUP','DIVISION','TEAM','COMPANY']
UNIQUE_HEADERS = ['ADID', 'EMAIL ADDRESS', 'FULL NAME']

application_window = tk.Tk()
application_window.withdraw() #hides the root window
application_window.lift()

initial_dir = os.getcwd()

import_report_df = pd.DataFrame(columns=(PASS, MISSING, DUPLICATE, EMPTY, WARNING))

def check_users():
	files = get_files()
	import_report_df[PASS] = pd.Series(files)
	files_to_data_frame(files)
	df_to_csv(import_report_df)
	

def get_files():
	directory = filedialog.askdirectory(parent=application_window,
										initialdir=os.getcwd(),
										title="Please select a folder")
	files = [file for file in glob(os.path.join(directory, '*.csv'))]
	return files

def reload_import_report_df(errors):
	global import_report_df
	import_report_df = pd.concat([pd.Series(errors[i]) for i in errors], keys=(PASS,MISSING,DUPLICATE,EMPTY,WARNING), axis=1)

def reload_statuses():
	global import_report_df
	status = {
		PASS: [],
		MISSING: [],
		DUPLICATE: [],
		EMPTY: [],
		WARNING: []
	}
	for i in status:
		status[i] = import_report_df[i].dropna().tolist()
	return status

def df_to_csv(data_frame):	
	current_date = datetime.today().strftime('%Y%m%d')
	output_file = "{}_import_results.csv".format(current_date)
	data_frame.to_csv(output_file, sep=',', encoding='utf-8', index=False)

def files_to_data_frame(files):
	for file in files:
		csv_data_frame = pd.read_csv(file, encoding="ISO-8859-1")
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
	status = reload_statuses()
	i = 0
	while i < len(USER_HEADERS)-1: #check if headers match the template
		if USER_HEADERS[i] not in headers:	
			status[MISSING].append("HEADER: {}: {}".format(USER_HEADERS[i], file))
			if file in status[PASS]:
				status[PASS].remove(file)
		i+=1
	reload_import_report_df(status)

def check_duplicate_headers(headers, file):
	global import_report_df
	status = reload_statuses()
	duplicate_headers = {}
	tuple_header_index = [i for i in enumerate(headers)] #creats a tuple of (column index, header name)
	for column, header in tuple_header_index:		
		if re.search('(\.\d+)$', header): #searches for [header_name].X, where X is a number and it indicates it is a duplicate header
			my_header = re.sub('(\.\d+)$','', header)
			index = str(column+1).zfill(2) #pads single digits numbers with 0 to become two-digits (1 -> 01)
			duplicate_headers[index] = my_header	
	for index in duplicate_headers:
		status[DUPLICATE].append("HEADER: COLUMN {} ({}): {}".format(index, duplicate_headers[index], file))
		if file in status[PASS]:
			status[PASS].remove(file)
	reload_import_report_df(status)

def check_users_data(headers, csv_data_frame, file):
	check_missing_data(headers, csv_data_frame, file)
	check_duplicate_data(headers, csv_data_frame, file)

def check_missing_data(headers, csv_data_frame, file):
	global TEAM_NAME
	required_cols = []
	team_cols = []
	data_column = []
	last_row = csv_data_frame.index[-1]+1
	status = reload_statuses()


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
			status[MISSING].append("TEAM NAME: Row {}: {}".format(index, file))
			if file in status[PASS]:
				status[PASS].remove(file)
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
				status[EMPTY].append("{}: Row {}: {}".format(header, index, file))
				if file in status[PASS]:
					status[PASS].remove(file)
			i += 1
	reload_import_report_df(status)

def check_duplicate_data(headers, csv_data_frame, file):
	global UNIQUE_HEADERS
	unique_cols = []
	status = reload_statuses()
	for unique_header in UNIQUE_HEADERS:
		try:
			unique_cols.append((headers.index(unique_header), unique_header))
		except ValueError:
			continue

	for column, header in unique_cols:
		data_column = [str(data).upper() for data in csv_data_frame.iloc[:,column].values.tolist()] #gets all values of column <index>
		for data in data_column:
			if (data_column.count(str(data).upper()) > 1) and any(data in s for s in status[DUPLICATE]) == False:
				status[DUPLICATE].append("{}: {}: {}".format(header, data, file))
				if file in status[PASS]:
					status[PASS].remove(file)
	reload_import_report_df(status)


if __name__ == "__check_users__": #allows to run only when called from another file, not during import
	check_users()