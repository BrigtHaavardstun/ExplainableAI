
import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import adam_v2
import numpy as np
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT

import abc


class AbstractModel(metaclass=abc.ABCMeta):

    def __init__(self, model=None, name: str = "Defualt", verbose: bool = True):
        self.verbose = verbose
        self.name = name
        if model:
            self.model = model
        else:
            self.model = Sequential()
            self._set_layers()
            self._compile()

    def __repr__(self):
        return self.name

    @abc.abstractmethod
    def _set_layers(self):
        """
        This has to be done in sub class
        """
        pass

    def _compile(self):
        """
        Compiles the model.
        """
        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=adam_v2.Adam(), metrics=['accuracy'])
        if self.verbose:
            self.model.summary()

    def fit_model(self, train_X, train_Y, valid_X, valid_Y, epochs):
        """"
        Trains the model on the given dataset.
        Returns history of training.
        """
        training_history = self.model.fit(
            train_X, train_Y, epochs=epochs, verbose=self.verbose, validation_data=(valid_X, valid_Y))
        return training_history

    def _test_eval(self, test_X, test_Y):
        "Performs test evaluation"
        return self.model.evaluate(test_X, test_Y, verbose=self.verbose)

    def save(self):
        self.model.save(f"models/savedModels/{self.name}")

    def predict(self, x):
        """
        WARNING performs max over options to calculate one-hot encoding over possibilities.
        """
        x = np.array([x])

        prediction = self.model.predict(x)[0]

        if prediction[0] > prediction[1]:
            return [1, 0]
        else:
            return [0, 1]
