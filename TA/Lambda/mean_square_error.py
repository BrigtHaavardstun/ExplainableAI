from models.abstract_model import AbstractModel
from LM.boolean.IBoolForest import IBoolForest
from TA.Lambda.ILambda import ILambda
from utils.common import get_all_letter_combinations
from utils.global_props import get_all_letters


class MSE(ILambda):
    def __init__(self):
        self.ai_prob_map = {}
        self.boolexpr_prob_map = {}

    def __repr__(self):
        return "Mean_Square_Error"

    def compatibility(self, ai_model: AbstractModel, bool_forest: IBoolForest, valid_X, valid_labels):
        """
        Returns a value describing the compatibility between tha ai_model and boolean expression.
        Low score is better.
        """
        """
        For model_ai: Itterate over all(?) validation data. 
        Keep a score over how many true and false each literal combination gives.

        For booleanExpr: Evaluate all possible combinations.

       
        """
        if (ai_model, bool_forest.get_forest()) in self.boolexpr_prob_map:
            return self.boolexpr_prob_map[(ai_model, bool_forest.get_forest())]

        all_labels = get_all_letter_combinations()

        # Maps holding score for each label combination.
        """
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
        """
        count_map_boolexpr = {}

        for label in all_labels:
            count_map_boolexpr[label] = [0, 0]

        # Handling boolean expression
        for label in all_labels:
            bool_dict = {}
            for l in get_all_letters():
                bool_dict[l] = l in label
            evaluation = bool_forest.evaluate(bool_dict)
            if evaluation:
                count_map_boolexpr[label][1] = 1
            else:
                count_map_boolexpr[label][0] = 1

        # Convert maps counting nr_false and nr_true into probabilities of true.
        # P(T|label) = nrTrue/(nrTrue +nrFalse)

        probaility_map_boolexpr = {}
        for label in all_labels:
            # bool expr
            false_count, true_count = count_map_boolexpr[label]
            probaility_map_boolexpr[label] = true_count / \
                (false_count+true_count)

        # Using mean square error. sum over all labels, (probAI - probBoolXpr)^2,
        probaility_map_ai = self._get_probaility_map_ai(
            ai_model=ai_model, valid_X=valid_X, valid_labels=valid_labels)
        mean_square_error = 0
        for label in all_labels:
            mean_square_error += (probaility_map_ai[label] -
                                  probaility_map_boolexpr[label])**2
        self.boolexpr_prob_map[(
            ai_model, bool_forest.get_forest())] = mean_square_error
        return mean_square_error

    def _get_probaility_map_ai(self, ai_model, valid_X, valid_labels):
        """
        Calulates the probabilities a given AI have for predicting true or false,
        given a (random) image contaning some given litterals.
        """
        # Memoization. If we know what this ai will give, we don't change.
        if ai_model in self.ai_prob_map:
            return self.ai_prob_map[ai_model]
        all_labels = get_all_letter_combinations()
        count_map_model_ai = {}
        for label in all_labels:
            count_map_model_ai[label] = [0, 0]

        # handling ai model
        for label, data in zip(valid_labels, valid_X):
            prediction = ai_model.predict(data)
            if prediction == [1, 0]:
                count_map_model_ai[label][0] += 1
            else:
                count_map_model_ai[label][1] += 1

        prob_map_ai = {}
        for label in all_labels:
            # ai model
            false_count, true_count = count_map_model_ai[label]
            assert false_count + \
                true_count != 0, f"You didn't give the ai label {label}, hence we can't make the prediction"
            prob_map_ai[label] = true_count/(false_count+true_count)
        self.ai_prob_map[ai_model] = prob_map_ai  # memoization.
        return prob_map_ai
