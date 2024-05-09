import PyPDF2
import tkinter as tk
from tkinter import filedialog

def remove_print_protection(input_path, output_path, password):
    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt(password)
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                if '/Perms' in page:
                    if '/Print' in page['/Perms']:
                        page['/Perms'].update({PyPDF2.generic.NameObject('/Print'): PyPDF2.generic.BooleanObject(False)})
                pdf_writer.add_page(page)
            pdf_writer.write(output_file)
        else:
            print("El PDF no está protegido.")

def select_input_file():
    input_path = filedialog.askopenfilename(title="Seleccionar archivo PDF")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)

def select_output_file():
    output_path = filedialog.asksaveasfilename(title="Guardar como", defaultextension=".pdf")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_path)

def process_pdf():
    input_path = input_entry.get()
    output_path = output_entry.get()
    password = password_entry.get()

    if input_path and output_path and password:
        remove_print_protection(input_path, output_path, password)
        result_label.config(text="Proceso completado. El PDF resultante se guardó en: " + output_path)
    else:
        result_label.config(text="Por favor, complete todos los campos.")

# Crear la ventana principal
window = tk.Tk()
window.title("Remover Protección de Impresión de PDF")

# Crear y colocar widgets
input_label = tk.Label(window, text="Seleccione el archivo PDF:")
input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

input_entry = tk.Entry(window, width=50)
input_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

input_button = tk.Button(window, text="Seleccionar", command=select_input_file)
input_button.grid(row=0, column=3, padx=5, pady=5)

output_label = tk.Label(window, text="Guardar como:")
output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

output_entry = tk.Entry(window, width=50)
output_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

output_button = tk.Button(window, text="Seleccionar", command=select_output_file)
output_button.grid(row=1, column=3, padx=5, pady=5)

password_label = tk.Label(window, text="Contraseña:")
password_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

password_entry = tk.Entry(window, show="*")
password_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

process_button = tk.Button(window, text="Procesar", command=process_pdf)
process_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

result_label = tk.Label(window, text="")
result_label.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

# Ejecutar la ventana
window.mainloop()
