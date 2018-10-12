import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import os
from glob import glob
import pandas

application_window = tk.Tk()
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
	'HEADER PASS' : [],
	'HEADER_MISSING' : []
}

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
	header_status['HEADER PASS'] = files
	return files

def read_file_data(files):
	for file in files:
		csv_file = pandas.read_csv(file, encoding="ISO-8859-1")
		do_checks(csv_file, file)

def do_checks(csv_file, file):
	check_headers(csv_file, file)

def check_headers(csv_file, file):
	headers = [line.upper() for line in csv_file]

	i = 0
	while i < len(user_headers)-1:
		if user_headers[i] not in headers:	
			header_status['HEADER_MISSING'].append("{}: {}".format(user_headers[i], file))
			header_status['HEADER PASS'].remove(file)
		i+=1	

def check_users_data():
	required_cols = []
	
def read_dict(this_dict):
	for status in this_dict:
		this_status = this_dict[status]
		for element in this_status:
			print("{}: {}".format(status, element))

check_users()