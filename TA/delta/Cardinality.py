from TA.delta.IDelta import IDelta


class Cardinality(IDelta):
    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        return len(labels)

    def __repr__(self):
        return "Cardinality"
