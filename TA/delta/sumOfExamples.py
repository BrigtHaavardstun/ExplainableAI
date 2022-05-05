from TA.delta.IDelta import IDelta


class SumOfExamples(IDelta):
    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        score = sum([len(label) for label in labels])
        #score += sum([0.1 for label in labels if len(label) == 0])
        return score

    def __repr__(self):
        return "SumOfExamples"
