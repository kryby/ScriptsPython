import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from docx import Document
from docx.shared import Inches

def reducir_resolucion(imagen, tamano_maximo):
    # Obtener la resolución DPI original de la imagen
    dpi_original = imagen.info.get("dpi", (96, 96))

    while True:
        # Calcular el factor de escala para ajustar el tamaño del archivo
        factor_escala = (tamano_maximo / len(imagen.tobytes())) ** 0.5

        # Reducir la resolución DPI
        nuevo_dpi = (int(dpi_original[0] * factor_escala), int(dpi_original[1] * factor_escala))
        imagen.info["dpi"] = nuevo_dpi

        # Guardar la imagen reducida en la carpeta temporal
        imagen_temporal = imagen.copy()
        imagen_temporal.save(tempfile.mktemp(), dpi=nuevo_dpi)

        # Verificar si el tamaño de la imagen reducida es menor o igual al límite máximo
        if len(imagen_temporal.tobytes()) <= tamano_maximo:
            return imagen_temporal, nuevo_dpi

def procesar_imagenes(ruta_carpeta, tamano_maximo_mb):
    # Crear una carpeta temporal para procesar las imágenes
    carpeta_temporal = tempfile.mkdtemp()

    # Crear el documento de Word
    doc = Document()

    # Tamaño máximo del archivo de Word en bytes
    tamano_maximo_doc = tamano_maximo_mb * 1024 * 1024  # Convertir a bytes

    # Obtener la lista de archivos en la carpeta de imágenes
    archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".jpg")]

    # Iterar sobre cada archivo en la carpeta de imágenes
    for archivo in archivos:
        try:
            # Abrir la imagen original
            ruta_imagen_original = os.path.join(ruta_carpeta, archivo)
            imagen_original = Image.open(ruta_imagen_original)

            # Reducir la resolución de la imagen si es necesario
            imagen_reducida, nuevo_dpi = reducir_resolucion(imagen_original, tamano_maximo_doc)

            # Guardar la imagen reducida en la carpeta temporal
            ruta_imagen_temporal = os.path.join(carpeta_temporal, archivo)
            imagen_reducida.save(ruta_imagen_temporal, dpi=nuevo_dpi)

            # Agregar la imagen al documento de Word
            doc.add_picture(ruta_imagen_temporal, width=Inches(6))  # Ajustar ancho de la imagen

        except Exception as e:
            print("Error procesando la imagen:", e)
            continue

    # Guardar el documento de Word
    ruta_docx = os.path.join(ruta_carpeta, "unidos.docx")
    doc.save(ruta_docx)

    # Obtener el tamaño del documento de Word
    tamano_doc = os.path.getsize(ruta_docx)

    # Mostrar mensaje si el tamaño del documento es superior al límite
    if tamano_doc > tamano_maximo_doc:
        messagebox.showwarning("Advertencia", f"El tamaño del documento ({tamano_doc / (1024 * 1024):.2f} MB) "
                                              f"supera el límite de {tamano_maximo_mb} MB.")

def seleccionar_carpeta():
    ruta_carpeta = filedialog.askdirectory()
    entry_carpeta.delete(0, tk.END)
    entry_carpeta.insert(0, ruta_carpeta)

def procesar():
    ruta_carpeta = entry_carpeta.get()
    tamano_maximo_mb = float(entry_tamano.get())
    
    try:
        procesar_imagenes(ruta_carpeta, tamano_maximo_mb)
        messagebox.showinfo("Proceso completado", "El proceso ha finalizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error durante el procesamiento: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Procesador de Imágenes")

# Crear los widgets
label_carpeta = tk.Label(root, text="Carpeta de imágenes:")
entry_carpeta = tk.Entry(root, width=50)
button_seleccionar = tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta)

label_tamano = tk.Label(root, text="Tamaño máximo del documento (MB):")
entry_tamano = tk.Entry(root, width=10)
entry_tamano.insert(0, "10")

button_procesar = tk.Button(root, text="Procesar", command=procesar)

# Posicionar los widgets en la ventana
label_carpeta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_carpeta.grid(row=0, column=1, padx=5, pady=5)
button_seleccionar.grid(row=0, column=2, padx=5, pady=5)

label_tamano.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_tamano.grid(row=1, column=1, padx=5, pady=5)

button_procesar.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
