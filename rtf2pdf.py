import os
import shutil
import subprocess
import winreg

# Replace with the path to the folder containing the RTF files
folder_path = "G:\PerfilUsuario\Descargas"

# Open the HKEY_LOCAL_MACHINE root key
root_key = winreg.HKEY_LOCAL_MACHINE

# Open the "Software" key
software_key = winreg.OpenKey(root_key, "Software")

# Open the "Microsoft" key
microsoft_key = winreg.OpenKey(software_key, "Microsoft")

# Open the "Windows" key
windows_key = winreg.OpenKey(microsoft_key, "Windows")

# Open the "CurrentVersion" key
current_version_key = winreg.OpenKey(windows_key, "CurrentVersion")

# Open the "App Paths" key
app_paths_key = winreg.OpenKey(current_version_key, "App Paths")

# Open the "WINWORD.EXE" key
winword_key = winreg.OpenKey(app_paths_key, "WINWORD.EXE")

# Read the (default) value of the WINWORD.EXE key
winword_path = winreg.QueryValue(winword_key, None)
# Replace with the full path to the winword executable


# Check if Microsoft Word is installed
if not os.path.exists(winword_path):
  print("Microsoft Word is not installed on this system.")
  print("Please install it and try again.")
  exit(1)

# Loop through all files in the specified folder
for filename in os.listdir(folder_path):
  # Check if the file has the RTF file extension
  if filename.endswith(".rtf"):
    # Construct the full file path
    file_path = os.path.join(folder_path, filename)

    # Call Microsoft Word to convert the RTF file to PDF
    subprocess.check_call([winword_path, "/q", "/n", "/mFilePrintDefault ", file_path])
