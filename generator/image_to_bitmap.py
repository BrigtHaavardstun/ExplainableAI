#https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
import numpy as np
from PIL import Image
import sys
def image_loc_to_bitmap(image_location):
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
    return bitmap

def main(new_prefix,image_location):
    
    bitmap = image_loc_to_bitmap(image_loc)
    # W
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(f'{new_prefix}{image_location[:-4].split("/")[-1]}.bmp')

if __name__ == "__main__":
    # THIS WILL BE RUN FROM ../../generated
    file_name = sys.argv[1]
    print(file_name)
    image_loc = file_name
    new_prefix = "../../MLmodels/training_data/"
    main(new_prefix,image_loc)