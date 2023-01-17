from random import choice, randint
import random
from TA.subset.ISubset import ISubsetSelector
from TA.subset.random_select import RandomSelect

from utils.global_props import get_sample_size


class RandomWHashSelect(ISubsetSelector):
    def __init__(self) -> None:
        super().__init__()
        self.randomSelector = RandomSelect()
        self.tried = []
        self.wait_factor = 2

    def __repr__(self):
        return "RandomWHashSelect"

    def load(self, all_data_zip, true_data_zip, false_data_zip):
        self.randomSelector.load(all_data_zip, true_data_zip, false_data_zip)
        self.tried = []  # Reset

    def get_next_subset(self, previous_score, previous_subset):
        while True:
            pick = self.randomSelector.get_next_subset(
                previous_score, previous_subset)

            choosen_labels = sorted([str(pL+str(pY)) for pX, pY, pL in pick])

            if choosen_labels in self.tried:
                # To avoid infinite spin
                if random.randint(0, 10000) < self.wait_factor:
                    self.wait_factor *= 2
                    pick.sort(key=lambda x: x[2])
                    return pick
                continue
            self.wait_factor = max(self.wait_factor//3, 2)  # never go below 2.
            self.tried.append(choosen_labels)
            pick.sort(key=lambda x: x[2])
            return pick
