import json
import csv
import pandas as pd
import math
from pathlib import Path


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
	path = path.replace('.json', '')
	df = intake_data_frame(filename)

	list_of_files = {}

	get_file_list(df, list_of_files)

	ownership_metric_list = []

	for key in list_of_files:
		contributers, top_contrib, number_of_major, number_of_minor = compute_ownership_metrics(list_of_files[key])
		owner_tuple = [path,key,contributers, top_contrib, number_of_major, number_of_minor]
		ownership_metric_list.append(owner_tuple)

	return(ownership_metric_list)

def run_through_directory(directory_name, project_name):
	pathlist = Path(directory_name).glob('*')

	mirantis_paths = []
	openstack_paths = []
	mozilla_paths = []
	wiki_paths = []
	for path in pathlist:
		str_path = str(path)
		if str_path.startswith("data/repo_commits/Mirantis"):
			if project_name == 'Mirantis':
				mirantis_paths.append(str(path))
		if str_path.startswith("data/repo_commits/openstack"):
			if project_name == 'openstack':
				openstack_paths.append(str(path))
		if str_path.startswith("data/repo_commits/mozilla"):
			if project_name == 'mozilla':
				mozilla_paths.append(str(path))
		if str_path.startswith("data/repo_commits/wikimedia"):
			if project_name == 'wikimedia':
				wiki_paths.append(str(path))



	total_output = []
	if project_name == "Mirantis":
		for path in mirantis_paths:
			total_output = total_output + create_ownership_list(path)
	elif project_name == "openstack":
		for path in openstack_paths:
			total_output = total_output + create_ownership_list(path)
	elif project_name == "mozilla":
		for path in mozilla_paths:
			total_output = total_output + create_ownership_list(path)
	elif project_name == "wikimedia":
		for path in wiki_paths:
			total_output = total_output + create_ownership_list(path)
	return(total_output)

def perform_all_projects():
	col = ["Path", "File", "contributers", "top", "major","minor"]

	mirantis_ownership_list = run_through_directory("data/repo_commits", "Mirantis")
	df = pd.DataFrame(mirantis_ownership_list, columns=col)
	df.to_csv('data/ownership_data_files/mirantis_output.csv', index = False)

	openstack_ownership_list = run_through_directory("data/repo_commits", "openstack")
	df = pd.DataFrame(openstack_ownership_list, columns=col)
	df.to_csv('data/ownership_data_files/openstack_output.csv', index = False)

	mozilla_ownership_list = run_through_directory("data/repo_commits", "mozilla")
	df = pd.DataFrame(mozilla_ownership_list, columns=col)
	df.to_csv('data/ownership_data_files/mozilla_output.csv', index = False)

	wikimedia_ownership_list = run_through_directory("data/repo_commits", "wikimedia")
	df = pd.DataFrame(wikimedia_ownership_list, columns=col)
	df.to_csv('data/ownership_data_files/wikimedia_output.csv', index = False)

perform_all_projects()




# with open('mirantis_output.csv', 'w') as out_file:
# 	wr = csv.writer(out_file, delimiter="\n")
# 	wr.writerow(ownership_list)


