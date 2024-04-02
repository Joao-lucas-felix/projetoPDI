import sympy as sp
from PIL import Image


# Arquivo que vai reunir todos os metodos do projeto
class Imagem:
    def __int__(self, size, matriz):
        self.size = size
        self.matriz = matriz


# Conversores De RGB - HSV
def rgb_to_hsv(cor):
    r, g, b = cor[0], cor[1], cor[2]
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    h = 0  # so por que tava dando um warning
    # definição do H
    if r == g and r == b:
        h = 0
    elif maximo == r and g >= b:
        h = 60 * ((g - b) / (maximo - minimo))
    elif maximo == r and g < b:
        h = 60 * ((g - b) / (maximo - minimo)) + 360
    elif maximo == g:
        h = 60 * ((b - r) / (maximo - minimo)) + 120
    elif maximo == b:
        h = 60 * ((r - g) / (maximo - minimo)) + 240

    # definição do S
    if maximo > 0:
        s = ((maximo - minimo) / maximo) * 100
    else:
        s = 0

    v = (maximo / 255) * 100
    return int(h), int(s), int(v)


def hsv_to_rgb(cor_hsv):
    # 1. Converter os valores HSV para o intervalo 0-1
    h = cor_hsv[0] / 360.0
    s = cor_hsv[1] / 100.0
    v = cor_hsv[2] / 100.0

    # 2. Calcular o componente de cor com base na matiz
    if s == 0:  # caso a saturação seja 0 a cor está na reta acromatica
        r = g = b = v
    else:
        h *= 6  # ajuste para o formato adequado como na multiplicação de transformação tem um *60
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

    # 3. Ajustar os valores RGB de acordo com o valor
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return r, g, b


def image_to_hsv_format(image: Image):
    hsv_matriz = []
    for i in range(0, int(image.width)):
        linha = []
        for j in range(0, int(image.height)):
            linha.append(rgb_to_hsv(image.getpixel((i, j))))
        hsv_matriz.append(linha)
    return hsv_matriz


def hsv_matriz_to_image(hsv_matriz):
    image2 = Image.new("RGB", (len(hsv_matriz), len(hsv_matriz[0])), 0)
    for i in range(0, image2.width):
        for j in range(0, image2.height):
            image2.putpixel((i, j), hsv_to_rgb(hsv_matriz[i][j]))
    return image2


# Filtros em HSV
def filtro_mutiplicativo_brilho(imagem: Imagem, fator_multiplicativo: float):
    imagem_filtrada = Imagem()
    imagem_filtrada.size = imagem.size
    matriz_nova = []
    for i in range(0, imagem.size[0]):
        linha_nova = []
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsv(imagem.matriz[i][j])
            brilho = hsv_cor[2] * fator_multiplicativo
            if brilho > 100:
                brilho = 100
            hsv_cor_nova = (hsv_cor[0], hsv_cor[1], brilho)
            linha_nova.append(hsv_to_rgb(hsv_cor_nova))
        matriz_nova.append(linha_nova)

    imagem_filtrada.matriz = matriz_nova
    return imagem_filtrada


def filtro_multiplicativo_saturacao(imagem: Imagem, fator_multiplicativo: float):
    imagem_filtrada = Imagem()
    imagem_filtrada.size = imagem.size
    matriz_nova = []
    for i in range(0, imagem.size[0]):
        linha_nova = []
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsv(imagem.matriz[i][j])
            saturacao = hsv_cor[1] * fator_multiplicativo
            if saturacao > 100:
                saturacao = 100
            hsv_cor_nova = (hsv_cor[0], saturacao, hsv_cor[2])
            linha_nova.append(hsv_to_rgb(hsv_cor_nova))
        matriz_nova.append(linha_nova)

    imagem_filtrada.matriz = matriz_nova
    return imagem_filtrada


def filtro_aditivo_matiz(imagem: Imagem, fator_aditivo: int):
    imagem_filtrada = Imagem()
    imagem_filtrada.size = imagem.size
    matriz_nova = []
    for i in range(0, imagem.size[0]):
        linha_nova = []
        for j in range(0, imagem.size[1]):
            hsv_cor = rgb_to_hsv(imagem.matriz[i][j])
            matiz = hsv_cor[0] + fator_aditivo
            if matiz >= 360:
                matiz = matiz % 360
            hsv_cor_nova = (matiz, hsv_cor[1], hsv_cor[2])
            linha_nova.append(hsv_to_rgb(hsv_cor_nova))
        matriz_nova.append(linha_nova)

    imagem_filtrada.matriz = matriz_nova
    return imagem_filtrada


# Transferencia de saturação de uma imagem para outra:
def filtro_transfere_saturacao(imagem1: Imagem, imagem2: Imagem):
    if imagem1.size != imagem2.size:
        print("Imagens possuem dimensões diferentes, impossivel fazer a operação")
        return
    for i in range(0, imagem1.size[0]):
        for j in range(0, imagem2.size[1]):
            cor_img1 = rgb_to_hsv(imagem1.matriz[i][j])
            cor_img2 = rgb_to_hsv(imagem2.matriz[i][j])
            cor_final = (cor_img2[0], cor_img1[1], cor_img2[2])
            imagem2.matriz[i][j] = hsv_to_rgb(cor_final)


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

    imagem_final = Imagem()
    imagem_final.size = [altura_imagem_final, largura_imagem_final]
    imagem_final.matriz = matriz_imagem_final

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
            linha.append(float(sp.N(mask_file[count])))
            # pega uma expressão aritimetica  e  a resolve com o sympy
            # depois faz um parse para float, dessa forma podemos definir expressões
            # aritimeticas nas mascaras.
            count += 1
        mascara.append(linha)

    mask = Imagem()
    mask.size = dim
    mask.matriz = mascara

    return mask


# processamento que arredonda os floats para inteiros e garante que eles estaram no intervalo (0,255)
# por meio de min/max
def processamento_para_exibir_imagem(img: Imagem):
    img_nova = Imagem()
    img_nova.size = img.size
    matriz = []
    for i in range(0, img.size[0]):
        linha = []
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
            linha.append((r, g, b))
        matriz.append(linha)
    img_nova.matriz = matriz
    return img_nova
