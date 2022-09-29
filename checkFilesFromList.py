import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfile, askopenfilename

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths(askdirectory(title='Select source folder'))
onlyNames = []
for file in full_file_paths:
    filename, file_extension = os.path.splitext(os.path.basename(file))
    onlyNames.append(filename)
    #print(filename)
#Loading file with names to search
file = askopenfilename()
fileobj = open(file)
lines=[]
for line in fileobj:
    lines.append(line.strip())

for line in lines:
    exist_count =onlyNames.count(line)
    if(exist_count==0):
        print("File not found: " + line)

print("Process completed")
