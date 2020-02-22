import json
import pandas as pd


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
	for author in list_of_authors:
		if list_of_authors[author] > top_contrib:
			top_contrib = list_of_authors[author]
	top_contrib = top_contrib/len(file)
	print(contributers, top_contrib)

	



df = intake_data_frame("data/repo_commits/Mirantis_fuel-plugin-celebrer.json")

list_of_files = {}

print(get_file_list(df, list_of_files))

for key in list_of_files:
	print(key)
	compute_ownership_metrics(list_of_files[key])
