import os
import pandas as pd
import csv

def intake_file(filename):
	df = pd.read_csv(filename, encoding='utf-8', sep=',')
	new_df = df.filter(["org", "file_", "contributers", "top", "major", "minor", "defect_status"])
	return new_df

INPUT_FILES = ["data/ownership_data_files/IST_MIR_OWN.csv", "data/ownership_data_files/IST_MOZ_OWN.csv", "data/ownership_data_files/IST_OST_OWN.csv", "data/ownership_data_files/IST_WIK_OWN.csv"]

for file in INPUT_FILES:
	print("file: ", file)
	df = intake_file(file)
	new_filename = file.replace(".csv", "_ONLY.csv")
	print(new_filename)
	df.to_csv(new_filename, index = False)