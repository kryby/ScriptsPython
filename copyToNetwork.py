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
    networkDrive = '\\\\' + workStation + '\\c$\\plantillas'
    winCMD = 'NET USE ' + networkDrive + ' /User:' + userName + ' ' + userPassword
    subprocess.Popen(winCMD, stdout=subprocess.PIPE, shell=True)
    try:
        shutil.copy2('f:\\notin\\plantillas\\normal.dotm',networkDrive+'\\normal.dotm')
        print (Fore.GREEN + "Archivo copiado correcatente a: "+ workStation)
    except IOError as e :
        print (Fore.RED + "Error copiando archivo. %s" % e)
