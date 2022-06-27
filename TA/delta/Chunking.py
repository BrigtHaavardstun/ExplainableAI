from TA.delta.IDelta import IDelta


class Chunking(IDelta):
    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        complexity = 0
        for example in teaching_set:
            if len(example) == 0:
                complexity += 0.1
            elif 1 <= len(example) <= 3:
                complexity += len(example)*0.2 + 1
            else:
                complexity += len(example)*1.3 + 2
        return complexity

    def __repr__(self):
        return "Chunking"
