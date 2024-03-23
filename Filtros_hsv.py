from Model import Imagem
import Conversor


def filtro_mutiplicativo_brilho(imagem: Imagem, fator_multiplicativo):
    imagem_filtrada = Imagem()
    imagem_filtrada.size = imagem.size
    matriz_nova = []
    conversor = Conversor
    for i in range(0, imagem.size[0]):
        linha_nova = []
        for j in range(0, imagem.size[1]):
            hsv_cor = conversor.rgb_to_hsv(imagem.matriz[i][j])
            brilho = hsv_cor[2] * fator_multiplicativo
            if brilho > 100:
                brilho = 100
            hsv_cor_nova = (hsv_cor[0], hsv_cor[1], brilho)
            linha_nova.append(conversor.hsv_to_rgb(hsv_cor_nova))
        matriz_nova.append(linha_nova)

    imagem_filtrada.matriz = matriz_nova
    return imagem_filtrada
