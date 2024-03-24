from Util.Util import image_to_rgb_matriz
from PIL import Image
from Services.Filtros_hsv import filtro_multiplicativo_saturacao
img = Image.open("Images/DancingInWater.jpg")
matriz = image_to_rgb_matriz(img)
img.show()
img = filtro_multiplicativo_saturacao(matriz, 1.2)
imagem_final = Image.new("RGB", matriz.size, 0)

for i in range(0, img.size[0]):
    for j in range(0, img.size[1]):
        imagem_final.putpixel((i, j), img.matriz[i][j])
imagem_final.show()
