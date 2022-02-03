class BooleanExpression:
    def __init__(self,expression_str:str):
        self.expression = expression_str
        self.expression_ors = self.expression.split(" + ")
    
    def evaluate(self, A,B,C,D):
        #print(f"A:{A}\nB:{B}\nC:{C}\nD:{D}")
        
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
            