class BooleanExpression:
    def __init__(self,expression_str:str):
        self.expression = expression_str
        self.expression_ors = self.expression.split("+")
        self.always_true = self.expression == "T"
        self.always_false = self.expression == "F"

        #comparrisons
        self.min_expression = find_smallest_expression(self.expression_ors)
        self.negative_expression = sum([expression.count("'") for expression in self.expression_ors])

    def evaluate(self, A,B,C,D):
        #print(f"A:{A}\nB:{B}\nC:{C}\nD:{D}")
        if self.always_true:
            return True
        if self.always_false:
            return False 
        
        literals = {
            "A":A,
            "B":B,
            "C":C,
            "D":D,
        }

        for clause in self.expression_ors:
            currentClause = True
            for i,e in enumerate(clause):
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

def find_smallest_expression( expression_list):
    min_expression = None
    for expression in expression_list:
        if min_expression is None:
            min_expression = expression
        elif is_smaller_then_current(min_expression, expression):
            min_expression = expression
    return min_expression

def is_smaller_then_current(current, test):
    current_negate_count = current.count("'")
    test_negate_count = test.count("'")

    cur_size = len(current.replace("'", ""))
    test_size = len(test.replace("'", ""))

    if test_size < cur_size:
        return True
    elif test_size > cur_size:
        return False
    elif test_negate_count < current_negate_count:
        return True
    elif test_negate_count > current_negate_count:
        return False
    else:
        return sorted(test.replace("'", "")) < sorted(current.replace("'", ""))

    
            