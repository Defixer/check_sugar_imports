import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import os
from glob import glob
from datetime import datetime
import pandas as pd

PASS = 'PASS'
MISSING = 'MISSING'
DUPLICATE = 'DUPLICATE'
EMPTY = 'EMPTY'
CONTACT_ROLES = 'CONTACT_ROLES'
DO_NOT_TAGGING = 'DO_NOT_TAGGING'

import_report_df = pd.DataFrame(columns=(PASS, MISSING, DUPLICATE, EMPTY, CONTACT_ROLES, DO_NOT_TAGGING))

application_window = tk.Tk()
application_window.withdraw() #hides the root window
application_window.lift() #makes the application window on top

def get_data(directory):
	files = [file for file in glob(os.path.join(directory, '*.csv'))]
	return files

def get_root_dir():
	directory = filedialog.askdirectory(parent=application_window,
										initialdir=os.getcwd(),
										title="Please select a folder")
	return directory

def df_to_csv(data_frame, output_file):
	data_frame.to_csv(output_file, sep=',', encoding='utf-8', index=False)

def reload_df(errors):
	import_report_df = pd.concat([pd.Series(errors[i]) for i in errors], 
											keys=(PASS,MISSING,DUPLICATE,EMPTY,CONTACT_ROLES, DO_NOT_TAGGING), axis=1)
	return import_report_df

def reload_statuses(import_report_df):
	status = {
		PASS: [],
		MISSING: [],
		DUPLICATE: [],
		EMPTY: [],
		CONTACT_ROLES: [],
		DO_NOT_TAGGING: []
	}
	for i in status:
		status[i] = import_report_df[i].dropna().tolist()
	return status
# if __name__ == "__get_files__": #allows to run only when called from another file, not during import
# 	get_files()