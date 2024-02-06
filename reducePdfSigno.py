import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import subprocess

class PDFCompressor(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Compressor')
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.label = QLabel('Selecciona un archivo PDF')
        layout.addWidget(self.label)

        self.compressBtn = QPushButton('Comprimir PDF')
        self.compressBtn.clicked.connect(self.compressPDF)
        layout.addWidget(self.compressBtn)

        self.setLayout(layout)

    def compressPDF(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecciona un archivo PDF', '', 'PDF Files (*.pdf)')

        if file_path:
            compressed_file_path = self.compress(file_path)
            self.label.setText(f'Archivo comprimido: {compressed_file_path}')

    def compress(self, input_path):
        max_size = 19000000  # Tamaño máximo en bytes (19 MB)
        max_attempts = 3     # Número máximo de intentos

        for attempt in range(1, max_attempts + 1):
            output_path = os.path.splitext(input_path)[0] + f'_compressed_attempt{attempt}.pdf'

            # Reemplaza las rutas con las rutas completas en tu sistema
            magick_path = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
            ghostscript_path = 'gswin64c'  # Utiliza el ejecutable por defecto de Ghostscript

            # Utiliza ImageMagick para comprimir el PDF con Ghostscript
            command = f'"{magick_path}" convert "{input_path}" -compress jpeg -quality 90 -define pdf:use-trimbox=true -define pdf:use-cropbox=true -define delegate:gscommand="{ghostscript_path}" "{output_path}"'

            try:
                subprocess.run(command, shell=True, check=True)

                # Verifica el tamaño del archivo comprimido
                compressed_size = os.path.getsize(output_path)

                if compressed_size <= max_size:
                    return output_path  # Si el tamaño es aceptable, termina el bucle

            except subprocess.CalledProcessError:
                # Si hay un error al comprimir, imprime un mensaje
                print(f'Error en el intento {attempt}. Intentando de nuevo...')

        return f'No se pudo comprimir satisfactoriamente después de {max_attempts} intentos.'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFCompressor()
    window.show()
    sys.exit(app.exec_())
