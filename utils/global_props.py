# Image attributes
IMAGE_WIDTH = 64
IMAGE_HIGHT = 64


# Letters being used
ALL_LETTERS = ["A", "B", "C", "D"]


# Data set sizes
DATA_SET_SIZE = 100

# Number of samples(?) picked by AT, maybe?
SAMPLE_SIZE = 4 # Number of pictures to be shown
SAMPLE_ATTEMPTS = 10000 # Number of itterations of AI argmin
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