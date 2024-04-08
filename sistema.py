from copy import copy

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from PIL import Image


# Arquivo que vai reunir todos os metodos do projeto
class Imagem:
    def __init__(self, size, matriz):
        self.size = size
        self.matriz = matriz


# Conversores De RGB - HSV
def rgb_to_hsb(cor_rgb):
    r, g, b = cor_rgb
    # Normaliza os valores de RGB para o intervalo [0, 1]
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Encontra o valor máximo e mínimo entre os componentes R, G e B
    max_val = max(r, g, b)
    min_val = min(r, g, b)

    # Calcula a diferença entre o máximo e o mínimo
    delta = max_val - min_val

    # Calcula o componente de brilho (Value)
    v = max_val

    # Se o valor de delta for muito pequeno, o pixel é uma tonalidade de cinza
    if delta < 0.00001:
        h = 0  # Nesse caso, a matiz é indefinida, então pode ser definida como 0
        s = 0
    else:
        # Calcula o componente de saturação (Saturation)
        s = delta / max_val

        # Calcula o componente de matiz (Hue)
        if r == max_val:
            h = (g - b) / delta
        elif g == max_val:
            h = 2 + (b - r) / delta
        else:
            h = 4 + (r - g) / delta

        # Converte h para o intervalo [0, 360] graus
        h *= 60
        if h < 0:
            h += 360

    # Retorna os valores HSB
    return h, s, v


def hsb_to_rgb(cor_hsb):
    h, s, v = cor_hsb
    if s == 0:
        r = g = b = int(v * 255)
    else:
        h /= 60.0
        i = int(h)
        f = h - i
        p = int(v * (1.0 - s) * 255)
        q = int(v * (1.0 - (s * f)) * 255)
        t = int(v * (1.0 - (s * (1.0 - f))) * 255)

        if i == 0:
            r, g, b = v * 255, t, p
        elif i == 1:
            r, g, b = q, v * 255, p
        elif i == 2:
            r, g, b = p, v * 255, t
        elif i == 3:
            r, g, b = p, q, v * 255
        elif i == 4:
            r, g, b = t, p, v * 255
        else:
            r, g, b = v * 255, p, q

    return int(r), int(g), int(b)


def image_to_hsb_format(image: Imagem):
    hsv_image = copy(image)
    for i in range(0, int(image.size[0])):
        for j in range(0, int(image.size[1])):
            hsv_image.matriz[i][j] = rgb_to_hsb(image.matriz[i][j])

    return hsv_image


def hsb_matriz_to_image(hsv_matriz: Imagem):
    image2 = copy(hsv_matriz)
    for i in range(0, image2.size[0]):
        for j in range(0, image2.size[1]):
            image2.matriz[i][j] = hsb_to_rgb(hsv_matriz.matriz[i][j])

    return image2


# Filtros em HSV
def filtro_mutiplicativo_brilho(imagem: Imagem, fator_multiplicativo: float):
    imagem_filtrada = copy(imagem)
    for i in range(0, imagem.size[0]):
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsb(imagem.matriz[i][j])
            brilho = hsv_cor[2] * fator_multiplicativo
            if brilho > 100:
                brilho = 100
            hsv_cor_nova = (hsv_cor[0], hsv_cor[1], brilho)
            imagem_filtrada.matriz[i][j] = hsb_to_rgb(hsv_cor_nova)

    return imagem_filtrada


def filtro_multiplicativo_saturacao(imagem: Imagem, fator_multiplicativo: float):
    imagem_filtrada = copy(imagem)
    for i in range(0, imagem.size[0]):
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsb(imagem.matriz[i][j])
            saturacao = hsv_cor[1] * fator_multiplicativo
            if saturacao > 100:
                saturacao = 100
            hsv_cor_nova = (hsv_cor[0], saturacao, hsv_cor[2])
            imagem_filtrada.matriz[i][j] = hsb_to_rgb(hsv_cor_nova)

    return imagem_filtrada


def filtro_aditivo_matiz(imagem: Imagem, fator_aditivo: int):
    imagem_filtrada = copy(imagem)
    for i in range(0, imagem.size[0]):
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsb(imagem.matriz[i][j])
            matiz = hsv_cor[0] + fator_aditivo
            if matiz >= 360:
                matiz = matiz % 360
            hsv_cor_nova = (matiz, hsv_cor[1], hsv_cor[2])
            imagem_filtrada.matriz[i][j] = hsb_to_rgb(hsv_cor_nova)

    return imagem_filtrada


# Transferencia de saturação de uma imagem para outra:
def filtro_transfere_saturacao(imagem1: Imagem, imagem2: Imagem):
    if imagem1.size != imagem2.size:
        print("Imagens possuem dimensões diferentes, impossivel fazer a operação")
        return
    for i in range(0, imagem1.size[0]):
        for j in range(0, imagem2.size[1]):
            cor_img1 = rgb_to_hsb(imagem1.matriz[i][j])
            cor_img2 = rgb_to_hsb(imagem2.matriz[i][j])
            cor_final = (cor_img2[0], cor_img1[1], cor_img2[2])
            imagem2.matriz[i][j] = hsb_to_rgb(cor_final)


# Maquina de Correlação
def correlacao(img: Imagem, mask: Imagem):
    m, n = mask.size
    altura, largura = img.size

    altura_imagem_final = altura - m + 1
    largura_imagem_final = largura - n + 1
    pivo = [(m // 2), (n // 2)]
    if altura_imagem_final <= 0 or largura_imagem_final <= 0:
        print("Impossivel de calcular sem extensão!")
        return -1

    matriz_imagem_final = []
    for i in range(0, altura_imagem_final):
        contador = 0
        linha_imagem_final = []
        for j in range(0, largura_imagem_final):
            vizinhanca = []
            for x in range(0, m):
                linha = []
                for y in range(0, n):
                    linha.append(img.matriz[(pivo[0] - (m // 2) + x)][(pivo[1] - (n // 2) + y)])
                vizinhanca.append(linha)
            # calculo da correlação:
            linha_imagem_final.append(produto_interno(vizinhanca, mask.matriz))
            # atualização do pivo
            pivo[1] += 1
            contador += 1

        matriz_imagem_final.append(linha_imagem_final)
        pivo[0] += 1
        pivo[1] -= contador
    imagem_final = Imagem([altura_imagem_final, largura_imagem_final], matriz_imagem_final)
    return imagem_final


# Util:
def produto_interno(img_matriz, mask):
    r, g, b = 0, 0, 0
    for line in range(len(img_matriz)):
        for cor in range(len(img_matriz[line])):
            r += img_matriz[line][cor][0] * mask[line][cor]
            g += img_matriz[line][cor][1] * mask[line][cor]
            b += img_matriz[line][cor][2] * mask[line][cor]
    return r, g, b


def image_to_rgb_matriz(image: Image):
    rgb_matriz = []
    for i in range(0, image.width):
        line = []
        for j in range(0, image.height):
            line.append(image.getpixel((i, j)))

        rgb_matriz.append(line)
    img = Imagem(image.size, rgb_matriz)
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
            linha.append(float(sp.N(mask_file[count])))
            # pega uma expressão aritimetica  e  a resolve com o sympy
            # depois faz um parse para float, dessa forma podemos definir expressões
            # aritimeticas nas mascaras.
            count += 1
        mascara.append(linha)

    mask = Imagem(dim, mascara)
    return mask


# processamento que arredonda os floats para inteiros e garante que eles estaram no intervalo (0,255)
# por meio de min/max
def processamento_para_exibir_imagem(img: Imagem):
    img_nova = Imagem(img.size, img.matriz)
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            r, g, b = img.matriz[i][j]
            r = round(r)
            g = round(g)
            b = round(b)
            r = min(255, r)
            g = min(255, g)
            b = min(255, b)

            r = max(0, r)
            g = max(0, g)
            b = max(0, b)
            img_nova.matriz[i][j] = (r, g, b)
    return img_nova


# processamento para exibir sobel:
def processamento_valor_absoluto(img: Imagem):
    img_nova = Imagem(img.size, img.matriz)
    for i in range(0, img_nova.size[0]):
        for j in range(0, img_nova.size[1]):
            r, g, b = img.matriz[i][j]
            r = abs(r)
            g = abs(g)
            b = abs(b)
            img_nova.matriz[i][j] = (r, g, b)
    return img_nova


# Criação do metodo para Espanção de histograma:

def histogram_expansion(img: Imagem):
    mat = np.array(img.matriz)
    # Separando os canais de cor
    canal_r = mat[:, :, 0]
    canal_g = mat[:, :, 1]
    canal_b = mat[:, :, 2]

    # Achando rmax e rmim em R, G e B. E calculando (l-1)/ rmax-rmim
    max_r = np.amax(canal_r)
    min_r = np.amin(canal_r)
    const_r = 255 / (max_r - min_r)
    max_g = np.amax(canal_g)
    min_g = np.amin(canal_g)
    const_g = 255 / (max_g - min_g)

    max_b = np.amax(canal_b)
    min_b = np.amin(canal_b)
    const_b = 255 / (max_b - min_b)

    new_image = Imagem(img.size, img.matriz)
    # fazendo o processo de expanção de histograma
    print(max_r)
    print(min_r)
    for i in range(new_image.size[0]):
        for j in range(new_image.size[1]):
            new_r = round((img.matriz[i][j][0] - min_r) * const_r)
            new_g = round((img.matriz[i][j][1] - min_g) * const_g)
            new_b = round((img.matriz[i][j][2] - min_b) * const_b)
            new_image.matriz[i][j] = (new_r, new_g, new_b)
    return new_image


# metodos para a vizualização do histograma antes e pos expanção
def build_histogram(img: Imagem):
    mat = np.array(img.matriz)
    # Separando os canais de cor
    canal_r = mat[:, :, 0]
    canal_g = mat[:, :, 1]
    canal_b = mat[:, :, 2]
    max_r = np.amax(canal_r)
    max_g = np.amax(canal_g)
    max_b = np.amax(canal_b)

    r = {i: 0 for i in range(0, int(max_r)+1)}
    g = {i: 0 for i in range(0, int(max_g)+1)}
    b = {i: 0 for i in range(0, int(max_b)+1)}

    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            r[img.matriz[i][j][0]] += 1
            g[img.matriz[i][j][1]] += 1
            b[img.matriz[i][j][2]] += 1
    print(r)
    print(g)
    print(b)
    return [r, g, b]


def plot_graficos_de_barras(lista_de_dicionarios):
    fig, axs = plt.subplots(1, len(lista_de_dicionarios), figsize=(18, 6))
    canais_cor = ["R", "G", "B"]
    for i, dicionario in enumerate(lista_de_dicionarios):
        chaves = list(dicionario.keys())
        valores = list(dicionario.values())

        axs[i].bar(chaves, valores)
        axs[i].set_xlabel('Niveis de quantização')
        axs[i].set_ylabel('Valores')
        axs[i].set_title('Canal {}'.format(canais_cor[i]))

    plt.tight_layout()
    plt.show()


def save_image(img: Imagem, path: str):
    img = rgb_matriz_to_image(img)
    img.save(path)


def open_image(path: str):
    img = Image.open(path)
    img = image_to_rgb_matriz(img)
    return img


def multplyB(path: str, fator: float, save_path: str):
    img = open_image(path)
    filtro_mutiplicativo_brilho(img, fator)
    save_image(img, save_path)


def multplyS(path: str, fator: float, save_path: str):
    img = open_image(path)
    filtro_multiplicativo_saturacao(img, fator)
    save_image(img, save_path)


def addM(path: str, fator: int, save_path: str):
    img = open_image(path)
    filtro_aditivo_matiz(img, fator)
    save_image(img, save_path)


def tranfereS(img1_path: str, img2_path: str, save_path: str):
    img1 = open_image(img1_path)
    img2 = open_image(img2_path)
    filtro_transfere_saturacao(img1, img2)
    save_image(img2, save_path)

def makecorelation(path_image: str, path_mask: str):
    img = open_image(path_image)
    mask = read_mask_from_file(path_mask)
    corelation = correlacao(img, mask)
    return corelation
