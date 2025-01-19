import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from PyPDF2 import PdfReader
from PIL import Image

class PDFImageExtractorWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, input_path, output_folder):
        super().__init__()
        self.input_path = input_path
        self.output_folder = output_folder

    def run(self):
        try:
            reader = PdfReader(self.input_path)
            total_pages = len(reader.pages)
            image_count = 0

            for page_number, page in enumerate(reader.pages):
                self.progress.emit(int((page_number / total_pages) * 100))
                if "/XObject" in page["/Resources"]:
                    xObject = page["/Resources"]["/XObject"].get_object()
                    for obj in xObject:
                        if xObject[obj]["/Subtype"] == "/Image":
                            size = (xObject[obj]["/Width"], xObject[obj]["/Height"])
                            data = xObject[obj].get_data()
                            mode = "RGB" if xObject[obj]["/ColorSpace"] == "/DeviceRGB" else "P"

                            image = Image.frombytes(mode, size, data)
                            output_file = os.path.join(self.output_folder, f"image_{image_count + 1}.png")
                            image.save(output_file)
                            image_count += 1

            self.progress.emit(100)
            self.finished.emit(f"Extracción completada: {image_count} imágenes extraídas.")

        except Exception as e:
            self.finished.emit(f"Error durante la extracción: {str(e)}")

class PDFImageExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Image Extractor')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Selecciona un archivo PDF para extraer imágenes')
        layout.addWidget(self.label)

        self.extractBtn = QPushButton('Extraer Imágenes')
        self.extractBtn.clicked.connect(self.extractImages)
        layout.addWidget(self.extractBtn)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

    def extractImages(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecciona un archivo PDF', '', 'PDF Files (*.pdf)')
        if file_path:
            output_folder = QFileDialog.getExistingDirectory(self, 'Selecciona una carpeta de destino')
            if output_folder:
                self.worker = PDFImageExtractorWorker(file_path, output_folder)
                self.worker.progress.connect(self.updateProgress)
                self.worker.finished.connect(self.onExtractionFinished)
                self.worker.start()
                self.label.setText("Extrayendo imágenes...")

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def onExtractionFinished(self, result):
        self.label.setText(result)
        self.progressBar.setValue(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFImageExtractor()
    window.show()
    sys.exit(app.exec_())
