from PIL import Image
from Conversor import  image_to_hsv_format
from Conversor import hsv_matriz_to_image

image = Image.open("Images/img2.jpg")
hsv_image = image_to_hsv_format(image)
image2 = hsv_matriz_to_image(hsv_image)
image2.show()
