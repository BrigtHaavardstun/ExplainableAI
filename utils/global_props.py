# Image attributes
IMAGE_WIDTH = 64
IMAGE_HIGHT = 64


# Letters being used
ALL_LETTERS = ["A", "B", "C", "D"]


def get_all_letters():
    global ALL_LETTERS
    return ALL_LETTERS


# Data set sizes
DATA_SET_SIZE = 10000


def set_data_size(size):
    global DATA_SET_SIZE
    DATA_SET_SIZE = size


def get_data_size():
    global DATA_SET_SIZE
    return DATA_SET_SIZE


SAMPLE_SIZE = 5  # Number of pictures to be shown


def set_sample_size(size):
    global SAMPLE_SIZE
    SAMPLE_SIZE = size


def get_sample_size():
    global SAMPLE_SIZE
    return SAMPLE_SIZE


SAMPLE_ATTEMPTS = 200  # Number of itterations of AI argmin

# Run overwrites this value.
# Move SAMPLE_ATTEMPTS_LITS TO THIS FILE(?)


def set_sample_attempts(size):
    """
    Using this we can create a graf plot of the "complexity" / "compatibility" score of each combination on different attempts to
    Hoping to show how fast they converge.
    """
    global SAMPLE_ATTEMPTS
    SAMPLE_ATTEMPTS = size


def get_sample_attempts():
    global SAMPLE_ATTEMPTS
    return SAMPLE_ATTEMPTS


def booleanFunctionDefiniton(boolean_dict):
    A = boolean_dict["A"]
    B = boolean_dict["B"]
    C = boolean_dict["C"]
    D = boolean_dict["D"]
    return not A


def score_function(complexity, compatibility):
    global e, B, mu
    if complexity <= e and compatibility <= B:
        return (complexity + compatibility*mu)
    return float("inf")


e = float("inf")  # complexity


def set_e(value):
    global e
    e = value


def get_e():
    global e
    return e


B = float("inf")  # compatibility


def set_B(value):
    global B
    B = value


def get_B():
    global B
    return B


mu = 100


def set_mu(value):
    global mu
    mu = value


def get_mu():
    global mu
    return mu


def set_e_b_mu(e, b, mu):
    set_e(e)
    set_B(b)
    set_mu(mu)
