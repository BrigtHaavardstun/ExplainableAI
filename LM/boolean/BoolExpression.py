import functools
from utils.global_props import get_all_letters


class BooleanExpression:
    def __init__(self, expression_str: str):
        self.expression = expression_str
        self.expression_ors = sort_expressions(self.expression.split("+"))
        self.always_true = self.expression == "T"
        self.always_false = self.expression == "F"

        # comparrisons
        self.min_expression = self.expression_ors[0]
        self.negative_expression = sum(
            [expression.count("'") for expression in self.expression_ors])

    def evaluate(self, bool_dict):
        # print(f"A:{A}\nB:{B}\nC:{C}\nD:{D}")
        if self.always_true:
            return True
        if self.always_false:
            return False

        literals = {}
        for l in get_all_letters():
            literals[l] = bool_dict[l]

        for clause in self.expression_ors:
            currentClause = True
            for i, e in enumerate(clause):
                if e == "'":
                    continue
                if i + 1 < len(clause) and clause[i + 1] == "'":
                    if literals[e] == False:
                        continue
                    else:
                        currentClause = False
                        break
                else:
                    if literals[e] == True:
                        continue
                    else:
                        currentClause = False
                        break

            if currentClause:
                return True
        return False

    def get_expression(self):
        return self.expression


def sort_expressions(expression_list):
    sorted_list = sorted(
        expression_list, key=functools.cmp_to_key(cmpr_clauses))
    return sorted_list


def cmpr_clauses(current, other):
    current_negate_count = current.count("'")
    other_negate_count = other.count("'")

    cur_size = len(current.replace("'", ""))
    other_size = len(other.replace("'", ""))

    if other_size < cur_size:
        return 1
    elif other_size > cur_size:
        return -1
    elif other_negate_count < current_negate_count:
        return 1
    elif other_negate_count > current_negate_count:
        return -1
    else:
        # convert negeated letters
        new_other = ""
        for i in range(len(other)):
            to_add = other[i]
            if i < len(other)-1 and other[i] == "'":
                to_add = to_add.lower()
        new_current = ""
        for i in range(len(current)):
            to_add = current[i]
            if i < len(current)-1 and current[i] == "'":
                to_add = to_add.lower()

        if sorted(new_other) < sorted(new_current):
            return 1
        elif sorted(new_other) > sorted(new_current):
            return -1
        else:
            return 0
