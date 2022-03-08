from models.trainModel import run as generate_new_model
from models.trainModel import load_model
from models.abstract_model import AbstractModel
from models.CNN.CNNmodel import CNN
from models.NN.NNmodel import NN

from TA.TA import arg_min_ta

from TA.subset.ISubset import ISubsetSelector
from TA.subset.random_select import RandomSelect
from TA.subset.smart_select import SmartSelect

from TA.delta.IDelta import IDelta
from TA.delta.sumOfLetters import SumOfLetters
from TA.delta.maxLetter import MaxLetter
from TA.delta.minLetter import MinLetter
from TA.delta.squaredSum import SquaredSum
from TA.delta.absLetter import AbsLetter

from TA.Lambda.ILambda import ILambda
from TA.Lambda.mean_square_error import MSE

from utils.dataset import load_dataset, sub_sample
from utils.save_data import save_data
from utils.common import one_hot_to_number
from utils.global_props import set_sample_attempts, DATA_SET_SIZE


from PIL import Image


def train_model(model_to_train: AbstractModel = CNN, model_name: str = "Defualt", verbose: bool = False):
    generate_new_model(constructor=model_to_train,
                       name=model_name, save=True, verbose=verbose)


def run_system(model: AbstractModel, set_selector: ISubsetSelector, delta: IDelta, compatibility_evalutator: ILambda,
               valid_X, valid_Y, valid_labels, verbose=False, save=True, with_data_valid=False, name="Standar"):
    # get data TODO: This should be the same.

    picks, compatibility, complexity, boolforest_best = arg_min_ta(verbose=verbose, valid_X=valid_X, valid_Y=valid_Y, valid_labels=valid_labels, ai_model=model,
                                                                   set_selector=set_selector,
                                                                   delta=delta,
                                                                   compatibility_evalutator=compatibility_evalutator
                                                                   )
    predictions = [str(one_hot_to_number(model.predict(x)))
                   for x, y, label in picks]
    #display_result(picks=picks, compatibility=compatibility, complexity=complexity, ai_model=model)
    save_data(ai_model=model, boolforest=boolforest_best, picks=picks, predictions=predictions, compatibility=compatibility, complexity=complexity,
              subset_selectors=set_selector, delta=delta, compatibility_evalutator=compatibility_evalutator)


def display_result(picks, compatibility, complexity, ai_model):
    print(
        f"Overall score: {compatibility*100}, compatibility: {compatibility}, complexity: {complexity}")
    for (example_X, example_Y, example_label) in picks:
        Image.fromarray(example_X).show()
        prediction = ai_model.predict(example_X)
        print(
            f"label: '{example_label}', Correct: {example_Y}, predicted: {prediction}")


def main_run_system(re_train=True):
    model_name_CNN = "CNN v1.1"
    if re_train:
        train_model(model_to_train=CNN, model_name=model_name_CNN)

    model_name_NN = "NN v1.1"
    if re_train:
        train_model(model_to_train=NN, model_name=model_name_NN)

    subset_selectors = [SmartSelect(), RandomSelect()]
    # , MinLetter(),SquaredSum(), MaxLetter()]
    deltas = [AbsLetter(), SumOfLetters(), MinLetter(),
              SquaredSum(), MaxLetter()]
    lambdas = [MSE()]
    #
    differentAttempts = [10, 50, 75, 100, 200, 500, 750, 100, 1500, 2000, 2500]
    ai_models = [load_model(model_name_CNN), load_model(model_name_NN)]

    valid_X, valid_Y, valid_labels = load_dataset()
    valid_X, valid_Y, valid_labels = sub_sample(
        valid_X, valid_Y, valid_labels, 150)

    for subset_selector in subset_selectors:
        for compatibility_evalutator in lambdas:
            for delta in deltas:
                for ai_model in ai_models:
                    for size in differentAttempts:
                        # set global attempts to size.
                        for i in range(3):
                            # we do three runs on each to get the average
                            # calulated afterwards
                            set_sample_attempts(size)
                            print(
                                f"model: {ai_model}\n" +
                                f"subset_selector: {subset_selector}\n" +
                                f"compatibility_evalutator: {compatibility_evalutator}\n" +
                                f"delta: {delta}\n" +
                                f"attemps: {size}"

                            )
                            run_system(model=ai_model,
                                       valid_X=valid_X, valid_Y=valid_Y, valid_labels=valid_labels,
                                       set_selector=subset_selector,
                                       delta=delta,
                                       compatibility_evalutator=compatibility_evalutator,
                                       verbose=False
                                       )


if __name__ == "__main__":
    main_run_system(re_train=False)
