from utils.dataset import load_dataset
from sklearn.model_selection import train_test_split
from .CNNmodel import CNN
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np


def run(verbose=False, save=False, with_data_valid=False):
    """
    Trains a CNN model based on data from ./data folder.
    Return: the trained model.
    """

    # Get the data
    X,Y, labels = load_dataset()
    Y_zip = zip(Y, labels)

    #Split into train, test, and validation datasets
    train_X, X, train_Y_zip, Y_zip = train_test_split(X,Y_zip, stratify=Y_zip, random_state=13)
    valid_X, test_X, valid_Y_zip, test_Y_zip = train_test_split(X,Y_zip, stratify=Y_zip, random_state=13)

    train_Y,train_labels = zip(*train_Y_zip)
    valid_Y,valid_labels = zip(*valid_Y_zip)
    test_Y,test_labels = zip(*test_Y_zip)

    # Create model
    print("making the model...")
    batch_size = 100
    model = CNN(verbose=True, name='FirstTest', batch_size=batch_size)

    

    print("training the model...")
    epochs = 20
    history = model.fit_model(train_X, train_Y, valid_X, valid_Y, epochs)

    if save:
        model.save()

    if verbose:
        plot_history(history)
        disply_confusion_matrix(model.model, test_X, test_Y)

    if with_data_valid:
        return model, (valid_X, valid_Y,valid_labels)
    return model

def run_preloaded():
    # Get the data
    X,Y = load_dataset()

    #Split into train, test, and validation datasets
    train_X, X, train_Y, Y = train_test_split(X,Y, stratify=Y, random_state=13)
    valid_X, test_X, valid_Y, test_Y = train_test_split(X,Y, stratify=Y, random_state=13)


    # load model
    model = keras.models.load_model('CNN/savedModels/FirstTest')
    
    #plot_history(history)
    disply_confusion_matrix(model, valid_X, valid_Y)

    print(model.score(test_X, test_Y))

def plot_history(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()



from sklearn import metrics
def disply_confusion_matrix(model, test_X, test_Y):
    predictions = np.asarray(model.predict(test_X)).argmax(axis=1)
    test_Y = test_Y.argmax(axis=1)


    disp = metrics.ConfusionMatrixDisplay.from_predictions(test_Y, predictions)
    disp.figure_.suptitle("Confusion Matrix")
    print(f"Confusion matrix:\n{disp.confusion_matrix}")

    plt.show()
    




if __name__ == "__main__":
    run(verbose=True, save=True)