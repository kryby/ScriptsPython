import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

class PDFCompressorWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, input_path, magick_path, ghostscript_path, max_size, max_attempts):
        super().__init__()
        self.input_path = input_path
        self.magick_path = magick_path
        self.ghostscript_path = ghostscript_path
        self.max_size = max_size
        self.max_attempts = max_attempts

    def run(self):
        for attempt in range(1, self.max_attempts + 1):
            self.progress.emit(int((attempt / self.max_attempts) * 100))  # Actualiza la barra de progreso
            output_path = os.path.splitext(self.input_path)[0] + f'_compressed_attempt{attempt}.pdf'
            command = (
                f'"{self.magick_path}" "{self.input_path}" -compress jpeg -quality 90 '
                f'-define pdf:use-trimbox=true -define pdf:use-cropbox=true '
                f'-define delegate:gscommand="{self.ghostscript_path}" "{output_path}"'
            )
            try:
                subprocess.run(command, shell=True, check=True)
                compressed_size = os.path.getsize(output_path)
                if compressed_size <= self.max_size:
                    self.finished.emit(output_path)
                    return
            except Exception as e:
                print(f"Error en el intento {attempt}: {e}")

        self.finished.emit("No se pudo comprimir satisfactoriamente.")


class PDFCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Compressor')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Selecciona un archivo PDF')
        layout.addWidget(self.label)

        self.compressBtn = QPushButton('Comprimir PDF')
        self.compressBtn.clicked.connect(self.compressPDF)
        layout.addWidget(self.compressBtn)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

    def compressPDF(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecciona un archivo PDF', '', 'PDF Files (*.pdf)')
        if file_path:
            magick_path = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
            ghostscript_path = r'C:\Program Files\gs\gs9.xx\bin\gswin64c.exe'
            max_size = 19000000  # 19 MB
            max_attempts = 3

            self.worker = PDFCompressorWorker(file_path, magick_path, ghostscript_path, max_size, max_attempts)
            self.worker.progress.connect(self.updateProgress)
            self.worker.finished.connect(self.onCompressionFinished)
            self.worker.start()
            self.label.setText("Comenzando la compresión...")

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def onCompressionFinished(self, result):
        self.label.setText(f'Resultado: {result}')
        self.progressBar.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFCompressor()
    window.show()
    sys.exit(app.exec_())
