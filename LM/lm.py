#from LM.QuineMcCluskey import find_minterms
from LM.kMaps.Kamps import find_minterms
from random import sample, choice
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
        curr_label = ""
        for i,e in enumerate(label):
            if e.isalpha():
                curr_label += e
            else: # e.isdigit()
                break
        proccessed_labels.append(curr_label)
    return proccessed_labels

# This corresponds to δ in the equation
def complexity_of_image(labels):
    return sum([len(label) for label in labels])

# This corresponds to δ in the equation
def complexity_of_model(booleanExpr:BooleanExpression):
    """
    This could possibly be better formulated.
    Maybe we should count the number of literals.

    ALSO: this should be moved to a TM module
    """
    return len(booleanExpr.get_expression())


# This corresponds to λ in the equation
def evaluate_compatibility(booleanExpr:BooleanExpression , model_ai:CNN, valid_X, valid_labels):
    """
    For model_ai: Itterate over all(?) validation data. 
    Keep a score over how many true and false each literal combination gives.

    For booleanExpr: Evaluate all possible combinations.

    Maps will be on the form of:

    {
        "": [0,0], #[false_count,true_count]
        "A": [0,0], 
        "B": [0,0], 
        "C": [0,0], 
        "D": [0,0], 
        "AB": [0,0],
        (...)
        "ABCD": [0,0],
    }

    ALSO: this should be moved to a TM module

    """

    
    all_labels = [
        "", "A","B", "C", "D",
        "AB", "AC", "AD","BC", "BD", "CD",
        "ABC", "ABD", "ACD", "BCD", "ABCD"
    ]

    # Maps holding score for each label combination. 
    count_map_model_ai = {}
    count_map_boolexpr = {} 

    for label in all_labels:
        count_map_model_ai[label] = [0,0]
        count_map_boolexpr[label] = [0,0]
    
    # Handling boolean expression first
    for label in all_labels:
        evaluation = booleanExpr.evaluate(A="A" in label,
                                    B="B" in label,
                                    C="C" in label,
                                    D="D" in label)
        if evaluation:
            count_map_boolexpr[label][1] = 1
        else:
            count_map_boolexpr[label][0] = 1


    # handling ai model 
    for label, data in zip(valid_labels, valid_X):
        prediction = model_ai.predict(data) 
        if prediction == [1,0]:
            count_map_model_ai[label][0] += 1
        else:
            count_map_model_ai[label][1] += 1


    # Convert maps counting nr_false and nr_true into probabilities of true.
    # P(T|label) = nrTrue/(nrTrue +nrFalse)

    probaility_map_ai = {}
    probaility_map_boolexpr = {}
    for label in all_labels:
        # ai model
        false_count, true_count = count_map_model_ai[label]
        assert false_count+ true_count != 0, f"You didn't give the ai label {label}, hence we can't make the prediction"
        probaility_map_ai[label] = true_count/(false_count+true_count)

        # bool expr
        false_count, true_count = count_map_boolexpr[label]
        probaility_map_boolexpr[label] = true_count/(false_count+true_count)
    


    # Using mean square error. sum over all labels, (probAI - probBoolXpr)^2, 

    mean_square_error = 0
    for label in all_labels:
        mean_square_error += (probaility_map_ai[label] - probaility_map_boolexpr[label])**2
    return mean_square_error


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

def convert_to_binary_reprsentation(label): 
    converted = ""
    if "A" in label:
        converted += "1"
    else:
         converted += "0"
    if "B" in label:
        converted += "1"
    else:
        converted += "0"
    if "C" in label:
        converted += "1"
    else:
        converted += "0"
    if "D" in label:
        converted += "1"
    else:
        converted += "0"
    return converted

def convert_digit_to_binary(digit): 
    return bin(digit)[2:].zfill(4)
 

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



    prediction_true_binary  = [convert_to_binary_reprsentation(label) for label in predicted_true]
    prediction_false_binary = [convert_to_binary_reprsentation(label) for label in predicted_false]

    dont_cares = []
    for i in range(16):
        if (convert_digit_to_binary(i) not in prediction_true_binary) and (convert_digit_to_binary(i) not in prediction_false_binary):
            dont_cares.append(convert_digit_to_binary(i))
    
    if len(prediction_true_binary) == 0:
        print("only false")
        return "F" #This should just return false.
    elif len(prediction_false_binary) == 0:
        print("only true")
        return "T"
    min_terms = find_minterms(prediction_true_binary, dont_cares)
    return(min_terms)




def arg_min_ta(valid_X, valid_Y, valid_labels,model_ai:CNN):
    """
    Given traning data and ai model finds examples to show to the user

    Uses QuineMcCluskey as minimzation technique.
    """
    valid_labels = process_labels(valid_labels)

    all_data_zip = []
    true_data_zip = []
    false_data_zip = []
    for i in range(len(valid_labels)):
        all_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))

        if valid_Y[i][0] == 1:
            false_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))
        else:
            true_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))
    sub_sets_attempts = 1000
    sample_size = 4

    min_picks = []
    min_score = float("inf")

    print("Searching for best sample to display...")
    for i in  range(sub_sets_attempts):
        print(f"{i+1}/{sub_sets_attempts}")

        # we take total 4 picks, >1 true, >1 false.
        # if we don't the result will always be either just true or just false.
        picks = []
        assert len(true_data_zip) != 0
        picks.append(choice(true_data_zip)) # one true
        assert len(false_data_zip) != 0
        picks.append(choice(false_data_zip))# one false
        picks.append(choice(all_data_zip)) #All random 
        picks.append(choice(all_data_zip)) #All random
        
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

        model_complexity = complexity_of_model(boolExpr)

        image_complexity = complexity_of_image(labels_picked)

        picks_score = compatibility*100 + model_complexity + image_complexity
        print(f"bool:{booleanExprStr}\ncompatibility: {compatibility}\nmodel_complex: {model_complexity}\n" 
                                + f"image_complexiy: {image_complexity}\npick_score: {picks_score}")
        if picks_score < min_score:
            print(f"new best set!!!\nLabels: {labels_picked}, predictions: {predictions}")
            min_score = picks_score
            min_picks = picks
    
    return min_picks


        





if __name__ == '__main__':
    test()



        

