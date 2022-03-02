from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from models.abstract_model import AbstractModel
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT


class CNN(AbstractModel):
    def __init__(self, name: str = "Defualt", verbose: bool = True):
        super(CNN, self).__init__(name=name, verbose=verbose)

    def _set_layers(self):
        """
        We have a set of (3,3) kernels, having 'same' padding. The number of kernels keep increasing.
        In the end we have a two dense layers, which then is fully connected.
        Activation function: LeakyReLU
        Pooling: MaxPool (2,2)
        """
        input_width = IMAGE_WIDTH
        input_height = IMAGE_HIGHT
        channels = 1

        num_classes = 2
        model = self.model
        model.add(Conv2D(32, kernel_size=(3, 3), activation='linear',
                  padding='same', input_shape=(input_width, input_height, channels)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D((2, 2), padding='same'))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, (3, 3), activation='linear', padding='same'))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3, 3), activation='linear', padding='same'))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
        model.add(Dropout(0.4))
        model.add(Flatten())
        model.add(Dense(128, activation='linear'))
        model.add(LeakyReLU(alpha=0.1))
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='linear'))
        model.add(LeakyReLU(alpha=0.1))
        model.add(Dense(num_classes, activation='softmax'))
