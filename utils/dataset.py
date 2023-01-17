
from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image
import random

from utils.common import memoize


def load_dataset_no_memoization():

    X = []
    y = []
    labels = []

    directory = "data/training_data"
    end = ".bmp"
    onlyfiles = sorted([f[:-len(end)] for f in listdir(directory)
                       if isfile(join(directory, f)) and f.endswith(end)])
    for file in onlyfiles:
        # get training data
        img = Image.open(f"{directory}/{file}.bmp")
        ary = np.asarray(img)
        X.append(ary)

        # get label
        label = -1
        with open(f"data/labels/{file}.txt", "r") as f:
            label = f.read()
        curr_y = [0, 0]  # hot encoding
        curr_y[int(label)] = 1
        y.append(curr_y)
        labels.append(file)

    X = np.asarray(X)
    y = np.asarray(y)
    labels = np.asarray(labels)

    # We want to force values to be in range [0,1]
    # X = X.astype('float32')
    # X = X / 255.0
    return X, y, labels


load_dataset = memoize(load_dataset_no_memoization)


def sub_sample(valid_X, valid_Y, valid_labels, sample_size):
    all_data_zip = []
    for i in range(len(valid_labels)):
        all_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))

    picks = random.sample(all_data_zip, sample_size)

    valid_X, valid_Y, valid_labels = zip(*picks)
    return valid_X, valid_Y, valid_labels


def bootstrap(X, y):
    X, y = makeBiggestMeetSmallest(X, y)
    # X,y = duplicateSmallestToMatchBiggest(X,y)
    return X, y


def makeBiggestMeetSmallest(X, y):
    unique, counts = np.unique(y, return_counts=True)
    occurences = dict(zip(unique, counts))
    print(occurences)
    zeros = occurences[0]
    ones = occurences[1]
    diff = abs(zeros-ones)
    biggest = -1
    if ones > zeros:
        biggest = 1
    else:
        biggest = 0

    new_x = []
    new_y = []

    for i in range(len(y)):

        if y[i] == biggest and diff > 0:
            # we skip diff many
            diff -= 1
            continue
        else:
            new_x.append(X[i])
            new_y.append(y[i])
    X = np.array(new_x)
    y = np.array(new_y)

    return X, y


def duplicateSmallestToMatchBiggest(X, y):
    unique, counts = np.unique(y, return_counts=True)
    occurences = dict(zip(unique, counts))
    print(occurences)
    zeros = occurences[0]
    ones = occurences[1]

    smallest = -1
    if ones > zeros:
        smallest = 0
    else:
        smallest = 1

    X_smallest = [x for i, x in enumerate(X) if y[i] == smallest]
    x_new = []
    y_new = [smallest]*(abs(ones-zeros))
    for _ in range(abs(ones-zeros)):
        x_new.append(random.choice(X_smallest))

    if len(x_new) > 0:
        X = np.append(X, x_new, axis=0)
        y = np.append(y, y_new)

    unique, counts = np.unique(y, return_counts=True)
    occurences = dict(zip(unique, counts))
    print(occurences)

    return X, y
