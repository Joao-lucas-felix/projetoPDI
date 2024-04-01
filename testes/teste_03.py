from Util.Util import image_to_rgb_matriz
from PIL import Image
from Services.Filtros_hsv import filtro_mutiplicativo_brilho

matriz = image_to_rgb_matriz(Image.open("./Images/testpat.1k.color2.tif"))

img = filtro_mutiplicativo_brilho(matriz, 1.4)
imagem_final = Image.new("RGB", matriz.size, 0)

for i in range(0, img.size[0]):
    for j in range(0, img.size[1]):
        imagem_final.putpixel((i, j), img.matriz[i][j])
imagem_final.show()
