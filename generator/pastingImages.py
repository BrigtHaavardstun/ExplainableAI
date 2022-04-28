from turtle import pos
from PIL import Image
import random
from multiprocessing.pool import ThreadPool as Pool
from utils.global_props import IMAGE_WIDTH, IMAGE_HIGHT, get_data_size
from utils.common import get_all_permutations

"""
[ref](https://www.geeksforgeeks.org/find-two-rectangles-overlap/)
"""


def is_overlap(l1, r1, l2, r2):
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False

    if l1[1] > r2[1] or l2[1] > r1[1]:
        return False

    return True


def genereator(images, name, count):
    height = IMAGE_HIGHT
    width = IMAGE_WIDTH
    background = Image.new(mode="RGBA", size=(
        width, height), color=(255, 255, 255))

    # More noise in the training data
    img_size_width = height//2 - random.randint(0, 10)
    img_size_height = img_size_width  # we want to maintain scale.

    paste_image_list = [Image.open(image_loc).resize(
        (img_size_width, img_size_height)).convert("RGBA") for image_loc in images]
    already_paste_point_list = []

    for img in paste_image_list:
        # if all not overlap, find the none-overlap start point
        attempts = 0
        while True:
            attempts += 1
            if attempts == 1000:
                print(f"{str(count)}:couldn't find a place, resizing...")
                im_width, im_height = img.size
                img = img.resize((im_width-2, im_height-2))
                attempts = 0
            # left-top point
            # x, y = random.randint(0, background.size[0]), random.randint(0, background.size[1])

            # if image need in the bg area, use this
            x, y = random.randint(0, max(0, background.size[0]-img.size[0])), random.randint(
                0, max(0, background.size[1]-img.size[1]))

            # right-bottom point
            l2, r2 = (x, y), (x+img.size[0], y+img.size[1])

            if all(not is_overlap(l1, r1, l2, r2) for l1, r1 in already_paste_point_list):
                # save alreay pasted points for checking overlap
                already_paste_point_list.append((l2, r2))
                background.paste(img, (x, y), img)
                break

    background.save(f"data/images/{name}{count}.png")

    # check like this, all three rectangles all not overlapping each other
    from itertools import combinations
    assert(all(not is_overlap(l1, r1, l2, r2)
           for (l1, r1), (l2, r2) in combinations(already_paste_point_list, 2)))


def randomPickLetters():
    possiblilities = get_all_permutations()
    picked = random.choice(possiblilities)
    return picked

# define worker function before a Pool is instantiated


def generateImage(i):
    letters = randomPickLetters()
    if len(letters) == 0:
        genereator([], "", i)
    name = "".join(sorted(letters))
    images = []
    for letter in letters:
        rotation = random.randint(0, 7)
        images.append(f"images/{letter}/{letter}{rotation}.png")
    genereator(images, name, i)


def run():
    pool_size = 4  # your "parallelness"

    pool = Pool(pool_size)

    for item in range(get_data_size()):

        pool.apply_async(generateImage, (item,))

    pool.close()
    pool.join()
