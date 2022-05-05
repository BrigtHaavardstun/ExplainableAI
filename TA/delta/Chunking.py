from TA.delta.IDelta import IDelta


class Chunking(IDelta):
    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        # return sum([(1 if len(l) <= 2 else 3) for l in labels])
        complexity = 0
        for example in labels:
            if len(example) == 0:
                complexity += 0
            elif 1 <= len(example) <= 3:
                complexity += len(example)*0.2 + 1
            else:
                complexity += len(example)*1.3 + 2
        return complexity

    def __repr__(self):
        return "Chunking"
