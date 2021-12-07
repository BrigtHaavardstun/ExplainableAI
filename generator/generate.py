# import the Python Image processing Library

from PIL import Image

 

# Create an Image object from an Image
colorImage  = Image.open("../images/a.png")

 
# Rotate it by 45 degrees
rotated  = colorImage.rotate(45)

# Rotate it by 90 degrees
transposed  = Image.open("../images/generated/A_90.png")

 

# Display the Original Image

#colorImage.show()

 

# Display the Image rotated by 45 degrees

#rotated.show()

 

# Display the Image rotated by 90 degrees

#transposed.show()

colorSize = colorImage.size
transposed = transposed.resize(colorSize)
print(transposed)
print(colorImage)

colorImage = colorImage.convert("RGBA")
transposed = transposed.convert("RGBA")
#transposed.show()
#colorImage.show()


blend = Image.alpha_composite(colorImage, transposed)
blend.show()