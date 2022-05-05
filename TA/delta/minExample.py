from TA.delta.IDelta import IDelta


class MinExample(IDelta):
    "This is sort of gimmicky, but will give us something to compare to."

    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        return min([len(label) for label in labels])

    def __repr__(self):
        return "MinExample"
