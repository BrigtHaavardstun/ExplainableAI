from PIL import Image
import random
import sys
from multiprocessing.pool import ThreadPool as Pool

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
    height = 57
    width = 57
    background = Image.new(mode="RGBA",size=(width,height), color=(255,255,255))

    img_size_width = height//3 #+ random.randint(-3,3)  # More noise in the training data
    img_size_height = height//3 #+ random.randint(-3,3) #
    
    paste_image_list = [Image.open(image_loc).resize((img_size_width,img_size_height)).convert("RGBA") for image_loc in images]
    alread_paste_point_list = []

    for img in paste_image_list:
        # if all not overlap, find the none-overlap start point
        attempts = 0
        while True:
            attempts += 1
            if attempts == 1000:
                print(f"{str(count)}:couldn't find a place, resizing...")
                im_width,im_height =img.size
                img = img.resize((im_width-2, im_height-2))
                attempts = 0
            # left-top point
            # x, y = random.randint(0, background.size[0]), random.randint(0, background.size[1])

            # if image need in the bg area, use this
            x, y = random.randint(0, max(0, background.size[0]-img.size[0])), random.randint(0, max(0, background.size[1]-img.size[1]))

            # right-bottom point
            l2, r2 = (x, y), (x+img.size[0], y+img.size[1])

            if all(not is_overlap(l1, r1, l2, r2) for l1, r1 in alread_paste_point_list):
                # save alreay pasted points for checking overlap
                alread_paste_point_list.append((l2, r2))
                background.paste(img, (x, y), img)
                break

    background.save(f"../data/images/{name}{count}.png")

    # check like this, all three rectangles all not overlapping each other
    from itertools import combinations
    assert(all(not is_overlap(l1, r1, l2, r2) for (l1, r1), (l2, r2) in combinations(alread_paste_point_list, 2)))


import random
def chooseFilesToCombine(num):
    possiblilities = ["A","B","C","D"]
    picked = []
    for i in range(num):
        picked.append(random.choice(possiblilities))
        possiblilities.remove(picked[-1])
    return picked

# define worker function before a Pool is instantiated
def generateImage(i, itterations):
    letters = chooseFilesToCombine(random.randint(0,4))    
    if len(letters) == 0:
        genereator([], "", i)
    name = "".join(sorted(letters))
    images = []
    for letter in letters:
        rotation = random.randint(0,7)
        images.append(f"../images/{letter}/{letter}{rotation}.png")
    genereator(images, name, i)


if __name__ == "__main__":
    itterations = 10000
   
    pool_size = 4  # your "parallelness"

    pool = Pool(pool_size)

    for item in range(itterations):
        
        pool.apply_async(generateImage, (item,(itterations),))

    pool.close()
    pool.join()