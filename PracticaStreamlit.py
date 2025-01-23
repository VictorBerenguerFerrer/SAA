import streamlit as st
from PIL import Image, ImageEnhance
import cv2
import numpy as np

# Título de la página
st.title("Editor de Imágenes con Streamlit")

# Subir una imagen (cargada por el código)
image_original = Image.open("C:/Users/Estudiant/Desktop/PracticaStreamlit2/imagen.JPG")

# Mostrar la imagen original
st.sidebar.header("Controles")
st.image(image_original, caption="Imagen Original", use_column_width=True)

# Copia de la imagen para modificaciones (sin afectar la original)
image_to_modify = image_original.copy()

# ---------------- Imagen Escalada (Por Píxeles) ----------------
# Usar sliders para controlar el tamaño de la imagen
max_width, max_height = image_original.size
new_width = st.sidebar.slider("Ancho (px):", min_value=1, max_value=max_width, value=max_width)
new_height = st.sidebar.slider("Alto (px):", min_value=1, max_value=max_height, value=max_height)

# Redimensionar la imagen en tiempo real
image_scaled = image_original.resize((new_width, new_height))
st.image(image_scaled, caption=f"Imagen Redimensionada ({new_width}x{new_height})", use_column_width=True)

# ---------------- Modificaciones (Brillo, Contraste, etc.) ----------------
# Brillo
brightness = st.sidebar.slider("Ajustar Brillo", 0.5, 2.0, 1.0)
enhancer = ImageEnhance.Brightness(image_to_modify)
image_bright = enhancer.enhance(brightness)

# Contraste
contrast = st.sidebar.slider("Ajustar Contraste", 0.5, 2.0, 1.0)
enhancer = ImageEnhance.Contrast(image_bright)
image_contrast = enhancer.enhance(contrast)

# Desenfoque
blur = st.sidebar.slider("Nivel de Desenfoque", 0, 10, 0)
if blur > 0:
    img_cv = cv2.GaussianBlur(np.array(image_contrast), (blur * 2 + 1, blur * 2 + 1), 0)
    image_blur = Image.fromarray(img_cv)
else:
    image_blur = image_contrast

# Convertir a Grises
if st.sidebar.checkbox("Convertir a Escala de Grises"):
    image_modified = image_blur.convert("L")
else:
    image_modified = image_blur

# Mostrar la imagen modificada
st.image(image_modified, caption="Imagen Modificada", use_column_width=True)

# ---------------- Conversión a HSV (Botón) ----------------
# Convertir a HSV
def convert_rgb_to_hsv(img):
    img_cv = np.array(img)
    img_hsv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2HSV)
    return Image.fromarray(img_hsv)

if st.sidebar.button("Convertir a HSV"):
    image_hsv = convert_rgb_to_hsv(image_modified)
    st.image(image_hsv, caption="Imagen en HSV", use_column_width=True)
