"""
This boolean forest will predict using a lexiograpical ordering of the BooleanExpressions.
"""
from LM.boolean.BoolExpression import BooleanExpression, is_smaller_then_current
from LM.boolean.IBoolForest import IBoolForest

class LexioForest(IBoolForest):
    def __init__(self,list_of_BooleanExpressions:list):
        self.list_of_BooleanExpressions = list_of_BooleanExpressions
        self.top_expression = self._find_minimal_expression()

    def _find_minimal_expression(self):
        min_expr = None
        for expression in self.list_of_BooleanExpressions:
            if min_expr is None:
                min_expr = expression
            elif self.smaller(expression, min_expr):
                min_expr = expression
        
        print(f"min_bool: {min_expr.get_expression()}")
        return min_expr


    def smaller(self,other, current):
        if len(other.expression_ors) < len(current.expression_ors):
            return True
        elif len(other.expression_ors) > len(current.expression_ors):
            return False
        elif is_smaller_then_current(test=other.min_expression, current=current.min_expression):
            return True
        return False

    def get_forest(self):
        return "{" + "-".join([boolExpr.get_expression() for boolExpr in self.list_of_BooleanExpressions]) + "}"

    def get_min_expression(self):
        return self.top_expression.get_expression()


    def evaluate(self,A,B,C,D):
        "Evaluates a boolean forest, e.g. one or more BooleanExpressions given som prioritation"
        return self.top_expression.evaluate(A,B,C,D)
        