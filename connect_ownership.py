import os
import pandas as pd

def get_important_info(line):
	project = ''
	repo = ''
	if "Mirantis" in line["Path"]:
		project = "Mirantis"
		repo = line["Path"].replace("Mirantis_", "")
	elif "openstack" in line["Path"]:
		project = "openstack"
		repo = line["Path"].replace("openstack_", "")
	elif "mozilla" in line["Path"]:
		project = "mozilla"
	elif "wikimedia" in line["Path"]:
		project = "wikimedia"
	return project, repo, line["File"]

def find_file_in_csv(project, repo, file, orig_df):
	for line in orig_df["file_"]:
		if repo in line:
			if file in line:
				return 1
	return 0



filename = "data/ownership_data_files/mirantis_output.csv"
df = pd.read_csv(filename, encoding='utf-8', sep=',')

filename = "data/IST_MIR.csv"
orig_df = pd.read_csv(filename, encoding='utf-8', sep=',')

total_found = 0

for index, row in df.iterrows():
	project, repo, file = get_important_info(row)
	print(project, repo, file)
	result = find_file_in_csv(project, repo, file, orig_df)
	total_found+= result

print(total_found)