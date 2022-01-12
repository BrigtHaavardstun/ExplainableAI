from os import WEXITED
from PIL import Image
import random
import sys

def genereator(images, name, count):
    height = 64
    width = 64
    background = Image.new(mode="RGBA",size=(width,height), color=(255,255,255))
    
    
    paste_image_list = [Image.open(image_loc).resize((width//2,height//2)).convert("RGBA") for image_loc in images]
 

    positions = [(0,0), (0,height//2), (width//2, 0), (width//2,height//2)]
    for img in paste_image_list:
        x,y = random.choice(positions)
        background.paste(img, (x, y), img)
        positions.remove((x,y))
    background.save(f"../generator/generated/{name}{count}.png")   

def chooseFilesToCombine(num):
    possiblilities = ["A","B","C","D"]
    picked = []
    for i in range(num):
        picked.append(random.choice(possiblilities))
        possiblilities.remove(picked[-1])
    return picked


if __name__ == "__main__":
    # Run this in ./generator directory. New created images will be stored in ./generator/generated
    for i in range(200):
        letters = chooseFilesToCombine(random.randint(1,4))    
        print(letters)
        name = "".join(sorted(letters))
        images = []
        for letter in letters:
            images.append(f"../images/{letter}/{letter}.png")
        print(images)
        genereator(images, name, i)