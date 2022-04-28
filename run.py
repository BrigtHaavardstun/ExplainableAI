from models.trainModel import run as generate_new_model
from models.trainModel import load_model
from models.abstract_model import AbstractModel
from models.CNN.CNNmodel import CNN
from models.NN.NNmodel import NN

from TA.TA import arg_min_ta

from TA.subset.ISubset import ISubsetSelector
from TA.subset.random_select import RandomSelect
from TA.subset.smart_select import SmartSelect
from TA.subset.try_all import TryAll
from TA.subset.random_w_hash import RandomWHashSelect

from TA.delta.IDelta import IDelta
from TA.delta.sumOfLetters import SumOfLetters
from TA.delta.maxLetter import MaxLetter
from TA.delta.minLetter import MinLetter
from TA.delta.squaredSum import SquaredSum
from TA.delta.absLetter import AbsLetter
from TA.delta.Cardinality import Cardinality

from TA.Lambda.ILambda import ILambda
from TA.Lambda.mean_square_error import MSE

from utils.dataset import load_dataset, sub_sample
from utils.save_data import save_data, clean_all_csv_files, save_best_run
from utils.common import one_hot_to_number
from utils.global_props import set_sample_attempts, set_sample_size, set_data_size, get_data_size


from PIL import Image


def train_model(model_to_train: AbstractModel = CNN, model_name: str = "Defualt", verbose: bool = False, traning_set_size=float("inf")):
    generate_new_model(constructor=model_to_train,
                       name=model_name, save=True, verbose=verbose, data_size_cap=traning_set_size)


def run_system(model: AbstractModel, set_selector: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda,
               valid_X, valid_Y, valid_labels, verbose=False, save=True, with_data_valid=False, name="Standar"):
    # get data TODO: This should be the same.

    picks, compatibility, complexity, boolforest, predictions = arg_min_ta(verbose=verbose, valid_X=valid_X, valid_Y=valid_Y, valid_labels=valid_labels, ai_model=model,
                                                                           set_selector=set_selector,
                                                                           delta=delta,
                                                                           compatibility_evalutator=compatibility_evalutator
                                                                           )
    predictions = [str(one_hot_to_number(model.predict(x)))
                   for x, y, label in picks]
    # display_result(picks=picks, compatibility=compatibility, complexity=complexity, ai_model=model)
    save_data(ai_model=model, boolforest=boolforest, picks=picks, predictions=predictions, compatibility=compatibility, complexity=complexity,
              subset_selectors=set_selector, delta=delta, compatibility_evalutator=compatibility_evalutator)

    return picks, compatibility, complexity, boolforest, predictions


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


def main_run_system(re_train=True, clean_data=True, traning_set_size=float("inf")):
    model_name_CNN = "CNN v1.1"
    if re_train:
        train_model(model_to_train=CNN, model_name=model_name_CNN,
                    traning_set_size=traning_set_size)

    model_name_NN = "NN v1.1"
    if re_train:
        train_model(model_to_train=NN, model_name=model_name_NN,
                    traning_set_size=traning_set_size)

    subset_selectors = [TryAll()]  # ] RandomSelect(), RandomWHashSelect()]
    # , MinLetter(),SquaredSum(), MaxLetter()]
    deltas = [SquaredSum()]  # , Cardinality()]  # ,
    # SquaredSum()]
    lambdas = [MSE()]
    #
    differentAttempts = [50000]
    differentSampleSize = [1, 2, 3, 4, 5, 6,
                           7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    ai_models = [load_model(model_name_CNN)]  # , load_model(model_name_NN)]

    print("Starting to load dataset....")
    valid_X, valid_Y, valid_labels = load_dataset()
    print("Loaded dataset!")
    valid_X, valid_Y, valid_labels = sub_sample(
        valid_X, valid_Y, valid_labels, min(10000, get_data_size()))

    # Make save files clean
    if clean_data:
        clean_all_csv_files()

    picks_best = None
    compatibility_best = float('inf')
    complexity_best = float('inf')
    boolforest_best = None
    predictions_best = []
    theoretical_best = True

    for compatibility_evalutator in lambdas:
        for delta in deltas:
            for ai_model in ai_models:
                for attemps in differentAttempts:
                    # set global attempts to size.
                    for count in differentSampleSize:
                        set_sample_size(count)
                        for subset_selector in subset_selectors:
                            for i in range(1):
                                # we do three runs on each to get the average
                                # calulated afterwards
                                set_sample_attempts(attemps)
                                print(
                                    f"model: {ai_model}\n" +
                                    f"subset_selector: {subset_selector}\n" +
                                    f"compatibility_evalutator: {compatibility_evalutator}\n" +
                                    f"delta: {delta}\n" +
                                    f"attemps: {attemps}"

                                )
                                picks, compatibility, complexity, boolforest, predictions = run_system(model=ai_model,
                                                                                                       valid_X=valid_X, valid_Y=valid_Y, valid_labels=valid_labels,
                                                                                                       set_selector=subset_selector,
                                                                                                       delta=delta,
                                                                                                       compatibility_evalutator=compatibility_evalutator,
                                                                                                       verbose=False,
                                                                                                       )
                                if not subset_selector.all_done:
                                    theoretical_best = False
                                    print(
                                        "Failed to get theoretical best on run " + str(count))
                                if compatibility < compatibility_best or (compatibility == compatibility_best and complexity < complexity_best):
                                    compatibility_best = compatibility
                                    complexity_best = complexity
                                    picks_best = picks
                                    boolforest_best = boolforest
                                    predictions_best = predictions
    tag_note = f"{traning_set_size}-theoretical{theoretical_best}"
    # display_result(picks_best, compatibility_best, complexity_best, ai_models[0])
    save_best_run(boolforest=boolforest_best, picks=picks_best, predictions=predictions_best,
                  compatibility=compatibility_best, complexity=complexity_best, tag=tag_note, post_fix="")


if __name__ == "__main__":
    import subprocess
    import fill_dataset
    # subprocess.call(['sh', './clean_all.sh'])
    # data_size = 100000
    # set_data_size(data_size)
    # fill_dataset.main(fixedSquare=True, rotation=True)
    different_traning_set_sizes = [50, 100,
                                   200, 500, 1000, 1500, 2000, 5000, 10000]

    for i in different_traning_set_sizes:
        main_run_system(re_train=False, clean_data=True, traning_set_size=i)
