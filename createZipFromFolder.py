import os, zipfile
from tkinter import Tk
import hashlib
from tkinter.filedialog import askdirectory

name = askdirectory(title='Select source folder') 
zip_name = name + '.zip'

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    for folder_name, subfolders, filenames in os.walk(name):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

zip_ref.close()

 
filename = zip_name
sha256_hash = hashlib.sha256()
with open(filename,"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    print(sha256_hash.hexdigest())
resultFile = os.path.join(os.path.dirname(filename),"HashResults.txt")
with open(resultFile, 'w') as f:
        f.write("Result file name: " + zip_name)
        f.write('\n')
        f.write("Hash: " + sha256_hash.hexdigest())
