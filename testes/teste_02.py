from PIL import Image
import Conversor

conversor = Conversor
image = Image.open("Images/lenna.jpg")
hsv_matriz = conversor.image_to_hsv_format(image)
lenna = conversor.hsv_matriz_to_image(hsv_matriz)
lenna.show()
