from PIL import Image
from random import choice
from utils.global_props import get_e, get_B, get_mu
from utils.global_props import set_sample_attempts, set_sample_size, set_data_size, get_data_size, get_all_letters, score_function
from utils.save_data import save_data, clean_all_csv_files, save_best_run
from utils.dataset import load_dataset, sub_sample
from TA.Lambda.mean_square_error import MSE
from TA.Lambda.ILambda import ILambda
from TA.delta.squaredSum import SquaredSum
from TA.delta.IDelta import IDelta
from TA.subset.try_all import TryAll
from TA.subset.ISubset import ISubsetSelector
from models.trainModel import run as generate_new_model
from models.trainModel import load_model
from models.abstract_model import AbstractModel
from models.CNN.CNNmodel import CNN
from TA.TA import arg_min_ta


def train_model(model_to_train: AbstractModel = CNN, model_name: str = "Defualt", verbose: bool = False, traning_set_size=float("inf")):
    generate_new_model(constructor=model_to_train,
                       name=model_name, save=True, verbose=verbose, data_size_cap=traning_set_size)


def run_system(model: AbstractModel, set_selector: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda,
               valid_X, valid_labels, verbose=False, save=True, with_data_valid=False, name="Standar", over_all_best_score=float("inf")):
    # get data TODO: This should be the same.

    best = arg_min_ta(verbose=verbose, valid_X=valid_X, valid_labels=valid_labels, ai_model=model,
                      set_selector=set_selector,
                      delta=delta,
                      compatibility_evalutator=compatibility_evalutator, over_all_best_score=over_all_best_score
                      )
    return best


def display_result(picks, compatibility, complexity, ai_model):
    print(
        f"Overall score: {compatibility*100}, compatibility: {compatibility}, complexity: {complexity}")
    for (example_X, example_Y, example_label) in picks:
        img = Image.fromarray(example_X)
        prediction = ai_model.predict(example_X)
        title = ""
        if prediction[0] == 1:
            title = "False"
        else:
            title = "True"
        img.show(title=title)
        print(
            f"label: '{example_label}', Correct: {example_Y}, predicted: {prediction}")


def main_run_system(re_train=True, clean_data=True, traning_set_size=float("inf"), model_name_NN="NN v1.1", model_name_CNN="CNN v1.1",
                    deltas=[SquaredSum()], ai_models=[], subset_selectors=[TryAll()], differentNrAttempts=[], verbose=True):

    if re_train:
        train_model(model_to_train=CNN, model_name=model_name_CNN,
                    traning_set_size=traning_set_size)

    lambdas = [MSE()]

    if differentNrAttempts == []:
        differentNrAttempts = [10, 25, 50, 75, 100,
                               200, 500, 1000, 2000, 5000, 10000]
    differentSampleSize = list(range(1, 2**len(get_all_letters())+1))
    if ai_models == []:
        # , load_model(model_name_NN)]
        ai_models = [load_model(model_name_CNN)]

    valid_X, valid_Y, valid_labels = load_dataset()

    # Make save files clean
    if clean_data:
        clean_all_csv_files()

    best_score = float('inf')
    theoretical_best = True
    over_all_best = None

    for compatibility_evalutator in lambdas:
        for delta in deltas:
            for ai_model in ai_models:
                for subset_selector in subset_selectors:
                    for attemps in differentNrAttempts:
                        set_sample_attempts(attemps)

                        for size in differentSampleSize:
                            set_sample_size(size)

                            if verbose:
                                print(
                                    f"model: {ai_model}\n" +
                                    f"subset_selector: {subset_selector}\n" +
                                    f"compatibility_evalutator: {compatibility_evalutator}\n" +
                                    f"delta: {delta}\n" +
                                    f"attemps: {attemps}"

                                )
                            best_teaching_set = run_system(model=ai_model,
                                                           valid_X=valid_X, valid_labels=valid_labels,
                                                           set_selector=subset_selector,
                                                           delta=delta,
                                                           compatibility_evalutator=compatibility_evalutator,
                                                           verbose=False, over_all_best_score=best_score
                                                           )

                            picks, compatibility, sample_complexity, boolean_forest, predictions = best_teaching_set
                            curr_score = score_function(
                                complexity=sample_complexity, compatibility=compatibility)
                            save_data(ai_model=ai_model, boolforest=boolean_forest, picks=picks, predictions=predictions, compatibility=compatibility, complexity=sample_complexity,
                                      subset_selectors=subset_selector, delta=delta, compatibility_evalutator=compatibility_evalutator, score=curr_score)

                            if not subset_selector.all_done:
                                theoretical_best = False
                                if verbose:
                                    print(
                                        "Failed to get theoretical best on run " + str(size))
                            if best_score > curr_score or over_all_best is None:
                                best_score = curr_score
                                over_all_best = best_teaching_set

    score_func_setting = f"e:{get_e()}-B:{get_B()}-mu:{get_mu()}-"
    tag_note = f"mu:{get_mu()}-" + \
        str(ai_models[0]) + f"-theoretical{theoretical_best}"

    picks, compatibility, complexity, boolean_forest, predictions = over_all_best
    save_best_run(boolforest=boolean_forest, picks=picks, predictions=predictions,
                  compatibility=compatibility, complexity=complexity, score=best_score, tag=tag_note, post_fix="", subset_selectors=subset_selectors[0])


if __name__ == "__main__":
    different_traning_set_sizes = [50, 100,
                                   200, 500, 1000, 1500, 2000, 5000, 10000]

    for i in different_traning_set_sizes:
        main_run_system(re_train=False, clean_data=True, traning_set_size=i)
