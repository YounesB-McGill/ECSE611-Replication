import os

#def countPuppetFiles(folder):
def countPuppetFiles(file):
    counter = 0
    #for root, dirs, files in os.walk(folder):
        #for file in files:
    if file.endswith(".pp"):
        counter += 1
    return  counter