

from os import listdir
from os.path import isfile, join

def booleanFunction(A,B,C,D):
    return (B and not C) or D#!!! MEGA IMPORTANT, defines ML if we need multiple MLs
                                     # we need different bool funcs

def parseNameToLabel(fileName):
    A = "A" in fileName 
    B = "B" in fileName
    C = "C" in fileName
    D = "D" in fileName
    return booleanFunction(A,B,C,D)

# filename = A232, ABC19, BD23 etc.
def generateLable(folderPrefix, filename):
    storeValue= None
    if parseNameToLabel(fileName=filename):
        storeValue=1
    else:
        storeValue=0
    
    with open(f"{folderPrefix}{filename}.txt","w") as  f:
        f.write(str(storeValue))


def readAllFileNamesInTrainingData():
    directory = "data/training_data"
    onlyfiles = sorted([f[:-4] for f in listdir(directory) if isfile(join(directory, f))])
    return onlyfiles
    

def run():
    all_files = readAllFileNamesInTrainingData()

    prefixFolder = "data/lables/"
    for file in all_files:
        generateLable(prefixFolder,file)
