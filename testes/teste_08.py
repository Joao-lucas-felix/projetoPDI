import sistema
from PIL import Image

img = Image.open("Images/lenna.jpg")
img.show()
img = sistema.image_to_rgb_matriz(img)
img = sistema.correlacao(img, sistema.read_mask_from_file("masks/box_1x26.txt"))
img = sistema.processamento_para_exibir_imagem(img)
img = sistema.rgb_matriz_to_image(img)
img.show()
