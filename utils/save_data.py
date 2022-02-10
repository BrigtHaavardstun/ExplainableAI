from TA.subset.ISubset import ISubsetSelector
from TA.delta.IDelta  import IDelta
from TA.Lambda.ILambda import ILambda
from LM.boolParser import BooleanExpression
from models.abstract_model import AbstractModel

def save_data(ai_model:AbstractModel, bool_expr:BooleanExpression, picks,predictions, compatibility:float, complexity:float, subset_selectors:ISubsetSelector, delta:IDelta, compatibility_evalutator:ILambda):
    """
    Format: 
    model_name,guessed_bool_expr,subset_selectors,delta,compatibility_evalutator,compatibility,complexity,label1,label2,label3,label4,prediction1,prediction2,prediction3,prediction4
    """
    labels = []
    for (x,y,label) in picks:
        labels.append(label)
    
    label_text = ",".join(labels)

    prediction_text = ",".join(predictions)
    
    text_to_save = f"{ai_model},{bool_expr.get_expression()},{subset_selectors},{delta},{compatibility_evalutator},{compatibility},{complexity},{label_text},{prediction_text}\n"
    with open("run_result/run_result.csv", "a") as f:
        f.write(text_to_save)