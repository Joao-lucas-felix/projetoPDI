import sistema

img = sistema.open_image("Images/testpat.1k.color2.tif")
img_hsv = sistema.image_to_hsb_format(img)
rgb_output_image = sistema.hsb_matriz_to_image(img_hsv)
sistema.save_image(rgb_output_image, "conversão_para_hsv.jpg")

img1 = sistema.open_image("Images/DancingInWater.jpg")
img1_hsv = sistema.image_to_hsb_format(img1)
rgb_output_image1 = sistema.hsb_matriz_to_image(img1_hsv)
sistema.save_image(rgb_output_image1, "conversão_para_hsv1.jpg")
