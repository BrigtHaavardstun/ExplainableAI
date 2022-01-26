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
    height = 32
    width = 32
    background = Image.new(mode="RGBA",size=(width,height), color=(255,255,255))

    
    paste_image_list = [Image.open(image_loc).resize((width//3,height//3)).convert("RGBA") for image_loc in images]
    alread_paste_point_list = []

    for img in paste_image_list:
        # if all not overlap, find the none-overlap start point
        while True:
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
    if item%(itterations//100)== 0:
            print(str(100*item/itterations)+"%")
    letters = chooseFilesToCombine(random.randint(1,4))    
    name = "".join(sorted(letters))
    images = []
    for letter in letters:
        rotation = 0
        images.append(f"../images/{letter}/{letter}{rotation}.png")
    genereator(images, name, i)


if __name__ == "__main__":
    itterations = 3000
   
    pool_size = 4  # your "parallelness"

    pool = Pool(pool_size)

    for item in range(itterations):
        
        pool.apply_async(generateImage, (item,(itterations+2000),))

    pool.close()
    pool.join()