import os
import csv
import Aggregator
from SmellDetector import Constants as CONSTS, Analyzer
# from collections import defaultdict

# results = defaultdict(list)

smells_types = ["Multifaceted Abstraction - Form 1", "Multifaceted Abstraction - Form 2", "Unnecessary Abstraction", "Imperative Abstraction", "Missing Abstraction", "Insufficient Modularization - Form 1", "Insufficient Modularization - Form 2", "Insufficient Modularization - Form 3", "Unstructured Module - Form 1", "Unstructured Module - Form 2", "Unstructured Module - Form 3", "Tightly-coupled Module", "Duplicate Abstraction", "Broken Hierarchy", "Missing Dependency", "Hairball Structure", "Deficient Encapsulation", "Weakend Modularity"]

root = CONSTS.REPO_ROOT
print("Initiating Analyzer...")
totalRepos = len(os.listdir(root))
currentItem = 0
for dirs in os.listdir(root):
	#print(">>> dirs: ", dirs)
	ecosystem = dirs.split("_")[0]
	project_name = dirs.split("_")[1]
	results_smells_path = "../../results_smells/"+ecosystem+"/"
	print("&&&&&&&&&&&&&&&&&&&&&& results smells path: ", results_smells_path)
	results_file_name = project_name+".csv"

	if not os.path.exists(results_smells_path):
		try:
			os.makedirs(results_smells_path)
			#os.chdir(name_new_dir)
		except:
			print("could not create directory: ", results_smells_path)

	
	if (dirs != ".DS_Store") and (dirs != "AggregatedOutput.csv") and (dirs  != "Puppeteer_output.txt"):
		full_path = os.path.join(results_smells_path, results_file_name)
		with open (full_path, "a") as outputfile:
			projectFolder = os.path.join(root, dirs)
			# print(">>>>>>>>>>>>> subdirectory: ", dirs)

			csv_columns = ['ecosystem', 'project', 'file', 'commit', 'puppetFileCount', 'totalClasses', 'totalDefines', 'totalFiles', 'totalPackages', 'totalServices', 'totalExecs', 'totalLOC', 'Multifaceted Abstraction - Form 1', 'Multifaceted Abstraction - Form 2', 'Unnecessary Abstraction', 'Imperative Abstraction', 'Missing Abstraction', 'Insufficient Modularization - Form 1', 'Insufficient Modularization - Form 2', 'Insufficient Modularization - Form 3', 'Unstructured Module - Form 1', 'Unstructured Module - Form 2', 'Unstructured Module - Form 3', 'Tightly-coupled Module', 'Duplicate Abstraction', 'Broken Hierarchy', 'Missing Dependency', 'Hairball Structure', 'Deficient Encapsulation', 'Weakend Modularity']
			writer = csv.DictWriter(outputfile, fieldnames=csv_columns)
			writer.writeheader()
								
			for subdirs in os.listdir(projectFolder):
				#print(">>> subdirs: ", subdirs)
				if (subdirs != ".DS_Store") and (subdirs != "AggregatedOutput.csv") and (subdirs  != "Puppeteer_output.txt"):
						files = os.path.join(projectFolder, subdirs)

						for item in os.listdir(files):
							currentFile = os.path.join(files, item)
							print("Analyzing: " + currentFile)
							if os.path.isfile(currentFile):
								resultsMetrics, CONSTS.smellsResults = Analyzer.analyze(projectFolder, currentFile)

								results = {}
								results["ecosystem"] = ecosystem
								results["project"] = project_name
								results["file"] = item
								results["commit"] = subdirs
								results["puppetFileCount"] = resultsMetrics[currentFile][0]
								results["totalClasses"] = resultsMetrics[currentFile][1]
								results["totalDefines"] = resultsMetrics[currentFile][2]
								results["totalFiles"] = resultsMetrics[currentFile][3]
								results["totalPackages"] = resultsMetrics[currentFile][4]
								results["totalServices"] = resultsMetrics[currentFile][5]
								results["totalExecs"] = resultsMetrics[currentFile][6]
								results["totalLOC"] = resultsMetrics[currentFile][7]

								result_total = []
								result_total.append(results)

								for s in smells_types:
									if s in CONSTS.smellsResults:
										results[s] = CONSTS.smellsResults[s]
									else:
										results[s] = 0

								print("results: ", results)

								# for key in results.keys():
								# 	outputfile.write("%s,%s\n"%(key,results[key]))

								
								try:
									
									for value in result_total:
										print("value: ", value)
										writer.writerow(value)
								except IOError:
									print("I/O error")

								# print("results: ", results)
								# for key, value in resultsMetrics.items():
								# 	print(">>> Metrics")
								# 	print("key: ", key)
								# 	print("value: ", value) # puppetFileCount, totalClasses,totalDefines,totalFiles,totalPackages,totalServices,totalExecs,totalLOC

								# print("\n\n")
								# for key, value in CONSTS.smellsResults.items():
								# 	print(">>> Smells")
								# 	print("key: ", key)
								# 	print("value: ", value)

							# currentItem += 1
							# print (str("{:.2f}".format(float(currentItem * 100)/float(totalRepos))) + "% analysis done.")
print("Analyzer - Done.")
						
# print("Initiating metrics and smells aggregator...")
# aggregatedFile = open(root + "/" + CONSTS.AGGREGATOR_FILE, 'wt')
# aggregatedFile.write(CONSTS.CSV_HEADER)
# for dirs in os.listdir(root):
# 	print(">>> DIRS: ", dirs)
# 	if (dirs != ".DS_Store") and (dirs != "AggregatedOutput.csv") and (dirs  != "Puppeteer_output.txt"):
# 		projectFolder = os.path.join(root, dirs)
# 		print(">>> CURRENT FOLDER: ", projectFolder)
# 		for subdirs in os.listdir(projectFolder):
# 			if (subdirs != ".DS_Store") and (subdirs != "AggregatedOutput.csv") and (subdirs  != "Puppeteer_output.txt"):
# 					files = os.path.join(projectFolder, subdirs)
# 					for item in os.listdir(files):
# 						currentFile = os.path.join(files, item)
# 						print("Analyzing: " + currentFile)
# 						Aggregator.aggregate(projectFolder, currentFile, aggregatedFile)
# aggregatedFile.close()
# print("Metrics and smells aggregator - Done.")

# 	subdirs = os.path.join(projectFolder, subdirs)
# 	for item in os.listdir(files):
# 	# if not os.path.isfile(currentFolder):
# 		Aggregator.aggregate(currentFolder, item, aggregatedFile)
# aggregatedFile.close()
# print("Metrics and smells aggregator - Done.")


#for dirs, subdirs, files in os.walk(root):
# 	print("dirs: ", dirs)
# 	print("subdirs: ", subdirs)
# 	print("files: ", files)
# 	# changing to calculate instead of folder, the file
# 	if (".DS_Store" not in files) and ("AggregatedOutput.csv" not in files) and ("Puppeteer_output.txt" not in files):
# 		for item in files:
# 			print("item: ", item)
# 			print("\n\n")

# 			currentFolder = os.path.join(root, item)
# 			print("current folder: ", currentFolder)

# 			print("Analyzing: " + currentFolder)
# 			if not os.path.isfile(currentFolder):
# 				Analyzer.analyze(currentFolder, item)
# 			currentItem += 1
# 			print (str("{:.2f}".format(float(currentItem * 100)/float(totalRepos))) + "% analysis done.")
# print("Analyzer - Done.")

# print("Initiating metrics and smells aggregator...")
# aggregatedFile = open(root + "/" + CONSTS.AGGREGATOR_FILE, 'wt')
# aggregatedFile.write(CONSTS.CSV_HEADER)
# for item in os.listdir(root):
# 	print(">>> ITEM: ", item)
# 	currentFolder = os.path.join(root, item)
# 	if not os.path.isfile(currentFolder):
# 		Aggregator.aggregate(currentFolder, item, aggregatedFile)
# aggregatedFile.close()
# print("Metrics and smells aggregator - Done.")