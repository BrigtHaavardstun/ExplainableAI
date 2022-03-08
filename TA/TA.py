from LM.boolean.BoolExpression import BooleanExpression
from models.abstract_model import AbstractModel

from utils.common import remove_digit_from_labels
from utils.global_props import get_sample_attempts

from TA.subset.ISubset import ISubsetSelector
from TA.delta.IDelta import IDelta
from TA.Lambda.ILambda import ILambda

from LM.lm import run_lm


def arg_min_ta(valid_X, valid_Y, valid_labels, ai_model: AbstractModel,
               set_selector: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda,
               verbose=False):
    """
    Given traning data and ai model finds examples to show to the user
    """
    valid_labels = remove_digit_from_labels(valid_labels)

    all_data_zip = []
    true_data_zip = []
    false_data_zip = []
    for i in range(len(valid_labels)):
        all_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))

        if valid_Y[i][0] == 1:
            false_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))
        else:
            true_data_zip.append((valid_X[i], valid_Y[i], valid_labels[i]))

    sub_sets_attempts = get_sample_attempts()

    min_picks = []
    min_score = float("inf")
    complexity_best = float("inf")
    compatibility_best = float("inf")
    boolforest_best = None

    # Pick the sub_set we are testing.
    set_selector.load(all_data_zip=all_data_zip,
                      true_data_zip=true_data_zip, false_data_zip=false_data_zip)

    print("Searching for best sample to display...")
    for i in range(sub_sets_attempts):

        if verbose:
            print(f"{i+1}/{sub_sets_attempts}")

        # we take total 4 picks, >1 true, >1 false.
        # if we don't the result will always be either just true or just false.
        picks = set_selector.get_next_subset(
            previus_score=None, previus_subset=None)

        predictions = []
        labels_picked = []
        ground_truth = []
        for (x, y, label) in picks:
            predictions.append(ai_model.predict(x))
            labels_picked.append(label)
            ground_truth.append(y)

        #booleanExprStr = run_lm(labels = labels_picked, predictions = predictions)
        #boolExpr = BooleanExpression(booleanExprStr)
        boolean_forest = run_lm(labels=labels_picked, predictions=predictions)

        compatibility = compatibility_evalutator.compatibility(
            ai_model=ai_model, bool_forest=boolean_forest, valid_X=valid_X, valid_labels=valid_labels)

        sample_complexity = delta.get_complexity_of_subset(labels_picked)

        picks_score = compatibility*100 + sample_complexity
        if verbose:
            print(f"bool_forest:{boolean_forest.get_forest()}\nbool_min:{boolean_forest.get_min_expression()}\ncompatibility: {compatibility}\n"
                  + f"sample_complexity: {sample_complexity}\n"
                  + f"pick_score: {picks_score}")
        if picks_score < min_score:
            print(
                f"new best set!!!\nLabels: {labels_picked}, predictions: {predictions}")
            min_score = picks_score
            min_picks = picks
            compatibility_best = compatibility
            complexity_best = sample_complexity
            boolforest_best = boolean_forest

    return min_picks, compatibility_best, complexity_best, boolforest_best
