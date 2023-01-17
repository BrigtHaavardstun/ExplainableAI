from TA.delta.IDelta import IDelta


class MaxExample(IDelta):
    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        return max([len(example) for example in teaching_set])

    def __repr__(self):
        return "MaxExample"
