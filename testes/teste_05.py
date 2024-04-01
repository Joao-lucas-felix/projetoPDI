from Util.Util import image_to_rgb_matriz
from PIL import Image
from Services.Filtros_hsv import filtro_aditivo_matiz


img = Image.open("./Images/testpat.1k.color2.tif")
matriz = image_to_rgb_matriz(img)
img.show()
img = filtro_aditivo_matiz(matriz, 120)
imagem_final = Image.new("RGB", matriz.size, 0)

for i in range(0, img.size[0]):
    for j in range(0, img.size[1]):
        imagem_final.putpixel((i, j), img.matriz[i][j])
imagem_final.show()

