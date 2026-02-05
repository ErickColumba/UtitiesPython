# DocumentProcessor.py
import fitz  # PyMuPDF
from docx import Document
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import platform


class DocumentProcessor:
    """Procesa múltiples formatos de documentos"""

    def __init__(self):
        # Configuración de rutas para Windows
        if platform.system() == 'Windows':
            # Configura Tesseract
            tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path

            # Configura Poppler
            self.poppler_path = r'C:\poppler\Library\bin'
        else:
            self.poppler_path = None

    def extract_text(self, file_path):
        """Extrae texto según el tipo de archivo"""
        extension = os.path.splitext(file_path)[1].lower()

        if extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return self._extract_from_word(file_path)
        elif extension == '.txt':
            return self._extract_from_txt(file_path)
        elif extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self._extract_from_image(file_path)
        else:
            raise ValueError(f"Formato no soportado: {extension}")

    def _extract_from_pdf(self, file_path):
        """Extrae texto de PDF (nativo o con OCR)"""
        text = ""

        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    page_text = page.get_text()
                    text += page_text
        except Exception as e:
            print(f"Error extrayendo con PyMuPDF: {e}")

        # Si no hay texto o es muy poco, usa OCR
        if len(text.strip()) < 50:
            print("Usando OCR para extraer texto del PDF...")
            try:
                # Usa poppler_path en Windows
                if self.poppler_path and os.path.exists(self.poppler_path):
                    images = convert_from_path(file_path, poppler_path=self.poppler_path)
                else:
                    images = convert_from_path(file_path)

                text = ""
                for i, image in enumerate(images):
                    print(f"Procesando página {i + 1}/{len(images)}...")
                    text += pytesseract.image_to_string(image, lang='spa')
                    text += "\n\n"
            except Exception as e:
                print(f"Error en OCR: {e}")
                raise

        return text

    def _extract_from_word(self, file_path):
        """Extrae texto de Word"""
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_from_txt(self, file_path):
        """Extrae texto de TXT"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _extract_from_image(self, file_path):
        """Extrae texto de imagen con OCR"""
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang='spa')