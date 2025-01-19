import win32com.client

# Iniciar una instancia de Word de manera invisible
word_app = win32com.client.Dispatch("Word.Application")
word_app.Visible = False

# Cargar la plantilla normal.dotm
normal_template = word_app.NormalTemplate

try:
    # Crear la combinación de teclas Ctrl+N para aplicar formato negrita
    # 11 es wdKeyControl, 78 es N
    # Cambiamos wdKeyN (78) a su constante interna si es necesario
    key_code_ctrl_n = word_app.BuildKeyCode(11, 78)  # 11 es wdKeyControl, 78 es N
    word_app.KeyBindings.Add(KeyCategory=1,  # wdKeyCategoryCommand
                             Command="Bold",
                             KeyCode=key_code_ctrl_n)

    # Guardar la plantilla normal.dotm
    normal_template.Save()
    print("La combinación Ctrl+N se ha asignado correctamente para aplicar negrita.")

except Exception as e:
    print(f"Error al asignar la combinación de teclas: {e}")

finally:
    word_app.Quit()



