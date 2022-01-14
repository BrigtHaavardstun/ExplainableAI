from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image
import random
class model:
    def __init__(self, boolFunc, labelData, images) -> None:
        self.boolFunc = boolFunc   

    


def load_train_test():

    X = []
    y = []

    directory = "training_data"
    onlyfiles = sorted([f[:-4] for f in listdir(directory) if isfile(join(directory, f)) and f != "clean.sh"])
    for file in onlyfiles:
        # get training data
        img = Image.open(f"{directory}/{file}.bmp")
        ary = np.asarray(img).flatten()
        X.append(ary)

        # get lable
        lable = -1
        with open(f"lables/{file}.txt", "r") as f:
            lable = f.read()
        y.append(int(lable))


    X = np.asarray(X)
    y = np.asarray(y)
    return X,y


def bootstrap(X,y):

    unique, counts = np.unique(y, return_counts=True)
    occurences = dict(zip(unique, counts))
    print(occurences)
    zeros = occurences[0]
    ones = occurences[1]
    if zeros < ones:
        X_0 = [x for i,x in enumerate(X) if y[i] == 0 ] 
        for i in range(ones-zeros):
            x_random = random.choice(X_0)
            X = np.append(X,[x_random], axis=0)
            y = np.append(y, [0])
    else:
        X_1 = [x for i,x in enumerate(X) if y[i] == 1 ] 
        for i in range(zeros-ones):
            x_random = random.choice(X_1)
            X = np.append(X,[x_random], axis=0)
            y = np.append(y, [1])
    
    unique, counts = np.unique(y, return_counts=True)
    occurences = dict(zip(unique, counts))
    print(occurences)
    print(len(X), len(y))

    return X,y
    

"""
Below is testing to get used to generate NNs
"""


print("loading dataset...")
#X, y = make_classification(n_samples=10000, random_state=1)
X,y = load_train_test()

print("test train split")
X,y = bootstrap(X,y)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=1)
print("fiting data")
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,  hidden_layer_sizes=(16, 4, 16),random_state=1, max_iter=3000).fit(X_train, y_train)
print("predicting")
print(clf.predict_proba(X_test[:1]))
print(clf.predict(X_test[:5, :]))
print("scoring")
print(clf.score(X_test, y_test))

print("####own testing#####")
predicted = clf.predict(X_test)
disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
disp.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp.confusion_matrix}")

plt.show()

print("You will now be presented with the predictions which failed")
testing = True
for i, (pred, correct) in enumerate(zip(predicted, y_test)):
    if pred != correct:
        if not testing:
            continue
        print(i)
        print(type(X_test[i]))
        print(X_test[i])
        ary = np.array(X_test[i],np.uint8)
        print(ary)
        d2ary = np.reshape(ary, (-1,int(ary.size**0.5)))
        img = Image.fromarray(d2ary)
        img.show()
        ans = input("q to quit, enter to continue: ").strip().lower()
        if ans == "q":
            break
