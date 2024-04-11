import sistema

from PIL import Image

img = Image.new("RGB", (225, 225), (25, 255, 25))
sistema.save_image(sistema.image_to_rgb_matriz(img), "bloco.png")
sistema.tranfereS("bloco.png",
                  "Images/lenna.jpg",
                  "teste_transfer.png")
