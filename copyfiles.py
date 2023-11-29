import tkinter as tk
from tkinter import filedialog
import shutil

# Función para seleccionar el archivo con extensión .txt
def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(filetypes=[('Archivos de texto', '*.txt')])
    return archivo

# Función para seleccionar el directorio de destino
def seleccionar_directorio():
    root = tk.Tk()
    root.withdraw()
    directorio = filedialog.askdirectory()
    return directorio

# Obtener la ruta del archivo de texto con los paths
archivo_paths = seleccionar_archivo()

# Obtener el directorio de destino
directorio_destino = seleccionar_directorio()

# Copiar los archivos indicados en el directorio de destino
with open(archivo_paths, 'r') as file:
    for line in file:
        archivo_origen = line.strip()  # Eliminar espacios en blanco al inicio y final de la línea
        shutil.copy(archivo_origen, directorio_destino)
        print(f"Archivo {archivo_origen} copiado correctamente a {directorio_destino}")
