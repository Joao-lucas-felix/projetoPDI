from Model.Imagem import Imagem


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
        linha_imagem_final =[]
        for j in range(0, largura_imagem_final):
            vizinhanca = []
            for x in range(0, m):
                linha = []
                for y in range(0, n):
                    linha.append(img.matriz[(pivo[0] - (m // 2) + x)][(pivo[1] - (n // 2) + y)])
                vizinhanca.append(linha)
            # calculo da correlação:
            linha_imagem_final.append(produto_interno(vizinhanca, mask.matriz))
            #atualização do pivo
            pivo[1] += 1
            contador += 1

        matriz_imagem_final.append(linha_imagem_final)
        pivo[0] += 1
        pivo[1] -= contador

    imagem_final = Imagem()
    imagem_final.size = [altura_imagem_final, largura_imagem_final]
    imagem_final.matriz = matriz_imagem_final

    return imagem_final


def produto_interno(img_matriz, mask):
    r, g, b = 0, 0, 0
    for line in range(len(img_matriz)):
        for cor in range(len(img_matriz[line])):
            r += img_matriz[line][cor][0] * mask[line][cor]
            g += img_matriz[line][cor][1] * mask[line][cor]
            b += img_matriz[line][cor][2] * mask[line][cor]

    r = round(r)
    g = round(g)
    b = round(b)
    r = min(255, r)
    g = min(255, g)
    b = min(255, b)

    r = max(0, r)
    g = max(0, g)
    b = max(0, b)

    return r, g, b
