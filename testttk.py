import tkinter as tk

# Intenta acceder al atributo ttk
try:
    tk.ttk
    print("El módulo ttk está disponible en esta versión de Python.")
except AttributeError:
    print("El módulo ttk no está disponible en esta versión de Python.")
