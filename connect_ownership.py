import os
import pandas as pd
import csv

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

def find_file_in_csv(project, repo, file, orig_file):
	for line in orig_file:
		if repo in line[1]:
			if file in line[1]:
				return 1
	return 0



filename = "data/ownership_data_files/mirantis_output.csv"
df = pd.read_csv(filename, encoding='utf-8', sep=',')

file = open("data/IST_MIR.csv", 'r')
data = list(csv.reader(file))

total_found = 0

for index, row in df.iterrows():
	project, repo, file = get_important_info(row)
	result = find_file_in_csv(project, repo, file, data)
	total_found+= result

print(total_found)