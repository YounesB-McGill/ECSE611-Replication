from SmellDetector import AbsSmellDectector, ModSmellDectector, HieSmellDectector, DepSmellDectector, EncSmellDectector


#def detectSmells(folder, outputFile):
def detectSmells(file, outputFile):
	# print (">>> FILE SMELLS DETECTOR: ", file)
	# print (">>> outputFile SMELLS DETECTOR: ", outputFile)
	AbsSmellDectector.detectSmells(file, outputFile)
	EncSmellDectector.detectSmells(file, outputFile)
	ModSmellDectector.detectSmells(file, outputFile)
	DepSmellDectector.detectSmells(file, outputFile)
	HieSmellDectector.detectSmells(file, outputFile)
