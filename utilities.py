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
WARNING = 'WARNING'
CONTACT_ROLES = 'CONTACT ROLES'

import_report_df = pd.DataFrame(columns=(PASS, MISSING, DUPLICATE, EMPTY, WARNING, CONTACT_ROLES))

application_window = tk.Tk()
application_window.withdraw() #hides the root window
application_window.lift() #makes the application window on top

def get_files(concat_dir):
	directory = filedialog.askdirectory(parent=application_window,
										initialdir=os.getcwd(),
										title="Please select a folder")
	directory = "{}/{}".format(directory, concat_dir)
	files = [file for file in glob(os.path.join(directory, '*.csv'))]
	return files

def df_to_csv(data_frame, output_file):
	data_frame.to_csv(output_file, sep=',', encoding='utf-8', index=False)

# if __name__ == "__get_files__": #allows to run only when called from another file, not during import
# 	get_files()