from models.abstract_model import AbstractModel
from LM.boolean.IBoolForest import IBoolForest


class ILambda:
    def compatibility(self, ai_model: AbstractModel, bool_forest: IBoolForest, valid_X, valid_labels):
        """
        Returns a value describing the compatibility between tha ai_model and boolean expression.
        Low score is better.
        """
        pass

    def get_theoreticaly_lowest_lambda(self, ai_model: AbstractModel,valid_X, valid_labels) -> float:
        """Find the theoretical_best lambda score"""
        pass