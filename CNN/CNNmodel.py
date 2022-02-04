import string
import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
#from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import adam_v2





class CNN:
    def __init__(self, verbose:bool, name:string, batch_size=int) -> None:
        self.model = Sequential()
        self.verbose = verbose
        self.name = name
        self.batch_size = batch_size
        self._set_layers()
        self._compile()
        

    def _set_layers(self):
        """
        We have a set of (3,3) kernels, having 'same' padding. The number of kernels keep increasing.
        In the end we have a two dense layers, which then is fully connected.
        Activation function: LeakyReLU
        Pooling: MaxPool (2,2)
        """
        input_width  = 57
        input_height = 57
        channels = 1

        num_classes = 2
        model = self.model
        model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',padding='same',input_shape=( input_width,input_height,channels))) 
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D((2, 2),padding='same'))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
        model.add(LeakyReLU(alpha=0.1))                  
        model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
        model.add(Dropout(0.4))
        model.add(Flatten())
        model.add(Dense(128, activation='linear'))
        model.add(LeakyReLU(alpha=0.1))           
        model.add(Dropout(0.3))
        model.add(Dense(128, activation='linear'))
        model.add(LeakyReLU(alpha=0.1)) 
        model.add(Dense(num_classes, activation='softmax'))

    def _compile(self):
        """
        Compiles the model.
        """
        self.model.compile(loss=keras.losses.categorical_crossentropy, optimizer=adam_v2.Adam(),metrics=['accuracy'])
        if self.verbose:
            self.model.summary()

    def fit_model(self, train_X, train_Y, valid_X, valid_Y, epochs):
        """"
        Trains the model on the given dataset.
        Returns history of training.
        """
        training_history = self.model.fit(train_X, train_Y, epochs=epochs,verbose=self.verbose,validation_data=(valid_X, valid_Y))
        return training_history

    def _test_eval(self, test_X, test_Y):
        "Performs test evaluation"
        return self.model.evaluate(test_X, test_Y, verbose=self.verbose)
    
    def save(self):
        self.model.save(f"CNN/savedModels/{self.name}")

    def predict(self, x):
        return self.model.predict(x)

