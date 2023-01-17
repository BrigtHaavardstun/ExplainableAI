from TA.delta.IDelta import IDelta


class Cardinality(IDelta):
    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        return len(teaching_set)

    def __repr__(self):
        return "Cardinality"
