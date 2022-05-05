"""
The goal of smart select is to not test combionations already tested. 
We only allow unique subset combinations.
We don't allow the letters of two instances to be the same.
"""


import random


from TA.subset.ISubset import ISubsetSelector
from TA.subset.random_select import RandomSelect

from utils.global_props import get_sample_size
from utils.common import total_combinations, get_all_permutations

from random import choice
from random import seed
from itertools import combinations


class TryAll(ISubsetSelector):
    def __init__(self):
        super().__init__()
        self.random_backup = RandomSelect()

    def __repr__(self):
        return "TryAll"

    def load(self, all_data_zip, true_data_zip, false_data_zip):
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip

        self.label_to_data_map_true = self.generate_label_to_data_map(
            true_data_zip)
        self.label_to_data_map_false = self.generate_label_to_data_map(
            false_data_zip)

        self.all_combinations = self.generate_all_possible_elements()
        self.next_to_try = 0
        self.queue_of_picks = []
        self.all_done = False

    def generate_label_to_data_map(self, data_zip):
        label_map = {}
        for pX, pY, pL in data_zip:
            if pL not in label_map:
                label_map[pL] = [(pX, pY, pL)]
            else:
                label_map[pL].append((pX, pY, pL))
        return label_map

    def generate_all_possible_elements(self):
        all_permutation = get_all_permutations()
        all_combinations = combinations(
            all_permutation, get_sample_size())
        all_combinations = list(all_combinations)
        random.shuffle(all_combinations)
        return all_combinations

    def get_from_pick_queue(self):
        temp = self.queue_of_picks[-1]
        self.queue_of_picks = self.queue_of_picks[:-1]  # Remove last pick
        temp.sort(key=lambda x: x[2])
        return temp

    def get_next_subset(self, previus_score, previus_subset):
        if len(self.queue_of_picks) > 0:
            return self.get_from_pick_queue()
        picks = []
        while True:
            # We use random as a back up.
            if self.next_to_try >= len(self.all_combinations):
                # picks = self.random_backup.get_next_subset(previus_score, previus_subset) not needed
                picks = None
                self.all_done = True
                return None  # no mor to test

            current = self.all_combinations[self.next_to_try]
            self.next_to_try += 1  # Try next set
            picks = []
            multiple_picks = []
            a_labeled_had_no_valid_mapping = False
            for pL in current:
                found_one = False
                # Currently we are only picking either a true or false, we should maybe try both?
                new_poss_picks = []

                if pL in self.label_to_data_map_true:
                    found_one = True
                    # If this is first we have to add it manually.
                    if len(multiple_picks) == 0:
                        new_poss_picks = [[self.label_to_data_map_true[pL][0]]]
                    else:
                        # For each possible combination we add this option aswell.
                        for pos_pick in multiple_picks:
                            new_poss_picks.append(
                                pos_pick + [self.label_to_data_map_true[pL][0]])

                if pL in self.label_to_data_map_false:
                    found_one = True

                    # If this is first we have to add it manually.
                    if len(multiple_picks) == 0:
                        new_poss_picks = [
                            [self.label_to_data_map_false[pL][0]]]
                    else:
                        # For each possible combination we add this option aswell.
                        for pos_pick in multiple_picks:
                            new_poss_picks.append(
                                pos_pick + [self.label_to_data_map_false[pL][0]])

                if not found_one:
                    a_labeled_had_no_valid_mapping = True
                    break
                multiple_picks = new_poss_picks

            if a_labeled_had_no_valid_mapping:
                continue

            picks = multiple_picks[0]
            self.queue_of_picks = multiple_picks[1:]
            break
        picks.sort(key=lambda x: x[2])
        return picks

    def display_hashed(self):
        with open("Output.txt", "w") as f:
            f.write("\n".join(sorted(self.tried_lables)))
