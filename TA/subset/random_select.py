from random import choice
from TA.subset.ISubset import ISubsetSelector
from utils.global_props import SAMPLE_SIZE


class RandomSelect(ISubsetSelector):
    def __repr__(self):
        return "RandomSelect"

    def load(self, all_data_zip, true_data_zip, false_data_zip) -> ISubsetSelector:
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip
        self.sample_size = SAMPLE_SIZE

    def get_next_subset(self, previus_score, previus_subset):
        picks = []
        assert len(self.true_data_zip) != 0
        picks.append(choice(self.true_data_zip))  # one true
        assert len(self.false_data_zip) != 0
        picks.append(choice(self.false_data_zip))  # one false
        while(len(picks) < self.sample_size):
            to_add = choice(self.all_data_zip)
            aX, aY, aL = to_add
            found_match = False
            for pX, pY, pL in picks:
                if (pX == aX).all() and (pY == aY).all() and pL == aL:
                    found_match = True
                    break
            if found_match:
                continue

            picks.append(to_add)
        return picks
