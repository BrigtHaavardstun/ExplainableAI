# import the Python Image processing Library

from PIL import Image
import glob, os, sys



def generate_rotations(letter):
    # Create an Image object from an Image
    print(letter)
    colorImage  = Image.open(f"./{letter}.png")
    
    for i in range(8):
    # Rotate it by 45 degrees
        rotated  = colorImage.rotate(45*i,expand=True)
        rotated.save(f"./{letter}{i}.png")

    
 
if __name__ == "__main__":
    arg = sys.argv[1]
    print(arg)
    generate_rotations(arg)
