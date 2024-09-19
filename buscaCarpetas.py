import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from threading import Thread

class FolderSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Carpetas")

        self.directory = tk.StringVar()
        self.folder_name = tk.StringVar()

        self.create_widgets()
        
    def create_widgets(self):
        # Etiqueta y campo para seleccionar el directorio raíz
        tk.Label(self.root, text="Directorio raíz:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.directory, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Seleccionar", command=self.browse_directory).grid(row=0, column=2, padx=10, pady=10)
        
        # Etiqueta y campo para especificar el nombre de la carpeta a buscar
        tk.Label(self.root, text="Nombre de la carpeta:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.folder_name, width=50).grid(row=1, column=1, padx=10, pady=10)
        
        # Botón para iniciar la búsqueda
        tk.Button(self.root, text="Buscar", command=self.start_search).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Barra de progreso
        self.progress = Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        # Campo de texto para mostrar los resultados
        self.result_text = tk.Text(self.root, width=60, height=15)
        self.result_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)

    def start_search(self):
        self.result_text.delete(1.0, tk.END)
        directory = self.directory.get()
        folder_name = self.folder_name.get()
        self.result_text.insert(tk.END, f"Iniciando la busqueda:\n")
        if not directory or not folder_name:
            messagebox.showwarning("Advertencia", "Debe seleccionar un directorio y especificar el nombre de la carpeta.")
            return
        
        thread = Thread(target=self.search_folders, args=(directory, folder_name))
        thread.start()

    def search_folders(self, base_path, folder_name):
        rutas = []
        total = sum([len(dirs) for _, dirs, _ in os.walk(base_path)])
        count = 0
        
        for root, dirs, files in os.walk(base_path):
            for dir in dirs:
                count += 1
                if dir.lower() == folder_name.lower():
                    rutas.append(os.path.join(root, dir))
                self.update_progress(count, total)
        
        self.display_results(rutas)
    
    def update_progress(self, count, total):
        porcentaje = (count / total) * 100
        self.progress['value'] = porcentaje
        self.root.update_idletasks()
    
    def display_results(self, rutas):
        self.result_text.insert(tk.END, f"Se encontraron {len(rutas)} carpetas:\n")
        for ruta in rutas:
            self.result_text.insert(tk.END, f"{ruta}\n")
        messagebox.showinfo("Búsqueda completada", f"Se encontraron {len(rutas)} carpetas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSearchApp(root)
    root.mainloop()

