from TA.delta.IDelta  import IDelta
class SquaredSum(IDelta):
        "This is also somwhat gimmicky. However, it will favore (2,2) over (3,1), so mitigates huge and some extrem small"
        def get_complexity_of_subset(self, labels):
            """Compute the complexity of the examples given"""
            return sum([len(label)**2 for label in labels])

        def __repr__(self):
            return "SquaredSum"
    