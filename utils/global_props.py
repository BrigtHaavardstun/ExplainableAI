# Image attributes
IMAGE_WIDTH = 64
IMAGE_HIGHT = 64


# Letters being used
ALL_LETTERS = ["A", "B", "C", "D"]


# Data set sizes
DATA_SET_SIZE = 100000


def set_data_size(size):
    global DATA_SET_SIZE
    DATA_SET_SIZE = size


def get_data_size():
    global DATA_SET_SIZE
    return DATA_SET_SIZE


# Number of samples(?) picked by AT, maybe?
SAMPLE_SIZE = 5  # Number of pictures to be shown


def set_sample_size(size):
    global SAMPLE_SIZE
    print(size)
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


def booleanFunctionDefiniton(A, B, C, D):
    return (A and B) or C
