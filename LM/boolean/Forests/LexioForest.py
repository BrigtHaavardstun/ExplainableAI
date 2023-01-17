"""
This boolean forest will predict using a lexiograpical ordering of the BooleanExpressions.
"""
from LM.boolean.BoolExpression import cmpr_clauses
from LM.boolean.IBoolForest import IBoolForest
import functools


class LexioForest(IBoolForest):
    def __init__(self, list_of_BooleanExpressions: list):

        self.list_of_BooleanExpressions = list_of_BooleanExpressions
        self.top_expression = self._find_minimal_expression()

    def _find_minimal_expression(self):
        min_expr = None
        for expression in self.list_of_BooleanExpressions:
            if min_expr is None:
                min_expr = expression
            elif not self.smaller_or_equal(current=min_expr, other=expression):
                min_expr = expression

        return min_expr

    def smaller_or_equal(self, current, other):
        # Swapped negations and size order
        curr_negations = sum([clause.count("'")
                             for clause in current.expression_ors])
        other_negations = sum([clause.count("'")
                              for clause in other.expression_ors])

        if curr_negations < other_negations:
            return True
        elif other_negations < curr_negations:
            return False

        if len(current.expression_ors) < len(other.expression_ors):
            return True
        elif len(current.expression_ors) > len(other.expression_ors):
            return False

        

        for currBolExpr, otherBolExpr in zip(current.expression_ors, other.expression_ors):
            cmp = cmpr_clauses(currBolExpr, otherBolExpr)
            if cmp > 0:
                return False
            elif cmp < 0:
                return True
        return True

    def get_forest(self):
        return "{" + "-".join([boolExpr.get_expression() for boolExpr in self.list_of_BooleanExpressions]) + "}"

    def get_min_expression(self):
        return self.top_expression.get_expression()

    def evaluate(self, bool_dict):
        "Evaluates a boolean forest, e.g. one or more BooleanExpressions given som prioritation"
        return self.top_expression.evaluate(bool_dict)
