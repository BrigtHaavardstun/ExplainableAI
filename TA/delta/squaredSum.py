from TA.delta.IDelta import IDelta


class SquaredSum(IDelta):
    "This is also somwhat gimmicky. However, it will favore (2,2) over (3,1), so mitigates huge and some extrem small"

    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        score = sum([(len(label))**2 for label in labels])
        #score += sum([0.1 for label in labels if len(label) == 0])
        return score

    def __repr__(self):
        return "SquaredSum"
