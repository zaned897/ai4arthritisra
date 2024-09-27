import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen en escala de grises
img = cv2.imread('data/532_OR_44_index0.tif', cv2.IMREAD_GRAYSCALE)

# Crear una máscara para los píxeles negros
black_mask = img == 0

# Normalizar la imagen para que los valores estén entre 0 y 1
img_norm = img.astype(float) / 255.0

# Crear un mapa de colores personalizado
# El primer color es negro, los siguientes van desde azul (profundo) hasta rojo (superficial)
colors = ['black', 'navy', 'blue', 'cyan', 'yellow', 'red']
n_bins = 256  # Número de bins para el mapa de colores
cmap = plt.cm.colors.LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

# Aplicar el mapa de colores a la imagen normalizada
img_color = cmap(img_norm)

# Convertir de RGBA a RGB
img_color = (img_color[:, :, :3] * 255).astype(np.uint8)

# Aplicar la máscara de píxeles negros
img_color[black_mask] = [0, 0, 0]

# Mostrar la imagen original en escala de grises y la imagen con color falso
plt.figure(figsize=(12, 6))

plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Imagen original en escala de grises')
plt.axis('off')

plt.subplot(122)
plt.imshow(img_color)
plt.title('Imagen con color falso')
plt.axis('off')

plt.tight_layout()
plt.show()

# Guardar la imagen procesada
#cv2.imwrite('imagen_procesada.png', cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR))