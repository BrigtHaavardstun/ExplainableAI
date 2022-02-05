from utils.dataset import load_dataset
from sklearn.model_selection import train_test_split
from .CNNmodel import CNN
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np

def train_test_validation_split(size):
    train, test_valid = train_test_split(list(range(size)), test_size=0.4)
    test, valid = train_test_split(test_valid, test_size=0.4)
    return train, test, valid




def run(verbose=False, save=True, with_data_valid=False, name="Standar"):
    """
    Trains a CNN model based on data from ./data folder.
    Return: the trained model.
    """

    # Get the data
    X,Y, labels = load_dataset()

    # Perfrom train_test_split, with labels.
    trainIdx, testIdx, validIdx = train_test_validation_split(len(X))
    # Train data
    train_X, train_Y, train_label = [], [], []
    for i in trainIdx:
        train_X.append(X[i])
        train_Y.append(Y[i])
        train_label.append(labels[i])

    train_X = np.array(train_X)
    train_Y = np.array(train_Y)
    train_label = np.array(train_label)

    #Test data
    test_X, test_Y, test_label = [],[], []
    for i in testIdx:
        test_X.append(X[i])
        test_Y.append(Y[i])
        test_label.append(labels[i])

    test_X = np.array(test_X)
    test_Y = np.array(test_Y)
    test_label = np.array(test_label)

    #Validation data
    valid_X, valid_Y,valid_labels = [], [], []
    for i in validIdx:
        valid_X.append(X[i])
        valid_Y.append(Y[i])
        valid_labels.append(labels[i])

    valid_X = np.array(valid_X)
    valid_Y = np.array(valid_Y)
    valid_labels = np.array(valid_labels)

    

    # Create model
    print("making the model...")
    model = CNN(verbose=True, name=name)

    

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

def load_model(name):
    ai_model =  keras.models.load_model(f'CNN/savedModels/{name}')
    cnn_model = CNN(name=name, model=ai_model)
    return cnn_model


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