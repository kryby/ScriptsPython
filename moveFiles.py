import os
import ctypes  # An included library with Python install.   

from tkinter import Tk
from tkinter.filedialog import askdirectory
source = askdirectory(title='Select source folder') #Shows dialog box and return the path
destination = askdirectory(title='Select destination folder') #Shows dialog box and return the path

if(source and destination):
    # gather all files
    allfiles = os.listdir(source)
    # iterate on all files to move them to destination folder
    for f in allfiles:
        src_path = os.path.join(source, f)
        dst_path = os.path.join(destination, f)
        os.rename(src_path, dst_path)
    ctypes.windll.user32.MessageBoxW(0, "Process completed.", "Result", 1)
else:
    ctypes.windll.user32.MessageBoxW(0, "Error.", "you must select a source and target directory.", 1)