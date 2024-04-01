from PIL import Image
from Services.Conversor import  image_to_hsv_format
from Services.Conversor import hsv_matriz_to_image

image = Image.open("Images/testpat.1k.color2.tif")
hsv_image = image_to_hsv_format(image)
image2 = hsv_matriz_to_image(hsv_image)
image2.show()
