

from os import listdir
from os.path import isfile, join

def booleanFunction(A,B,C,D):
    return (A and not B and C and not D) or (not A and B and not C and D) or (D and  C and  B) or (not A  and B and not D)  #!!! MEGA IMPORTANT, defines ML if we need multiple MLs
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
    prefixFolder = "lables/"
    directory = "training_data"
    onlyfiles = sorted([f[:-4] for f in listdir(directory) if isfile(join(directory, f))])
    for file in onlyfiles:
        generateLable(prefixFolder,file)


if __name__ == "__main__":
    readAllFileNamesInTrainingData()