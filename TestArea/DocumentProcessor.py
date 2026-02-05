# document_processor.py
import fitz  # PyMuPDF
from docx import Document
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os


class DocumentProcessor:
    """Procesa múltiples formatos de documentos"""

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

        # Primero intenta extraer texto nativo
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

        # Si no hay texto, usa OCR
        if not text.strip():
            images = convert_from_path(file_path)
            for image in images:
                text += pytesseract.image_to_string(image, lang='spa')

        return text

    def _extract_from_word(self, file_path):
        """Extrae texto de Word"""
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_from_txt(self, file_path):
        """Extrae texto de TXT"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_from_image(self, file_path):
        """Extrae texto de imagen con OCR"""
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang='spa')