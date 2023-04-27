import os
import shutil
from tkinter import filedialog, Tk

# Abrir ventana de diálogo para seleccionar el archivo original
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Documentos de Word", "*.ANE.DOCX")])

# Abrir ventana de diálogo para seleccionar la carpeta donde guardar las copias
root = Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

# Preguntar el primer y último número para los nombres de archivo
first_num = int(input("Protocolo inicial: "))
last_num = int(input("Protocolo final: "))

# Obtener la extensión del archivo original
extension = ".ANE.DOCX"

# Copiar el archivo múltiples veces con nombres de archivo diferentes
for i in range(first_num, last_num+1):
    new_file_name = str(i).zfill(8) + extension
    shutil.copy(file_path, os.path.join(folder_path, new_file_name))
