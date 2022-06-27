from PIL import Image
from multiprocessing.pool import ThreadPool as Pool
from utils.common import get_all_letter_combinations

import random
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT, get_data_size
import sys


def genereator(images, name, count, scale=False):
    height = IMAGE_HIGHT
    width = IMAGE_WIDTH
    background = Image.new(mode="RGBA", size=(
        width, height), color=(255, 255, 255))

    letter_w = IMAGE_WIDTH//2
    letter_h = IMAGE_HIGHT//2
    diff = 0
    if scale:
        maxDiff = min(letter_w//2, letter_h//2)
        diff = random.randint(0, maxDiff)
    paste_image_list = [Image.open(image_loc).resize(
        (letter_w-diff, letter_h-diff)).convert("RGBA") for image_loc in images]

    positions = [(0, 0), (0, height//2), (width//2, 0), (width//2, height//2)]
    for img in paste_image_list:
        x, y = random.choice(positions)
        background.paste(img, (x, y), img)
        positions.remove((x, y))
    background.save(f"data/images/{name}{count}.png")


def chooseFilesToCombine():
    possiblilities = get_all_letter_combinations()
    return random.choice(possiblilities)


def run(verbose=False, rotation=False, scale=False):
    # Run this in ./generator directory. New created images will be stored in ./generator/generated

    pool_size = 20  # your "parallelness"
    pool = Pool(pool_size)

    for i in range(get_data_size()):
        letters = chooseFilesToCombine()
        if verbose:
            print(letters)
        name = "".join(sorted(letters))
        images = []
        for letter in letters:
            letterRotation = letter
            if rotation:
                letterRotation += str(random.randint(0, 7))
            images.append(f"images/{letter}/{letterRotation}.png")
        if verbose:
            print(images)
        pool.apply_async(genereator, (images, name, i, scale,))

    pool.close()
    pool.join()
