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
		repo = "wikimedia-downloads"
	return project, repo, line["File"]

def find_file_in_csv(project, repo, file, orig_file):
	better_file = '/' + file
	save_return = 0
	if project =="Mirantis":
		for i in range(0, len(orig_file)):
			if repo in orig_file[i][1]:
				if orig_file[i][1].endswith(better_file):
					if save_return != 0:
						print(orig_file[i][1], "  ", repo, "  ", file)
						return -1
					else:
						save_return = i
	elif project == "openstack":
		for i in range(0, len(orig_file)):
			if repo in orig_file[i][1]:
				if orig_file[i][1].endswith(better_file):
					if save_return != 0:
						print(orig_file[i][1], "  ", repo, "  ", file)
						return -1
					else:
						save_return = i
	elif project == "wikimedia":
		for i in range(0, len(orig_file)):
			if orig_file[i][1].endswith(better_file):
				if save_return != 0:
					print(orig_file[i][1], "  ", repo, "  ", file)
					return -1
				else:
					save_return = i
	elif project == "mozilla":
		for i in range(0, len(orig_file)):
			if orig_file[i][1].endswith(better_file):
				if save_return != 0:
					print(orig_file[i][1], "  ", repo, "  ", file)
					return -1
				else:
					save_return = i
	return save_return

def find_two_matches(df_in, total_filename):
	matches = []
	df_matches = []
	for index, row in df_in.iterrows():
		project, repo, file = get_important_info(row)
		better_file = '/' + file
		if total_filename.endswith(better_file):
			matches.append(better_file)
			df_matches.append(row)

	best_match = max(matches, key=len)
	best_match = best_match[2:]
	for line in df_matches:
		if best_match in line[1]:
			return line, line[1]
	

def run_through_project(filename_own, filename_base, project):
	df = pd.read_csv(filename_own, encoding='utf-8', sep=',')

	file_base = open(filename_base, 'r')
	data = list(csv.reader(file_base))

	total_found = 0
	total_double_found = 0

	problem_numbers = []

	for index, row in df.iterrows():
		project, repo, file = get_important_info(row)
		result = find_file_in_csv(project, repo, file, data)
		if result == -1:
			total_double_found+=1
		elif result != 0:
			total_found+=1
			if(len(data[result]) > 17):
				total_double_found+=1
				res = data[result]
				print(res[1],"  ", repo, "  ", file)
				problem_numbers.append(data[result])
				continue
			data[result].append(row["contributers"])
			data[result].append(row["top"])
			data[result].append(row["major"])
			data[result].append(row["minor"])
	data[0].append("contributers")
	data[0].append("top")
	data[0].append("major")
	data[0].append("minor")

	print("found" , total_found)
	print("double" , total_double_found)
	if project == "wikimedia":
		for line in problem_numbers:
			bm, best_match = find_two_matches(df, line[1])
			print(bm)
			for i in range(0, len(data)):
				if data[i][1].endswith(best_match):
					print(line)
					new_line = line
					new_line[15] = bm["contributers"]
					new_line[16] = bm["top"]
					new_line[17] = bm["major"]
					new_line[15] = bm["minor"]
					data.append(new_line)
	if project == "mozilla":
		for line in problem_numbers:
			bm, best_match = find_two_matches(df, line[1])
			print(bm)
	for line in data:
		if len(line) < 18:
			# print(line[1])
			problem_numbers.append(line)
	
	print(len(data))
	for line in problem_numbers:
		data.remove(line)
	print(len(data))

	out_df = pd.DataFrame(data, columns = data[0])
	fixed_out_df = out_df.drop(index=0, axis = 0)
	if project == "Mirantis":
		fixed_out_df.to_csv('data/ownership_data_files/IST_MIR_OWN.csv', index = False)
	elif project == "openstack":
		fixed_out_df.to_csv('data/ownership_data_files/IST_OST_OWN.csv', index = False)
	elif project == "mozilla":
		fixed_out_df.to_csv('data/ownership_data_files/IST_MOZ_OWN.csv', index = False)
	elif project == "wikimedia":
		fixed_out_df.to_csv('data/ownership_data_files/IST_WIK_OWN.csv', index = False)

	
def run_through_all():
	# run_through_project("data/ownership_data_files/mirantis_output.csv", "data/IST_MIR.csv", "Mirantis")
	run_through_project("data/ownership_data_files/mozilla_output.csv", "data/IST_MOZ.csv", "mozilla")
	# run_through_project("data/ownership_data_files/wikimedia_output.csv", "data/IST_WIK.csv", "wikimedia")
	# run_through_project("data/ownership_data_files/openstack_output.csv", "data/IST_OST.csv", "openstack")


run_through_all()
# filename = "data/ownership_data_files/mirantis_output.csv"
# df = pd.read_csv(filename, encoding='utf-8', sep=',')

# file = open("data/IST_MIR.csv", 'r')
# data = list(csv.reader(file))

# total_found = 0
# total_double_found = 0

# for index, row in df.iterrows():
# 	project, repo, file = get_important_info(row)
# 	result = find_file_in_csv(project, repo, file, data)
# 	if result != 0:
# 		total_found+=1
# 		data[result].append(row["contributers"])
# 		data[result].append(row["top"])
# 		data[result].append(row["major"])
# 		data[result].append(row["minor"])

# data[0].append("contributers")
# data[0].append("top")
# data[0].append("major")
# data[0].append("minor")
# out_df = pd.DataFrame(data, columns = data[0])
# fixed_out_df = out_df.drop(index=0, axis = 0)
# fixed_out_df.to_csv('data/ownership_data_files/IST_MIR_OWN.csv', index = False)
# print(total_found)
# print(total_double_found)

# for line in data:
# 	if len(line) < 18:
# 		print(line[1])