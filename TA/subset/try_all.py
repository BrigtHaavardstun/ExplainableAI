"""
The goal of smart select is to not test combionations already tested. 
We only allow unique subset combinations.
We don't allow the letters of two instances to be the same.
"""


import random


from TA.subset.ISubset import ISubsetSelector
from TA.subset.random_select import RandomSelect

from TA.delta.IDelta import IDelta

from utils.global_props import get_sample_size
from utils.common import total_combinations, get_all_letter_combinations

from random import choice
from random import seed
from itertools import combinations


class TryAll(ISubsetSelector):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "TryAll"

    def load(self, all_data_zip, true_data_zip, false_data_zip, delta: IDelta):
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip

        self.delta = delta

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
        all_permutation = get_all_letter_combinations()

        all_combinations = list(combinations(
            all_permutation, get_sample_size()))

        all_combinations.sort(
            key=lambda x: self.delta.get_complexity_of_subset(x))
        return all_combinations

    def get_from_pick_queue(self):
        temp = self.queue_of_picks[-1]
        self.queue_of_picks = self.queue_of_picks[:-1]  # Remove last pick
        temp.sort(key=lambda x: x[2])
        return temp

    def get_next_subset(self, previous_score, previous_subset):
        if len(self.queue_of_picks) > 0:
            return self.get_from_pick_queue()
        picks = []
        while True:
            # If we done we just return None
            if self.next_to_try >= len(self.all_combinations):
                picks = None
                self.all_done = True
                return picks  # no more to test

            current = self.all_combinations[self.next_to_try]

            self.next_to_try += 1  # Move one up for nextime

            # Picks will be returned this time
            picks = []
            multiple_picks = []  # Queue of picks to be tried later on.
            a_labeled_had_no_valid_mapping = False

            for pL in current:
                label_has_corresponding_data_instance = False
                # Currently we are only picking either a true or false, we should maybe try both?
                new_poss_picks = []

                if pL in self.label_to_data_map_true:
                    label_has_corresponding_data_instance = True
                    # If this is first we have to add it manually.
                    if len(multiple_picks) == 0:
                        new_poss_picks.append(
                            [self.label_to_data_map_true[pL][0]])
                    else:
                        # For each possible combination we add this option aswell.
                        for pos_pick in multiple_picks:
                            new_poss_picks.append(
                                pos_pick + [self.label_to_data_map_true[pL][0]])

                if pL in self.label_to_data_map_false:
                    label_has_corresponding_data_instance = True

                    # If this is first we have to add it manually.
                    if len(multiple_picks) == 0:
                        new_poss_picks.append(
                            [self.label_to_data_map_false[pL][0]])
                    else:
                        # For each possible combination we add this option aswell.
                        for pos_pick in multiple_picks:
                            new_poss_picks.append(
                                pos_pick + [self.label_to_data_map_false[pL][0]])

                if not label_has_corresponding_data_instance:
                    a_labeled_had_no_valid_mapping = True
                    break
                multiple_picks = new_poss_picks

            if a_labeled_had_no_valid_mapping:
                continue

            picks = multiple_picks[0]
            self.queue_of_picks = multiple_picks[1:]
            break
        picks.sort(key=lambda x: x[2])
        if len(self.queue_of_picks) == 0 and self.next_to_try >= len(self.all_combinations):
            self.all_done = True
        return picks
