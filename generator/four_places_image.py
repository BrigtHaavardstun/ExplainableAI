from os import WEXITED
from PIL import Image
from multiprocessing.pool import ThreadPool as Pool
from utils.common import get_all_permutations

import random
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT, DATA_SET_SIZE
import sys

def genereator(images, name, count):
    height = IMAGE_HIGHT
    width = IMAGE_WIDTH
    background = Image.new(mode="RGBA",size=(width,height), color=(255,255,255))
    
    diff = random.randint(0,10)-5
    paste_image_list = [Image.open(image_loc).resize((width//2+diff,height//2+diff)).convert("RGBA") for image_loc in images]
 

    positions = [(0,0), (0,height//2), (width//2, 0), (width//2,height//2)]
    for img in paste_image_list:
        x,y = random.choice(positions)
        background.paste(img, (x, y), img)
        positions.remove((x,y))
    background.save(f"data/images/{name}{count}.png")   

import random
def chooseFilesToCombine():
    possiblilities = get_all_permutations()
    return random.choice(possiblilities)


def run(verbose=False):
    # Run this in ./generator directory. New created images will be stored in ./generator/generated
    
    pool_size = 4  # your "parallelness"
    pool = Pool(pool_size)

    for i in range(DATA_SET_SIZE):
        letters = chooseFilesToCombine()   
        if verbose: 
            print(letters)
        name = "".join(sorted(letters))
        images = []
        for letter in letters:
            images.append(f"images/{letter}/{letter}.png")
        if verbose:
            print(images)
        pool.apply_async(genereator, (images, name, i,))

    pool.close()
    pool.join()
      