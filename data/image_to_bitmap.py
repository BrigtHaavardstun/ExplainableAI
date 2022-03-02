# https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
import numpy as np
from PIL import Image
import sys


def image_loc_to_bitmap(image_location):

    img = Image.open(image_location).convert('L')
    ary = np.array(img)
    bitmap = np.array(ary).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap < 128).astype(float), 255)

    return bitmap


def converter(new_prefix, image_location):
    bitmap = image_loc_to_bitmap(image_location)

    # W
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(f'{new_prefix}{image_location[:-4].split("/")[-1]}.bmp')


if __name__ == "__main__":
    # THIS WILL BE RUN FROM data
    file_name = sys.argv[1]
    print(file_name)
    image_loc = file_name
    new_prefix = "training_data/"
    converter(new_prefix, image_loc)
