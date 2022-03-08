
from itertools import combinations
from utils.global_props import ALL_LETTERS
import math

def get_all_permutations(letters=ALL_LETTERS):
    if len(letters) <= 1:
        return letters
    all_combinations = list()
    all_combinations.append("")
    all_combinations.extend(letters)

    for i in range(2, len(letters)+1):
        result = list(combinations(letters, i))

        all_combinations.extend(["".join(list(elem)) for elem in result])
    return all_combinations

_TOT_COMB_SIZE = None
def total_combinations():
    global _TOT_COMB_SIZE
    """
    We allow multiple *, but no else repating.

    Hence total is (2^n-1 pick n) + (2^n-1 pick (n-1)) + ...+ (2^n-1 pick 1) + (2^n-1 pick 0)

    for each we place "*" in the empty places.
    """
    if _TOT_COMB_SIZE is not None:
        return _TOT_COMB_SIZE
    
    total_combinations = 0
    N = len(ALL_LETTERS)
    for i in range(len(ALL_LETTERS)+1):
        total_combinations = math.factorial(N)/(math.factorial(i)*(math.factorial(N-i)))

    _TOT_COMB_SIZE = total_combinations
    print(_TOT_COMB_SIZE)
    return _TOT_COMB_SIZE


def remove_digit_from_labels(labels):
    """
    Removes all digits from labels

    abc3242 -> abc
    cd33 -> cd
    24 -> ''
    """
    proccessed_labels = []
    for label in labels:
        curr_label = ""
        for i, e in enumerate(label):
            if e.isalpha():
                curr_label += e
            else:  # e.isdigit()
                break
        proccessed_labels.append(curr_label)
    return proccessed_labels


def convert_label_to_binary(label):
    converted = ""
    if "A" in label:
        converted += "1"
    else:
        converted += "0"
    if "B" in label:
        converted += "1"
    else:
        converted += "0"
    if "C" in label:
        converted += "1"
    else:
        converted += "0"
    if "D" in label:
        converted += "1"
    else:
        converted += "0"
    return converted


def convert_digit_to_binary(digit):
    return bin(digit)[2:].zfill(4)


def one_hot_to_number(one_hot):
    if one_hot[0] == 1:
        return 0
    else:
        return 1
