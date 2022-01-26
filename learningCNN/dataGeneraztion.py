import numpy as np
from tensorflow.keras.utils import  to_categorical
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist

def get_data():
    (train_X,train_Y), (test_X,test_Y) = fashion_mnist.load_data()
    train_X = train_X.reshape(-1, 28,28, 1)
    test_X = test_X.reshape(-1, 28,28, 1)

    # We want to force values to be in range [0,1]
    train_X = train_X.astype('float32')
    test_X = test_X.astype('float32')
    train_X = train_X / 255.
    test_X = test_X / 255.

    # Change the labels from categorical to one-hot encoding
    train_Y_one_hot = to_categorical(train_Y)
    test_Y = to_categorical(test_Y)

    from sklearn.model_selection import train_test_split
    (train_X, train_Y),(valid_X,valid_Y) = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=13)
    return train_X,train_Y,test_X,test_Y, valid_X, valid_Y


print(get_data())