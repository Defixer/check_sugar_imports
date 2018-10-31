import pandas as pd
from datetime import datetime
from check_users_files import check_users
import utilities

def main():
	current_date = datetime.today().strftime('%Y%m%d')
	output_file = "{}_import_results.csv".format(current_date)

	import_report_df = check_users()
	# import_report_df = check_contact_roles(import_report_df)
	utilities.df_to_csv(utilities.import_report_df, output_file)

main()