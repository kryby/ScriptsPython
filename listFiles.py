from os import walk
from tkinter import Tk
from tkinter.filedialog import askdirectory

# folder path
dir_path = askdirectory(title='Select source folder')

# list to store files name
res = []
for (dir_path, dir_names, file_names) in walk(dir_path):
    res.extend(file_names)
print(res)