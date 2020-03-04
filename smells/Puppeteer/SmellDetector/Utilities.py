from SmellDetector import Constants as CONSTS

def myPrint(msg):
    if(CONSTS.DEBUG_ON):
        print(msg)

def reportSmell(outputFile, fileName, smellName, reason):
    outputFile.write(smellName + " at " + reason + " in file " + fileName + "\n")
    myPrint(smellName + " at " + reason + " in file " + fileName + "\n")

    print(smellName + " at " + reason + " in file " + fileName + "\n")
    if smellName in CONSTS.smellsResults:
    	CONSTS.smellsResults[smellName] = CONSTS.smellsResults[smellName] + 1
    else:
    	CONSTS.smellsResults[smellName] = 1

def intersection(list1, list2):
    return list(set(list1) & set(list2))

def summation(list1, list2):
    return list(set(list1) | set(list2))