from models.abstract_model import AbstractModel
from LM.boolParser import BooleanExpression

class ILambda:
    def compatibility(self, ai_model:AbstractModel, boolean_expression:BooleanExpression, valid_X, valid_labels):
        """
        Returns a value describing the compatibility between tha ai_model and boolean expression.
        Low score is better.
        """
        pass


