from LM.boolean.BoolExpression import BooleanExpression
from models.abstract_model import AbstractModel

from utils.common import remove_digit_from_labels, memoize
from utils.global_props import get_sample_attempts, get_sample_size

from TA.subset.ISubset import ISubsetSelector
from TA.delta.IDelta import IDelta
from TA.Lambda.ILambda import ILambda

from LM.lm import run_lm

from utils.global_props import score_function


def split_data_in_true_false(valid_X, valid_labels, ai_model: AbstractModel):
    all_data_zip = []

    predicted_true_data_zip = []
    predicted_false_data_zip = []
    for i in range(len(valid_labels)):
        # one hot encoding
        prediction = [0, 0]
        prediction[ai_model.predict(valid_X[i])[0]] = 1
        if prediction[0] == 1:
            predicted_false_data_zip.append(
                (valid_X[i], prediction, valid_labels[i]))
        else:
            predicted_true_data_zip.append(
                (valid_X[i], prediction, valid_labels[i]))
        all_data_zip.append((valid_X[i], prediction, valid_labels[i]))
    return all_data_zip, predicted_true_data_zip, predicted_false_data_zip


split_data_in_true_false_w_memoization = memoize(split_data_in_true_false)


def arg_min_ta(valid_X, valid_labels, ai_model: AbstractModel,
               set_selector: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda,
               verbose=False, over_all_best_score=float("inf")):
    """
    Given traning data and ai model finds examples to show to the user
    """
    valid_labels = remove_digit_from_labels(valid_labels)

    all_data_zip, predicted_true_data_zip, predicted_false_data_zip = split_data_in_true_false(
        valid_X, valid_labels, ai_model)

    sub_sets_attempts = get_sample_attempts()

    min_score = float("inf")

    best = None
    # Pick the sub_set we are testing.
    print("Start load..")
    set_selector.load(all_data_zip=all_data_zip,
                      true_data_zip=predicted_true_data_zip, false_data_zip=predicted_false_data_zip, delta=delta)
    print("end load")
    prev_delta = float("-inf")
    for i in range(sub_sets_attempts):
        if prev_delta > over_all_best_score:
            print("impossible to find better score. Early break")
            break
        if verbose:
            print(f"{i+1}/{sub_sets_attempts}")

        # we take total 4 picks, >1 true, >1 false.
        # if we don't the result will always be either just true or just false.
        picks = set_selector.get_next_subset(
            previous_score=None, previous_subset=None)

        # No more to try. So we end early
        if picks == None:
            print("early return at", i, get_sample_size())
            break
        predictions = []
        labels_picked = []
        ground_truth = []
        for (x, y, label) in picks:
            predictions.append(ai_model.predict(x))
            labels_picked.append(label)
            ground_truth.append(y)

        boolean_forest = run_lm(labels=labels_picked, predictions=predictions)

        compatibility = compatibility_evalutator.compatibility(
            ai_model=ai_model, bool_forest=boolean_forest, valid_X=valid_X, valid_labels=valid_labels)
        sample_complexity = delta.get_complexity_of_subset(labels_picked)
        prev_delta = sample_complexity
        picks_score = score_function(
            compatibility=compatibility, complexity=sample_complexity)
        if verbose:
            print(f"bool_forest:{boolean_forest.get_forest()}\nbool_min:{boolean_forest.get_min_expression()}\ncompatibility: {compatibility}\n"
                  + f"sample_complexity: {sample_complexity}\n"
                  + f"pick_score: {picks_score}")
        if picks_score < min_score:
            min_score = picks_score
            best = [picks, compatibility, sample_complexity,
                    boolean_forest, predictions]
            if over_all_best_score > min_score:
                over_all_best_score = min_score
    return best
