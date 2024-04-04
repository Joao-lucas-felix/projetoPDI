import sistema
from PIL import Image

img = Image.open("Images/Shapes.png")
img.show()
img = sistema.image_to_rgb_matriz(img)
img = sistema.correlacao(img, sistema.read_mask_from_file("masks/sobel1.txt"))
img = sistema.processamento_para_exibir_imagem(sistema.processamento_valor_absoluto(img))
img = sistema.rgb_matriz_to_image(img)
img.show()

img = Image.open("Images/Shapes.png")
img = sistema.image_to_rgb_matriz(img)
img = sistema.correlacao(img, sistema.read_mask_from_file("masks/sobel2.txt"))
img = sistema.processamento_para_exibir_imagem(sistema.processamento_valor_absoluto(img))
img = sistema.rgb_matriz_to_image(img)
img.show()