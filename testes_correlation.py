import sistema

# os resultados não são imagens
gauss = sistema.makecorelation("Images/lenna.jpg",
                               "masks/gaussian_5x5.txt")
box_1x26 = sistema.makecorelation("Images/DancingInWater.jpg",
                                   "masks/box_1x26.txt")

sobel_horizontal = sistema.makecorelation("Images/img2.jpg",
                                          "masks/sobel_horizontal.txt")
sobel_vertical = sistema.makecorelation("Images/img2.jpg",
                                        "masks/sobel_vertical.txt")
#transformando os resultados em imagens

gauss = sistema.processamento_para_exibir_imagem(gauss)
box_1x26 = sistema.processamento_para_exibir_imagem(box_1x26)

#processamento definido na especificação para exibir sobel:

sobel_horizontal = sistema.processamento_valor_absoluto(sobel_horizontal)
sobel_horizontal = sistema.histogram_expansion(sobel_horizontal)
sobel_horizontal = sistema.processamento_para_exibir_imagem(sobel_horizontal)
sobel_vertical = sistema.processamento_valor_absoluto(sobel_vertical)
sobel_vertical = sistema.histogram_expansion(sobel_vertical)
sobel_vertical = sistema.processamento_para_exibir_imagem(sobel_vertical)

sistema.save_image(gauss, "gauss 5x5.png")
sistema.save_image(box_1x26, "box 1x26.png")
sistema.save_image(sobel_horizontal, "sobel horizontal.png")
sistema.save_image(sobel_vertical, "sobel vertical.png")
