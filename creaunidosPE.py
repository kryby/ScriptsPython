import os
from PIL import Image
from docx import Document
from docx.shared import Inches
from tqdm import tqdm

def ajustar_tamano(imagen):
    # Dimensiones de una página A4 en centímetros
    ancho_pagina = 21  # cm
    alto_pagina = 29.7  # cm
    
    # Calcular el factor de escala para ajustar la imagen al tamaño de la página
    factor_ancho = ancho_pagina / float(imagen.width)
    factor_alto = alto_pagina / float(imagen.height)
    factor_escala = min(factor_ancho, factor_alto)
    
    # Ajustar el tamaño de la imagen
    nueva_ancho = int(imagen.width * factor_escala)
    nueva_alto = int(imagen.height * factor_escala)
    
    return imagen.resize((nueva_ancho, nueva_alto))

def comprimir_imagenes(ruta_carpeta):
    # Crear un nuevo documento de Word
    doc = Document()

    # Obtener la lista de archivos en la carpeta de imágenes y ordenarlos por nombre numérico
    archivos = sorted(os.listdir(ruta_carpeta), key=lambda x: int(os.path.splitext(x)[0]))

    # Calcular el tamaño máximo del archivo de Word en bytes (80 MB)
    tamano_maximo = 80 * 1024 * 1024

    # Tamaño actual del archivo de Word
    tamano_actual = 0

    # Barra de progreso
    with tqdm(total=len(archivos), desc="Procesando imágenes") as pbar:
        # Iterar sobre cada archivo en la carpeta de imágenes
        for archivo in archivos:
            if archivo.endswith(".jpg"):
                # Abrir la imagen
                ruta_imagen = os.path.join(ruta_carpeta, archivo)
                imagen = Image.open(ruta_imagen)

                # Reducir la resolución a la mitad hasta que el tamaño del archivo sea inferior al máximo permitido
                while os.path.getsize(ruta_imagen) > tamano_maximo:
                    nueva_resolucion = (int(imagen.width / 2), int(imagen.height / 2))
                    imagen.thumbnail(nueva_resolucion)

                    # Guardar la imagen con la nueva resolución
                    imagen.save(ruta_imagen, quality=85, dpi=(96, 96))

                # Obtener el tamaño de la imagen comprimida
                tamano_imagen = os.path.getsize(ruta_imagen)

                # Agregar la imagen al documento de Word si no excede el tamaño máximo
                if tamano_actual + tamano_imagen < tamano_maximo:
                    # Ajustar tamaño y centrar la imagen
                    imagen_ajustada = ajustar_tamano(imagen)
                    parrafo = doc.add_paragraph()
                    parrafo.alignment = 1  # Centrado
                    run = parrafo.add_run()
                    run.add_picture(ruta_imagen, width=Inches(6))  # Ajustar ancho de la imagen
                    tamano_actual += tamano_imagen

                # Actualizar la barra de progreso
                pbar.update(1)
                pbar.set_postfix({"Imagen": archivo})

    # Guardar el documento de Word
    doc.save(os.path.join(ruta_carpeta, "unidos.docx"))

if __name__ == "__main__":
    ruta_carpeta = input("Ingrese la ruta de la carpeta de imágenes: ")
    comprimir_imagenes(ruta_carpeta)
