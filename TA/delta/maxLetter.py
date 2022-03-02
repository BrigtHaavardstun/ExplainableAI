from TA.delta.IDelta import IDelta


class MaxLetter(IDelta):
    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        return max([len(label) for label in labels])

    def __repr__(self):
        return "MaxLetter"
