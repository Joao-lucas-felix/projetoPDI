from PIL import Image
from Services.Filtros_hsv import filtro_transfere_saturacao
from Util.Util import image_to_rgb_matriz, rgb_matriz_to_image
from Services.Conversor import rgb_to_hsv

img1 = Image.new("RGB", (225, 225), (255, 75, 255))
img2 = Image.new("RGB", (225, 225), (255, 255, 0))
img2.show()

matriz1 = image_to_rgb_matriz(img1)
matriz2 = image_to_rgb_matriz(img2)

print(rgb_to_hsv(matriz1.matriz[0][0]))
print(rgb_to_hsv(matriz2.matriz[0][0]))

filtro_transfere_saturacao(matriz1, matriz2)

print()
print(rgb_to_hsv(matriz1.matriz[0][0]))
print(rgb_to_hsv(matriz2.matriz[0][0]))

img_final = rgb_matriz_to_image(matriz2)

img_final.show()
