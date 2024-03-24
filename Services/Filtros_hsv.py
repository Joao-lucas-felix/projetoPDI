from Model.Imagem import Imagem
from Services.Conversor import rgb_to_hsv, hsv_to_rgb


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



