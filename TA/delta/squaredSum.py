from TA.delta.IDelta import IDelta


class SquaredSum(IDelta):
    "This is also somwhat gimmicky. However, it will favore (2,2) over (3,1), so mitigates huge and some extrem small"

    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        score = sum([(len(example))**2 for example in teaching_set])
        score += sum([0.1 for example in teaching_set if len(example) == 0])
        return score

    def __repr__(self):
        return "SquaredSum"
