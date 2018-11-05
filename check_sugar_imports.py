import pandas as pd
from datetime import datetime
from check_users_files import check_users
from check_contact_roles_files import check_contact_roles
import utilities
import os

import itertools
import threading
import time
import sys

USERS = 'USERS'
CONTACT_ROLES = 'CONTACT_ROLES'
# LOADING = ['|', '/', '-', '\\']
LOADING =  ['[=    ]', '[==   ]', '[===  ]', '[ === ]', '[  ===]', '[   ==]', '[    =]']
done = False

def animate():
	global done
	for c in itertools.cycle(LOADING):
		if done:
			break
		sys.stdout.write('\rLOADING ' + c)
		sys.stdout.flush()
		time.sleep(0.3)

def main():
	t = threading.Thread(target=animate)
	t.start()
	
	global done
	current_date = datetime.today().strftime('%Y%m%d')	
	root_directory = utilities.get_root_dir()
	file_directory = "{}/{}".format(root_directory, USERS)
	files = utilities.get_data(file_directory)
	import_report_df = check_users(files)
	print("\tDONE: Check Users import")	
	file_directory = "{}/{}".format(root_directory, CONTACT_ROLES)
	files = utilities.get_data(file_directory)
	import_report_df = check_contact_roles(import_report_df, files)	
	print("\tDONE: Check Contact Roles import")
	output_file = "{}/{}_import_results.csv".format(root_directory, current_date)	
	utilities.df_to_csv(import_report_df, output_file)
	done = True
	print("IMPORT REPORT: {}".format(output_file))
	os.system("open {}".format(output_file))

main()