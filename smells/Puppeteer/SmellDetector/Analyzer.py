import SmellDetector.Constants as CONSTS
from SmellDetector import SmellDectector, SizeMetrics, FileOperations, Utilities
from collections import defaultdict

def analyze(folder, file):
	resultsMetrics = defaultdict(list)		# erasing for the next file

	outputFile = open(folder + "/" + CONSTS.PUPPETEER_OUT_FILE, 'a+')
	print("folder: ", folder)
	print("file: ", file)

	puppetFileCount = FileOperations.countPuppetFiles(file)
	# print("puppetFileCount: ", puppetFileCount)
	resultsMetrics[file].append(puppetFileCount)

	outputFile.write(CONSTS.PUPPET_FILE_COUNT + str(puppetFileCount) + "\n")
	Utilities.myPrint(CONSTS.PUPPET_FILE_COUNT + str(puppetFileCount))

	metricsResults = SizeMetrics.collectSizeMetrics(file, outputFile)

	for i in metricsResults:
		resultsMetrics[file].append(i)

	# puppetFileCount, totalClasses,totalDefines,totalFiles,totalPackages,totalServices,totalExecs,totalLOC
	# print("RESULTS: ", resultsMetrics)

	CONSTS.smellsResults = {}		# erasing for the next file
	SmellDectector.detectSmells(file, outputFile)

	# print("CONSTS.smellsResults: ", CONSTS.smellsResults)
	# print("\n\n")

	outputFile.close()
	return resultsMetrics, CONSTS.smellsResults