from TA.subset.ISubset import ISubsetSelector
from TA.delta.IDelta import IDelta
from TA.Lambda.ILambda import ILambda

from LM.boolean.BoolExpression import BooleanExpression
from LM.boolean.IBoolForest import IBoolForest

from models.abstract_model import AbstractModel

from utils.global_props import get_sample_attempts


def save_data(ai_model: AbstractModel, boolforest: IBoolForest, picks, predictions, compatibility: float, complexity: float, subset_selectors: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda):
    """
    Format: 
    model_name,boolforest,bool_min,subset_selectors,delta,compatibility_evalutator,sample_attemps,compatibility,complexity,label1,label2,label3,label4,prediction1,prediction2,prediction3,prediction4
    """
    labels = []
    for (x, y, label) in picks:
        labels.append(label)

    label_text = ",".join(labels)

    prediction_text = ",".join(predictions)

    text_to_save = f"\n{ai_model},{boolforest.get_forest()},{boolforest.get_min_expression()},{subset_selectors},{delta},{compatibility_evalutator},{get_sample_attempts()},{compatibility},{complexity},{label_text},{prediction_text}"

    with open(f"run_result/run_result{len(labels)}.csv", "a") as f:
        f.write(text_to_save)


def save_best_run(boolforest: IBoolForest, picks, predictions, compatibility: float, complexity: float, tag: str = "Nothing", post_fix=""):
    labels = []
    for (x, y, label) in picks:
        labels.append(label)

    label_text = "-".join(labels)

    prediction_text = "-".join(predictions)

    text_to_save = f"\n{tag},{boolforest.get_forest()},{boolforest.get_min_expression()},{get_sample_attempts()},{compatibility},{complexity},{label_text},{prediction_text}"

    with open(f"run_result/best/over_all_best{post_fix}.csv", "a") as f:
        f.write(text_to_save)


def clean_all_csv_files():
    for i in range(1, 17):
        with open(f"run_result/run_result{i}.csv", "w") as f:
            text = "model_name,boolforest,bool_min,subset_selectors,delta,compatibility_evalutator,sample_attemps,compatibility,complexity"
            for j in range(i):
                text += f",label{j}"
            for j in range(i):
                text += f",prediction{j}"
            f.write(text)

    with open(f"run_result/best/over_all_best.csv", "w") as f:
        text = "tag,boolforest,bool_min,sample_attemps,compatibility,complexity,labels,predictions"
        f.write(text)
