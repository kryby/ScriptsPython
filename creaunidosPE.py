import os
import shutil
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from docx import Document
from docx.shared import Inches
from tkinter import ttk

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

def comprimir_imagenes(ruta_carpeta, tamano_maximo_mb, progreso, doc, label_estado):
    # Crear una carpeta temporal para procesar las imágenes
    carpeta_temporal = tempfile.mkdtemp()
    
    # Obtener la lista de archivos en la carpeta de imágenes
    archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".jpg")]
    archivos_ordenados = sorted(archivos, key=lambda x: int(os.path.splitext(x)[0]))

    total_imagenes = len(archivos_ordenados)

    # Tamaño máximo del archivo de Word en bytes
    tamano_maximo = tamano_maximo_mb * 1024 * 1024

    # Tamaño actual del archivo de Word
    tamano_actual = 0
    imagenes_procesadas = 0

    # Barra de progreso
    progreso.config(maximum=total_imagenes, value=0)
    
    # Iterar sobre cada archivo en la carpeta de imágenes
    for archivo in archivos_ordenados:
        # Abrir la imagen
        ruta_imagen_original = os.path.join(ruta_carpeta, archivo)
        imagen_original = Image.open(ruta_imagen_original)

        # Copiar la imagen original a la carpeta temporal
        ruta_imagen_temporal = os.path.join(carpeta_temporal, archivo)
        shutil.copyfile(ruta_imagen_original, ruta_imagen_temporal)

        # Reducir la resolución a la mitad hasta que el tamaño del archivo sea inferior al máximo permitido
        while os.path.getsize(ruta_imagen_temporal) > tamano_maximo:
            imagen = Image.open(ruta_imagen_temporal)
            nueva_resolucion = (int(imagen.width / 2), int(imagen.height / 2))
            imagen.thumbnail(nueva_resolucion)
            imagen.save(ruta_imagen_temporal, quality=85, dpi=(96, 96))

        # Obtener el tamaño de la imagen comprimida
        tamano_imagen = os.path.getsize(ruta_imagen_temporal)

        # Agregar la imagen al documento de Word si no excede el tamaño máximo
        if tamano_actual + tamano_imagen < tamano_maximo:
            imagen_ajustada = ajustar_tamano(imagen_original)
            parrafo = doc.add_paragraph()
            parrafo.alignment = 1  # Centrado
            run = parrafo.add_run()
            run.add_picture(ruta_imagen_temporal, width=Inches(6))  # Ajustar ancho de la imagen
            tamano_actual += tamano_imagen

        # Actualizar el progreso y el estado
        imagenes_procesadas += 1
        progreso.config(value=imagenes_procesadas)
        progreso.update()
        label_estado.config(text=f"Procesando imagen {imagenes_procesadas} de {total_imagenes}")

    # Guardar el documento de Word
    ruta_docx = os.path.join(ruta_carpeta, "unidos.docx")
    if os.path.exists(ruta_docx):
        os.remove(ruta_docx)
    doc.save(ruta_docx)

    # Eliminar la carpeta temporal
    shutil.rmtree(carpeta_temporal)

    # Mostrar mensaje de finalización
    messagebox.showinfo("Proceso terminado", "El proceso ha terminado correctamente.")

def seleccionar_carpeta():
    ruta_carpeta = filedialog.askdirectory()
    entry_carpeta.delete(0, tk.END)
    entry_carpeta.insert(0, ruta_carpeta)

def procesar_imagenes():
    ruta_carpeta = entry_carpeta.get()
    tamano_maximo_mb = int(entry_tamano.get())
    
    progreso.start()
    
    # Crear el documento de Word
    doc = Document()
    
    # Crear etiqueta de estado
    label_estado = tk.Label(root, text="")
    label_estado.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    try:
        comprimir_imagenes(ruta_carpeta, tamano_maximo_mb, progreso, doc, label_estado)
    except Exception as e:
        print("Error:", e)
        progreso.stop()

    # Detener la barra de progreso
    progreso.stop()

# Crear la ventana principal
root = tk.Tk()
root.title("Procesador de Imágenes")

# Crear los widgets
label_carpeta = tk.Label(root, text="Carpeta de imágenes:")
entry_carpeta = tk.Entry(root, width=50)
button_seleccionar = tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta)

label_tamano = tk.Label(root, text="Tamaño máximo del archivo Word (MB):")
entry_tamano = tk.Entry(root, width=10)
entry_tamano.insert(tk.END,"30") # el tamaño por defecto lo ponemos en 30mb 

button_procesar = tk.Button(root, text="Procesar Imágenes", command=procesar_imagenes)

progreso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

# Posicionar los widgets en la ventana
label_carpeta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_carpeta.grid(row=0, column=1, padx=5, pady=5)
button_seleccionar.grid(row=0, column=2, padx=5, pady=5)

label_tamano.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_tamano.grid(row=1, column=1, padx=5, pady=5)

button_procesar.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

progreso.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
