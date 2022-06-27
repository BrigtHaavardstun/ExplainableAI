"""
The goal of smart select is to not test combionations already tested. 
We only allow unique subset combinations.
We don't allow the letters of two instances to be the same.
"""


import random
from TA.subset.ISubset import ISubsetSelector

from utils.global_props import get_sample_size
from utils.common import total_combinations
from random import choice
from random import seed

from TA.subset.random_select import RandomSelect


class SmartSelect(ISubsetSelector):
    def __init__(self):
        super(SmartSelect, self).__init__()

    def __repr__(self):
        return "SmartSelect"

    def load(self, all_data_zip, true_data_zip, false_data_zip):
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip
        self.tried_lables = []
        self.found_all_possible = False

        self.random_backup = RandomSelect()
        self.random_backup.load(all_data_zip, true_data_zip, false_data_zip)

    def get_next_subset(self, previous_score, previus_subset):
        found_new = False
        picks = []
        MAX_ITER = 100000
        counter = 0
        while not found_new:
            counter += 1
            if counter == MAX_ITER:
                self.found_all_possible = True
            picks = []
            assert len(self.true_data_zip) != 0
            # picks.append(choice(self.true_data_zip))  # one true
            assert len(self.false_data_zip) != 0
            # picks.append(choice(self.false_data_zip))  # one false
            while(len(picks) < get_sample_size()):
                to_add = choice(self.all_data_zip)
                picks.append(to_add)

            # If we have found "all_possible" we return earlier
            if self.found_all_possible:
                print("all_possible early!")
                break

            # We don't want to check for equvilant examples multiple times.
            choosen_labels = sorted([str(pL+str(pY)) for pX, pY, pL in picks])

            # Add check for duplicates
            contains_duplicates = False

            """ 
            for i, e in enumerate(choosen_labels):
                if i < len(choosen_labels) - 1:
                    # we allow duplicate for ''
                    if e == "":
                        continue
                    # Check for duplicate
                    if e == choosen_labels[i+1]:
                        contains_duplicates = True
                        break
            
            # Restart while, do new search
            if contains_duplicates:
                continue
            """

            # We have found all combinations. So its okey to return something tried.
            if total_combinations() == len(self.tried_lables):
                break
            # Check if we already have tested this letter combination. Made to str for hash abilty
            # Note, if tha AI have different predictions for same letter we skip them.
            labels_picked = ",".join(choosen_labels)
            if labels_picked in self.tried_lables:
                #print("HASH HIT!")
                continue
            else:
                found_new = True
                self.tried_lables.append(labels_picked)
                print("found new hash!", labels_picked,
                      "total: " + str(len(self.tried_lables)))

        picks.sort(key=lambda x: x[2])  # sort on lable.
        return picks

    def display_hashed(self):
        with open("Output.txt", "w") as f:
            f.write("\n".join(sorted(self.tried_lables)))
