from cmath import e
import subprocess
import shutil
from colorama import Fore #pip3 install colorama
from tkinter.filedialog import  askopenfilename

userName = input('Nombre de usuario: ')
userPassword = input('Password: ')
#Loading file with names to search
file = askopenfilename()
fileobj = open(file)
workStations=[]
for line in fileobj:
    workStations.append(line.strip())

for workStation in workStations:
    networkDrive = '\\\\' + workStation + '\\NETWORKSHARE'
    winCMD = 'NET USE ' + networkDrive + ' /User:' + userName + ' ' + userPassword
    process = subprocess.Popen(winCMD, stdout=subprocess.PIPE, shell=True)
    process.wait()
    try:
        shutil.copy2('FILETOCOPY',networkDrive+'\\FILENAMEDESTINATION')
        print (Fore.GREEN + "Archivo copiado correctamente a: "+ workStation)
    except IOError as e :
        print (Fore.RED + "Error copiando archivo. %s" % e)
