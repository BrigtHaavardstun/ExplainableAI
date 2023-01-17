from TA.delta.IDelta import IDelta
from utils.global_props import get_all_letters


class AbsExample(IDelta):
    """
    The complexity of showing all letters might be low, beacuse we could just as well show only the false values.
    """

    def get_complexity_of_subset(self, teaching_set):
        """Compute the complexity of the examples given"""
        score = sum([min(len(example), (len(get_all_letters())-len(example)))
                    for example in teaching_set])
        score += sum([1.1 for example in teaching_set if len(example) == 0])
        return score

    def __repr__(self):
        return "AbsExample"
