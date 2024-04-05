from Services.Correlacao import correlacao
from PIL import  Image
import  Util.Util as ut

img = Image.open("Images/testpat.1k.color2.tif")
img.show()
img = ut.image_to_rgb_matriz(img)
mask = ut.read_mask_from_file("masks/gaussian_5x5.txt")
img_final = correlacao(img, mask)
imgF = ut.rgb_matriz_to_image(img_final)
imgF.show()
