import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def convert_heic_to_jpg(heic_folder):
    output_folder = os.path.join(heic_folder, 'JPG')
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(heic_folder):
        if filename.lower().endswith('.heic'):
            heic_path = os.path.join(heic_folder, filename)
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_path = os.path.join(output_folder, jpg_filename)

            try:
                image = Image.open(heic_path)
                image.save(jpg_path, "JPEG")
                print(f'Converted {heic_path} to {jpg_path}')
            except Exception as e:
                print(f'Error converting {heic_path}: {e}')

    messagebox.showinfo("Proceso completado", "Todas las imágenes HEIC se han convertido a JPG.")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        convert_heic_to_jpg(folder_selected)

# Crear la ventana principal
root = Tk()
root.title("Convertidor de HEIC a JPG")

# Etiqueta de instrucciones
label = Label(root, text="Selecciona la carpeta que contiene las imágenes HEIC:")
label.pack(pady=10)

# Botón para seleccionar la carpeta
select_button = Button(root, text="Seleccionar carpeta", command=select_folder)
select_button.pack(pady=10)

# Iniciar el bucle principal de la GUI
root.mainloop()
