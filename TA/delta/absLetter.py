from TA.delta.IDelta import IDelta
from utils.global_props import ALL_LETTERS


class AbsLetter(IDelta):
    """
    The complexity of showing all letters might be low, beacuse we could just as well show only the false values.
    """

    def get_complexity_of_subset(self, labels):
        """Compute the complexity of the examples given"""
        return min(sum([len(label) for label in labels]), sum([len(ALL_LETTERS)-len(label) for label in labels]))

    def __repr__(self):
        return "AbsLetter"
