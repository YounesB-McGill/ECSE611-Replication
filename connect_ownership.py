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
	better_file = '/' + file
	for i in range(0, len(orig_file)):
		if repo in orig_file[i][1]:
			if orig_file[i][1].endswith(better_file):
				return i
	return 0



filename = "data/ownership_data_files/mirantis_output.csv"
df = pd.read_csv(filename, encoding='utf-8', sep=',')

file = open("data/IST_MIR.csv", 'r')
data = list(csv.reader(file))

total_found = 0
total_double_found = 0

for index, row in df.iterrows():
	project, repo, file = get_important_info(row)
	result = find_file_in_csv(project, repo, file, data)
	if result != 0:
		total_found+=1
		data[result].append(row["contributers"])
		data[result].append(row["top"])
		data[result].append(row["major"])
		data[result].append(row["minor"])

data[0].append("contributers")
data[0].append("top")
data[0].append("major")
data[0].append("minor")
out_df = pd.DataFrame(data, columns = data[0])
fixed_out_df = out_df.drop(index=0, axis = 0)
fixed_out_df.to_csv('data/ownership_data_files/IST_MIR_OWN.csv', index = False)
print(total_found)
print(total_double_found)