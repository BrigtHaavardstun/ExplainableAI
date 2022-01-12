from PIL import Image
import random
import sys

def genereator(images, name, count):
    height = 200
    width = 200
    background = Image.new(mode="RGBA",size=(width,height), color=(255,255,255))
    
    
    paste_image_list = [Image.open(image_loc).resize((100,100)).convert("RGBA") for image_loc in images]
 

    positions = [(0,0), (0,100), (100, 0), (100,100)]
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
    for i in range(10):
        letters = chooseFilesToCombine(random.randint(1,4))    
        print(letters)
        name = "".join(sorted(letters))
        images = []
        for letter in letters:
            images.append(f"../images/{letter}/{letter}.png")
        print(images)
        genereator(images, name, i)