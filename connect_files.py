import os
import pandas as pd

def perform_line_cleanup(line):
	line = line.replace('/Users/akond/PUPP_REPOS/mirantis-downloads/','Mirantis-')
	print(line)

filename = "data/IST_MIR.csv"
df = pd.read_csv(filename, encoding='utf-8', sep=',')


for line in df['file_']:
	perform_line_cleanup(line)