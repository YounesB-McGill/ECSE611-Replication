import json
import csv
import pandas as pd
import math


def intake_data_frame(filename):
	with open(filename) as file:
		data = json.load(file)

	df = pd.DataFrame(data["commits"])
	return df

def get_file_list(df, list_of_files):

	for index, row in df.iterrows():
		for file in row["files"]:
			if(file.endswith(".pp")):
				if file not in list_of_files:
					list_of_files[file] = [row["cmtr"]]
				else:
					list_of_files[file].append(row["cmtr"])

	return(list_of_files)

def compute_ownership_metrics(file):
	list_of_authors = {}
	for author in file:
		if author in list_of_authors:
			list_of_authors[author] += 1
		else:
			list_of_authors[author] = 1

	contributers = len(list_of_authors)
	top_contrib = 0
	number_for_major = math.ceil(.05*len(file))
	number_of_major = 0
	number_of_minor = 0

	for author in list_of_authors:
		if list_of_authors[author] > top_contrib:
			top_contrib = list_of_authors[author]
		if list_of_authors[author] >= number_for_major:
			number_of_major+=1
		else:
			number_of_minor+=1
	
	top_contrib = top_contrib/len(file)

	return(contributers, top_contrib, number_of_major, number_of_minor)

def create_ownership_list(filename):
	path = filename.replace('data/repo_commits/','')
	df = intake_data_frame(filename)

	list_of_files = {}

	get_file_list(df, list_of_files)

	ownership_metric_list = []

	for key in list_of_files:
		contributers, top_contrib, number_of_major, number_of_minor = compute_ownership_metrics(list_of_files[key])
		owner_tuple = [path,key,contributers, top_contrib, number_of_major, number_of_minor]
		ownership_metric_list.append(owner_tuple)

	print(ownership_metric_list)
	return(ownership_metric_list)


ownership_list = create_ownership_list("data/repo_commits/Mirantis_fuel-plugin-celebrer.json")

with open('test_output.csv', 'w') as out_file:
	wr = csv.writer(out_file, delimiter="\n")
	wr.writerow(ownership_list)



