from PIL import Image
from Model.Imagem import Imagem


def image_to_rgb_matriz(image: Image):
    rgb_matriz = []
    for i in range(0, image.width):
        line = []
        for j in range(0, image.height):
            line.append(image.getpixel((i, j)))

        rgb_matriz.append(line)
    img = Imagem()
    img.size = image.size
    img.matriz = rgb_matriz
    return img


def rgb_matriz_to_image(rgb: Imagem):
    img = Image.new("RGB", rgb.size, 0)
    for i in range(0, rgb.size[0]):
        for j in range(0, rgb.size[1]):
            img.putpixel((i, j), rgb.matriz[i][j])
    return img


def read_mask_from_file(path: str):
    with open(path, "r") as file:
        mask_file = file.readline()

    mask_file = mask_file.split()
    count = 2
    mascara = []
    dim = [int(mask_file[0]), int(mask_file[1])]
    for i in range(0, dim[0]):
        linha = []
        for j in range(0, dim[1]):
            linha.append(float(mask_file[count]))
            count += 1
        mascara.append(linha)

    mask = Imagem()
    mask.size = dim
    mask.matriz = mascara

    return mask
