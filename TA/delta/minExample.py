from TA.delta.IDelta import IDelta


class MinExample(IDelta):
    "This is sort of gimmicky, but will give us something to compare to."

    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        return min([len(example) for example in teaching_set])

    def __repr__(self):
        return "MinExample"
