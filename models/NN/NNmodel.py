import string
import keras
from keras.models import Input
from keras.layers import Dense, Dropout, Flatten
from keras.layers.advanced_activations import LeakyReLU
from models.abstract_model import AbstractModel
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT






class NN(AbstractModel):
    def __init__(self,name:str="Defualt",verbose:bool=True):
        super(NN, self).__init__(name=name,verbose=verbose)

        
    

    def _set_layers(self):
        """
        We have a set of (3,3) kernels, having 'same' padding. The number of kernels keep increasing.
        In the end we have a two dense layers, which then is fully connected.
        Activation function: LeakyReLU
        Pooling: MaxPool (2,2)
        """
        input_width  = IMAGE_WIDTH
        input_height = IMAGE_HIGHT
        channels = 1

        num_classes = 2
        model = self.model
        model.add(Input(shape=( input_width,input_height,channels))) 
        model.add(Flatten())
        model.add(Dense(8, activation='linear'))
        model.add(LeakyReLU(alpha=0.1))
        #model.add(Dropout(0.3))
        model.add(Dense(4, activation='linear'))
        model.add(LeakyReLU(alpha=0.1))            
        #model.add(Dropout(0.3))
        model.add(Dense(16, activation='linear'))
        model.add(Dense(num_classes, activation='softmax'))