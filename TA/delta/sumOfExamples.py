from TA.delta.IDelta import IDelta


class SumOfExamples(IDelta):
    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        score = sum([len(example) for example in teaching_set])
        score += sum([0.1 for example in teaching_set if len(example) == 0])
        return score

    def __repr__(self):
        return "SumOfExamples"
