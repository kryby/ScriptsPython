import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from docx import Document
from docx.shared import Inches
import shutil
import tempfile
import win32com.client

def compress_and_generate_doc():
    # Obtener la ruta de la carpeta de imágenes
    folder_path = folder_path_var.get()
    
    # Obtener el tamaño máximo del documento
    max_size_mb = float(max_size_mb_var.get() or "100")
    
    # Validar la existencia de la carpeta
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "La carpeta seleccionada no existe.")
        return
    
    # Crear una carpeta temporal para procesar las imágenes
    temp_folder = tempfile.mkdtemp()
    
    # Calcular el tamaño máximo por archivo
    max_size_kb = calculate_max_file_size(folder_path, max_size_mb)
    if max_size_kb < 50:
        max_size_kb = 50
    
    # Ajustar imágenes y generar documento
    adjust_images_and_generate_doc(folder_path, temp_folder, max_size_kb)

def calculate_max_file_size(folder_path, max_size_mb):
    num_files = len([file for file in os.listdir(folder_path) if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))])
    max_size_bytes = max_size_mb * 1024 * 1024
    max_size_kb_per_file = max_size_bytes / num_files / 1024
    return max_size_kb_per_file

def adjust_images_and_generate_doc(folder_path, temp_folder, max_size_kb):
    # Obtener la lista de archivos ordenada por nombres
    files = sorted([file for file in os.listdir(folder_path) if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))], key=lambda x: int(os.path.splitext(x)[0]))
    
    # Copiar las imágenes a la carpeta temporal
    progress_window_copy_files = tk.Toplevel(root)
    progress_window_copy_files.title("Progreso")
    progress_window_copy_files.geometry("400x100")
    progress_label_copy_files = tk.Label(progress_window_copy_files,text="Copiando imagenes a carpeta temporal...")
    progress_label_copy_files.pack(pady=10)
    progress_bar_copy_files=ttk.Progressbar(progress_window_copy_files,orient=tk.HORIZONTAL,mode='determinate')
    progress_bar_copy_files.pack(expand=True, fill='both')
    progress_bar_copy_files['maximum'] = len(files)

    for i, file in enumerate(files):
        progress_label_copy_files.config(text=f"Copiando imagen {file}")
        shutil.copy(os.path.join(folder_path, file), temp_folder)
        progress_bar_copy_files["value"] = i + 1
        progress_window_copy_files.update()

    progress_window_copy_files.destroy()
    # Ajustar imágenes y generar documento
    progress_window = tk.Toplevel(root)
    progress_window.title("Progreso")
    progress_window.geometry("400x100")
    progress_label = tk.Label(progress_window, text="Procesando imágenes...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, mode='determinate')
    progress_bar.pack(expand=True, fill='both')
    progress_bar["maximum"] = len(files)
    
    for i, file in enumerate(files):
        file_path = os.path.join(temp_folder, file)
        image = Image.open(file_path)
        factor_compression = 1.0
        while os.path.getsize(file_path) > max_size_kb * 1024:
            progress_label.config(text=f"Procesando imagen {file}, tamaño actual {os.path.getsize(file_path)}")
            factor_compression -= 0.4
            image.save(file_path, quality=int(75 * factor_compression))
            if factor_compression < 0.1:
                # si llegamos aun factor de compresión insignificante pero el tamaño de la imagen
                # aún es muy grande, modificamos a escala de grises y resolución a la mitad.
                image_grises = image.convert("L")
                nuevo_ancho = image.width//2
                nuevo_alto = image.height//2
                imagen_redimensionada = image_grises.resize((nuevo_ancho,nuevo_alto))
                imagen_redimensionada.save(file_path)
                image = Image.open(file_path)
        progress_bar["value"] = i + 1
        progress_window.update()
        image.close()
    progress_window.destroy() 


    # Generar documento
    doc = Document()
    progress_window_doc = tk.Toplevel(root)
    progress_window_doc.title("Progreso")
    progress_window_doc.geometry("400x100")
    progress_label_doc = tk.Label(progress_window_doc, text="Generando archivo...")
    progress_label_doc.pack(pady=10)
    progress_bar_doc = ttk.Progressbar(progress_window_doc, orient=tk.HORIZONTAL, mode='determinate')
    progress_bar_doc.pack(expand=True, fill='both')
    progress_bar_doc["maximum"] = len(files)

    for i,file in enumerate(files):
        progress_label_doc.config(text=f"Insertando imagen {file}")
        file_path = os.path.join(temp_folder, file)
        doc.add_picture(file_path, width=Inches(6))
        progress_bar_doc["value"] = i + 1
        progress_window_doc.update()
    doc_path = os.path.join(folder_path, 'unidos.docx')
    doc.save(doc_path)
    progress_label_doc.config(text=f"Asegurando compatibilidad del documento.")
    fix_compatibility_mode(doc_path)
    progress_window_doc.destroy()
    messagebox.showinfo("Éxito", f"Documento Word creado correctamente en {doc_path}.")
    
    # Eliminar la carpeta temporal después de procesar las imágenes
    shutil.rmtree(temp_folder)
    
    # Cerrar la ventana de progreso
def fix_compatibility_mode(docx_path):
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(docx_path)
    doc.Convert()
    doc.Save()
    doc.Close()
    word.Quit()

# Crear ventana principal
root = tk.Tk()
root.title("Comprimir Imágenes y Generar Documento Word")

# Crear y posicionar widgets
tk.Label(root, text="Ruta de la carpeta de imágenes:").grid(row=0, column=0, padx=5, pady=5)
folder_path_var = tk.StringVar()
folder_path_entry = tk.Entry(root, textvariable=folder_path_var, width=50)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Seleccionar Carpeta", command=lambda: folder_path_var.set(filedialog.askdirectory())).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Tamaño máximo del documento (MB):").grid(row=1, column=0, padx=5, pady=5)
max_size_mb_var = tk.StringVar(value=100)

max_size_mb_entry = tk.Entry(root, textvariable=max_size_mb_var)

max_size_mb_entry.grid(row=1, column=1, padx=5, pady=5)

compress_button = tk.Button(root, text="Comprimir y Generar Documento", command=compress_and_generate_doc)
compress_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Ejecutar la aplicación
root.mainloop()
