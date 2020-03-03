from collections import defaultdict
import pandas as pd
import json
import os
import subprocess
import shutil
from shutil import copyfile


INPUT_FILES = ["../data/IST_MIR.csv", "../data/IST_MOZ.csv", "../data/IST_OST.csv", "../data/IST_WIK.csv"]
MINED_DATA_FILES = "../data/repo_commits"
PUPPET_PROJECTS = "../puppet_projects/"
OUTPUT = "../../to_detect_smells/"

PAPER_DATA = defaultdict(list)
MINED_DATA = defaultdict(list)
FILE_BUG_STATUS = {}

def get_ecosystem_name(file):
	if file.startswith("Mirantis"):
		return "MIR"
	elif file.startswith("mozilla"):
		return "MOZ"
	elif file.startswith("openstack"):
		return "OST"
	elif file.startswith("wikimedia"):
		return "WIK"		

def get_mined_data():
	for file in os.listdir(MINED_DATA_FILES):		 # each file is a project
		os.chdir("/Users/isabellaferreira/Dropbox/PhD/Winter2020/ECSE611_SoftwareAnalytics/replication/ECSE611-Replication/smells")
		mined_with_status = defaultdict(list)		 # reset for each project
		ecosystem = get_ecosystem_name(file)
		project = file.split("_")[-1].split(".json")[0]
		full_path = os.path.join(MINED_DATA_FILES, file)

		print("##############################################################################################################################")
		print ("file: ", file)
		print("ecosystem: ", ecosystem)
		print("project: ", project)
		print("\n\n")

		with open(full_path) as json_file:
			data = json.load(json_file)	
			for commit_info in data["commits"]: 				# go over each commit of that project checking for changed files that we have bug status in the oracle
				commit_hash = commit_info["hash"]
				for f in commit_info["files"]:					# files changed in that commit
					file_full_path = project + "/" + f
					if file_full_path in FILE_BUG_STATUS:		# if we have the status of the file that was changed
						mined_with_status[commit_hash].append(file_full_path)		# all files changed in that commit that we have the status

		# Here we finished collecting commits vs. changed files with status for that project. Then, we can checkout the files in a specific commits and move then to other folder to collect smells
		for key, value in mined_with_status.items():
			for v in value:		# for each file changed in that commit, we checkout the commit in that file
				os.chdir("/Users/isabellaferreira/Dropbox/PhD/Winter2020/ECSE611_SoftwareAnalytics/replication/ECSE611-Replication/smells")
				path_v = PUPPET_PROJECTS + v
				proj_name = v.replace(project + "/", "")

				print("file: ", proj_name)

				if (".git" not in proj_name) or ("git" not in proj_name):
					# print("puppet project: ", PUPPET_PROJECTS+project+"/")
					os.chdir(PUPPET_PROJECTS+project+"/")			# project folder
					# print("Current dir: ", os.getcwd())
					print("Checking out repo...")
					try:
						subprocess.check_output("git checkout " + key + " " + proj_name,  shell=True)    # git checkout <commit>  <file>
					except:
						print("unable to checkout: %s %s" % (key, proj_name))
						
					name_new_dir = OUTPUT + ecosystem + "/" + project+"/"+key+"/"		# one folder for each project and each commit
					# print("name new dir: ", name_new_dir)
					# print("Current dir: ", os.getcwd())


					if not os.path.exists(name_new_dir):
						try:
							os.makedirs(name_new_dir)
							#os.chdir(name_new_dir)
						except:
							print("could not create directory")
						try: 
							# print("moving project source: ", proj_name)
							# print("moving project dest: ", name_new_dir)
							#shutil.copyfile(proj_name, name_new_dir)
							# print("cp: ", "cp " +  proj_name + " " + name_new_dir)
							subprocess.check_output("cp " +  proj_name + " " + name_new_dir,  shell=True)    # git checkout <commit>  <file>
							print("File copied successfully.")
						except:
							print(">>>>>>>>>>>>>>>>>>>>> Error moving file")
					else:
						try: 
							# print("moving project source: ", proj_name)
							# print("moving project dest: ", name_new_dir)
							# print("cp: ", "cp " +  proj_name + " " + name_new_dir)
							subprocess.check_output("cp " +  proj_name + " " + name_new_dir,  shell=True)    # git checkout <commit>  <file>
							print("File copied successfully.")
						except:
							print(">>>>>>> Error moving file")
					print("\n\n")

def process_file(filename):
	df = pd.read_csv(filename, encoding='utf-8', sep=',')
	return df

def get_paper_data():
	for file in INPUT_FILES:
		ecosystem = file.split("/")[-1].split(".csv")[0].split("_")[1]
		if ecosystem == "MIR":
			full_ecosystem = "mirantis"
		elif ecosystem == "MOZ":
			full_ecosystem = "mozilla-releng"
		elif ecosystem == "OST":
			full_ecosystem = "openstack"
		elif ecosystem == "WIK":
			full_ecosystem = "wikimedia"

		df = process_file(file)
		PAPER_DATA[ecosystem] = df

		for index, row in df.iterrows():
			file = row["file_"]
			replacement = "/Users/akond/PUPP_REPOS/" + full_ecosystem + "-" + "downloads/"
			file = file.replace(replacement, "")
			bug_status = row["defect_status"]
			FILE_BUG_STATUS[file] = bug_status 

if __name__ == '__main__':
	get_paper_data()
	get_mined_data()