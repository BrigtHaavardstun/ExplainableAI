

from os import listdir
from os.path import isfile, join
from utils.global_props import booleanFunctionDefiniton, get_all_letters


def parseNameToLabel(fileName):
    bool_dict = {}
    for l in get_all_letters():
        bool_dict[l] = l in fileName
    return booleanFunctionDefiniton(bool_dict)

# filename = A232, ABC19, BD23 etc.


def generateLable(folderPrefix, filename):
    storeValue = None
    if parseNameToLabel(fileName=filename):
        storeValue = 1
    else:
        storeValue = 0

    with open(f"{folderPrefix}{filename}.txt", "w") as f:
        f.write(str(storeValue))


def readAllFileNamesInTrainingData():
    directory = "data/training_data"
    onlyfiles = sorted([f[:-4] for f in listdir(directory)
                       if isfile(join(directory, f))])
    return onlyfiles


def run():
    all_files = readAllFileNamesInTrainingData()

    prefixFolder = "data/lables/"
    for file in all_files:
        generateLable(prefixFolder, file)
