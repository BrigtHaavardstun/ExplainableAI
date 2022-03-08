"""
The goal of smart select is to not test combionations already tested. 
We only allow unique subset combinations.
We don't allow the letters of two instances to be the same.
"""


import random
from TA.subset.ISubset import ISubsetSelector

from utils.global_props import SAMPLE_SIZE
from utils.common import total_combinations 
from random import choice
from random import seed


class SmartSelect(ISubsetSelector):
    def __repr__(self):
        return "SmartSelect"

    def load(self, all_data_zip, true_data_zip, false_data_zip):
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip
        self.sample_size = SAMPLE_SIZE
        self.tried_lables = []
        

    def get_next_subset(self, previus_score, previus_subset):
        found_new = False
        picks = []
        while not found_new:
            picks = []
            assert len(self.true_data_zip) != 0
            # picks.append(choice(self.true_data_zip))  # one true
            assert len(self.false_data_zip) != 0
            # picks.append(choice(self.false_data_zip))  # one false
            while(len(picks) < self.sample_size):
                to_add = choice(self.all_data_zip)
                picks.append(to_add)

            # We don't want to check for equvilant examples multiple times.
            choosen_labels = sorted([str(pL) for pX, pY, pL in picks])

            # Add check for duplicates
            contains_duplicates = False

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

        return picks

    def display_hashed(self):
        with open("Output.txt", "w") as f:
            f.write("\n".join(sorted(self.tried_lables)))
