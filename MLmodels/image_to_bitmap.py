#https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
import numpy as np
from PIL import Image

def main(image_location):
    img = Image.open(image_location).convert('L')
    
    ary = np.array(img)
    # Split the three channels
    #r,g,b = np.split(ary,3,axis=2)
    #r=r.reshape(-1)
    #g=r.reshape(-1)
    #b=r.reshape(-1)

    # Standard RGB to grayscale 
    #bitmap = list(map(lambda x: 0.2989*x[0]+0.5870*x[1]+0.1140*x[2], zip(r,g,b))) #https://www.delftstack.com/howto/python/convert-image-to-grayscale-python/
    bitmap = np.array(ary).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap < 128).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(f'{image_location[:-4]}.bmp')

if __name__ == "__main__":
    image_loc = "../generator/generated/A3.png"
    main(image_loc)