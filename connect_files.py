import os
import pandas as pd

def perform_line_cleanup(line):
	line = line.replace('/Users/akond/PUPP_REPOS/mirantis-downloads/','Mirantis-')
	return line

def find_file(filename):
	os.chdir("../source-code-repos")

	try:
		file = open(filename, 'r')
		# print("found file")
	except FileNotFoundError:
		print("file not found")


filename = "data/IST_MIR.csv"
df = pd.read_csv(filename, encoding='utf-8', sep=',')


for line in df['file_']:
	cleaned_line = perform_line_cleanup(line)
	find_file(cleaned_line)