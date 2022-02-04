from LM.QuineMcCluskey import find_minterms
from random import sample
from CNN.CNNmodel import CNN 
from LM.boolParser import BooleanExpression
def process_labels(labels):
    """
    Removes all digits from labels

    abc3242 -> abc
    cd33 -> cd
    """
    proccessed_labels = []
    for label in labels:
        stopIdx = 0
        for i,e in enumerate(label):
            if e.isalpha():
                stopIdx = i
            else: # e.isdigit()
                break
        proccessed_labels.append(label[0:stopIdx+1])
    return proccessed_labels

def evaluate_compatibility(booleanExpr:BooleanExpression , model_ai:CNN, valid_X, valid_labels):
    """
    For model_ai: Itterate over all(?) validation data. 
    Keep a score over how many true and false each literal combination gives.

    For booleanExpr: Evaluate all possible combinations.

    Maps will be on the form of:

    {
        "": [0,0], 
        "A": [0,0], 
        "B": [0,0], 
        "C": [0,0], 
        "D": [0,0], 
        "AB": [0,0],
        (...)
        "ABCD": [0,0],
    }
    """
    all_labels = [
        "", "A","B", "C", "D",
        "AB", "AC", "AD","BC", "BD", "CD",
        "ABC", "ABD", "ACD", "BCD", "ABCD"
    ]
    score_map_model_ai = {}
    score_map_boolexpr = {} 

    for label in all_labels:
        score_map_model_ai[label] = [0,0]
        score_map_boolexpr[label] = [0,0]
    
    # Handling boolean expression first
    for label in all_labels:
        evaluation = booleanExpr.evaluate(A="A" in label,
                                    B="B" in label,
                                    C="C" in label,
                                    D="D" in label)

    pass


def convert_to_binary_sum(label):
    """
    A: 8
    B: 4
    C: 2
    D: 1

    e.g. ACD = 8+2+1=11
    """
    binary_sum = 0
    if "A" in label:
        binary_sum += 8
    if "B" in label:
        binary_sum += 4
    if "C" in label:
        binary_sum += 2
    if "D" in label:
        binary_sum += 1

    return binary_sum



def test():
    
    labels = ["ABC", "AB", "BCD"]
    predictions = [[0,1],[0,1], [1,0]]

    bool_expr = run_lm(labels, predictions)


def run_lm(labels, predictions):
    """
    Given labels and correspoding predictions, runs QuineMcCluskey to find the minimal fitting boolean expression.

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



    prediction_true_binary_sum  = [convert_to_binary_sum(label) for label in predicted_true]
    prediction_false_binary_sum = [convert_to_binary_sum(label) for label in predicted_false]

    dont_cares = []
    for i in range(16):
        if (i not in prediction_true_binary_sum) and (i not in prediction_false_binary_sum):
            dont_cares.append(i)

    min_terms = find_minterms(prediction_true_binary_sum, dont_cares)
    return(min_terms)




def run_ta(valid_X, valid_Y, valid_labels,model_ai:CNN):
    """
    Given traning data and ai model finds examples to show to the user

    Uses QuineMcCluskey as minimzation technique.
    """
    valid_labels = process_labels(valid_labels)

    all_data_zip = []
    for i in range(len(valid_labels)):
        all_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))
    sub_sets_attempts = 1000
    sample_size = 4
    for i in  range(sub_sets_attempts):
        picks = sample(all_data_zip,sample_size)
        
        predictions = []
        labels_picked = []
        ground_truth = []
        for (x,y, label) in picks:
            predictions.append(model_ai.predict(x))
            labels_picked.append(label)
            ground_truth.append(y)

        
        booleanExprStr = run_lm(labels = labels_picked, predictions = predictions)
        boolExpr = BooleanExpression(booleanExprStr)


        compatibility = evaluate_compatibility(boolExpr, model_ai, valid_X, valid_labels)

        





if __name__ == '__main__':
    test()



        

