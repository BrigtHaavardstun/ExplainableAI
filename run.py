from CNN.trainCNN import run as generate_new_model
from CNN.trainCNN import load_model
from LM.lm import arg_min_ta
from utils.dataset import load_dataset
from PIL import Image

import random



def train_model():
    generate_new_model(name="new model v1.0", save=True, verbose=True)

def _sub_sample(valid_X, valid_Y, valid_labels, sample_size):
    all_data_zip = []
    for i in range(len(valid_labels)):
        all_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))


    picks = random.sample(all_data_zip,sample_size)
    
    valid_X,valid_Y,valid_labels = zip(*picks)
    return valid_X,valid_Y,valid_labels 

def run_system():
    #model, data = get_model(save=True,with_data_valid=True, verbose=True, name="StandarStrongModel")
    #valid_X, valid_Y,valid_labels = data

    #load datamodel
    model= load_model(name="new model v1.0" )
    
    #get data TODO: should get less data
    valid_X,valid_Y,valid_labels = load_dataset()
    valid_X,valid_Y,valid_labels= _sub_sample(valid_X,valid_Y,valid_labels, 200)


    result = arg_min_ta(valid_X=valid_X, valid_Y=valid_Y, valid_labels=valid_labels, model_ai=model)


    for (example_X, example_Y, example_label) in result:
        Image.fromarray(example_X).show()
        prediction = model.predict(example_X)
        print(f"label: '{example_label}', Correct: {example_Y}, predicted: {prediction}")





import LM.QuineMcCluskey as QMC
import LM.kMaps.Kamps as kMaps
if __name__ == "__main__":
    run_system()
    #train_model()
    #QMC.test()
