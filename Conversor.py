from PIL import Image


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
