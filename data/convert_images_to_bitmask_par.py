from multiprocessing.pool import ThreadPool as Pool

from data.image_to_bitmap import converter
from os import listdir
from os.path import isfile, join


def load_files():
    directory = "data/images"
    onlyfiles = sorted([directory + "/" + f for f in listdir(directory)
                       if isfile(join(directory, f)) and f[-4:] == ".png"])
    return onlyfiles


def run():

    pool_size = 20  # your "parallelness"
    files = load_files()

    pool = Pool(pool_size)

    new_prefix = "data/training_data/"

    for filelocation in files:
        pool.apply_async(converter, (new_prefix, filelocation,))
    pool.close()
    pool.join()
