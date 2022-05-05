from TA.delta.IDelta import IDelta
from utils.global_props import get_all_letters


class AbsExample(IDelta):
    """
    The complexity of showing all letters might be low, beacuse we could just as well show only the false values.
    """

    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        score = sum([min(len(label), (len(get_all_letters())-len(label)))
                    for label in labels])
        #score += sum([0.1 for label in labels if len(label) == 0])
        return score

    def __repr__(self):
        return "AbsExample"
