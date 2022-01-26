from multiprocessing.pool import ThreadPool as Pool

from image_to_bitmap import main as converter
from os import listdir
from os.path import isfile, join
    
def load_files():
    directory = "images"
    onlyfiles = sorted([directory +"/"+ f for f in listdir(directory) if isfile(join(directory, f)) and f[-4:] == ".png"])
    return onlyfiles

if __name__ == "__main__":


    pool_size = 20  # your "parallelness"
    files = load_files()

    pool = Pool(pool_size)

    new_prefix = "training_data/"


    for filelocation in files:        
        pool.apply_async(converter, (new_prefix,filelocation,))
    pool.close()
    pool.join()
