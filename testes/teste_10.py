import sistema
from PIL import Image

img = Image.open("Images/lenna.jpg")
img = sistema.image_to_rgb_matriz(img)
img = sistema.correlacao(img, sistema.read_mask_from_file("masks/sobel1.txt"))
img = sistema.processamento_valor_absoluto(img)
sistema.plot_graficos_de_barras(sistema.build_histogram(img))
sistema.rgb_matriz_to_image(sistema.processamento_para_exibir_imagem(img)).show()


img = sistema.histogram_expansion(img)
sistema.plot_graficos_de_barras(sistema.build_histogram(img))
sistema.rgb_matriz_to_image(img).show()