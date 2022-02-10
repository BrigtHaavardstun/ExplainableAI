#from LM.QuineMcCluskey import find_minterms
from LM.kMaps import Kamps
from utils.common import convert_label_to_binary, convert_digit_to_binary

 

def run_lm(labels, predictions):
    """
    Given labels and correspoding predictions, runs Karnaugh maps to find the minimal fitting boolean expression.

    Since we only have a few rows of explinations, the minimal "fitting" expression will be the boolean expression
    witch evalutes to the same for the known rows. All other rows will be considered "don't care". 

    As we don't know their value we have little to no reasone to asume they are one or the othe.
    One could argue this is a faulty logic, as if "a=t,b=f,c=f", "a=t,b=t,c=f","a=t,b=f,c=t" all is true,
    it is not given that "a=t,b=t,c=t" also gives true.
    """

    #split into true and false groups
    predicted_true = []
    predicted_false = []
    for label, predicition in zip(labels,predictions):
        # predictions is one-hot encoded. Where [1 ,0] == False and [0, 1] == True
        if predicition == [0,1]:
            predicted_true.append(label)
        elif predicition == [1,0]:
            predicted_false.append(label)
        else:
            raise ValueError(f"Invalid prediction. Got {predicition} from {label}")



    prediction_true_binary  = [convert_label_to_binary(label) for label in predicted_true]
    prediction_false_binary = [convert_label_to_binary(label) for label in predicted_false]

    dont_cares = []
    for i in range(16):
        if (convert_digit_to_binary(i) not in prediction_true_binary) and (convert_digit_to_binary(i) not in prediction_false_binary):
            dont_cares.append(convert_digit_to_binary(i))
    
    if len(prediction_true_binary) == 0:
        return "F" 
    elif len(prediction_false_binary) == 0:
        return "T"
    min_terms = Kamps.find_minterms(prediction_true_binary, dont_cares)
    return(min_terms)



