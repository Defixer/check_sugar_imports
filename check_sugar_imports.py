import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import os
from glob import glob
import pandas as pd
import re

PASS = 'PASS'
WARNING = 'WARNING'
ERROR = 'ERROR'
DUPLICATE = 'DUPLICATE'
user_headers = ['ADID', 'FIRST NAME', 'LAST NAME', 'FULL NAME', 'EMAIL ADDRESS', 'SUPERVISOR ADID', 'ECRM ROLE 1', 'ECRM ROLE 2', 'GROUP', 'DIVISION', 'TEAM', 'COMPANY']
required_user_headers = ['ADID', 'SUPERVISOR ADID', 'ECRM ROLE 1', {
							'TEAM_NAME': [
								'GROUP',
								'DIVISION',
								'TEAM',
								'COMPANY'
								]
							}
						]
header_status = {
	PASS: [],
	WARNING: [],
	ERROR: [],
	DUPLICATE: []
}

application_window = tk.Tk()
def check_users():
	files = get_files()
	read_file_data(files)
	read_dict(header_status)

def get_files():
	directory = filedialog.askdirectory(parent=application_window,
										initialdir=os.getcwd(),
										title="Please select a folder")
	os.chdir(directory)
	files = [file for file in glob('*.csv')]
	header_status[PASS] = files
	return files

def read_file_data(files):
	for file in files:
		csv_file = pd.read_csv(file, encoding="ISO-8859-1")
		do_checks(csv_file, file)

def do_checks(csv_file, file):
	headers = [line.upper() for line in csv_file]
	check_headers(headers, file)

def check_headers(headers, file):
	check_complete_headers(headers, file)
	check_duplicate_headers(headers, file)	

def check_complete_headers(headers, file):
	i = 0
	while i < len(user_headers)-1: #check if headers match the template
		if user_headers[i] not in headers:	
			header_status[WARNING].append("MISSING HEADER: {}: {}".format(user_headers[i], file))
			if file in header_status[PASS]:
				header_status[PASS].remove(file)
		i+=1	

def check_duplicate_headers(headers, file):
	duplicate_headers = {}
	indeces = [i for i, header in enumerate(headers) if re.search('(\.\d+)$', header)]
	if len(indeces) <= 0:
		return
	duplicate_headers = {(headers[x],x+1) for x in indeces}
	for header,col in duplicate_headers:
		header_status[DUPLICATE].append("DULPICATE HEADER: COLUMN {} ({}): {}".format(col, header.split('.')[0], file))
	if file in header_status[PASS]:
		header_status[PASS].remove(file)

def check_users_data():
	required_cols = []
	
def read_dict(this_dict):
	for status in this_dict:
		this_status = this_dict[status]
		for element in this_status:
			print("{}: {}".format(status, element))

check_users()