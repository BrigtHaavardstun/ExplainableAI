from random import choice
from TA.subset.ISubset import ISubsetSelector
from utils.global_props import get_sample_size
from utils.common import get_all_letter_combinations
import numpy as np


class RandomSelect(ISubsetSelector):
    def __init__(self):
        super(RandomSelect, self).__init__()

    def __repr__(self):
        return "RandomSelect"

    def load(self, all_data_zip, true_data_zip, false_data_zip) -> ISubsetSelector:
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip

        self.label_to_data = self.initzatie()

    def initzatie(self):
        data_dict = {}
        for l in get_all_letter_combinations():
            data_dict[l] = []
        for pX, pY, pL in self.all_data_zip:
            data_dict[pL].append((pX, pY, pL))
        return data_dict

    def get_next_subset(self, previous_score, previous_subset):
        picks = []
        possiblilities = get_all_letter_combinations()
        while(len(picks) < get_sample_size()):
            label = choice(possiblilities)
            possiblilities.remove(label)

            to_add = choice(self.label_to_data[label])
            picks.append(to_add)
        picks.sort(key=lambda x: x[2])
        return picks
