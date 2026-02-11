from paddleocr import PaddleOCR


class OCRProcessor:
    """
    RESPONSABILIDAD: Convertir imágenes en texto

    ¿Qué hace?
    - Recibe una imagen (PNG, JPG, PDF)
    - Usa PaddleOCR para extraer texto
    - Devuelve el texto completo y la confianza promedio
    """

    def __init__(self, lang='en'):
        """
        Inicializa el motor OCR

        Args:
            lang: Idioma ('en' para inglés, 'es' para español)
        """
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def extraer_texto(self, ruta_imagen):
        """
        Extrae texto de una imagen

        Args:
            ruta_imagen: Ruta al archivo de imagen

        Returns:
            dict con:
                - texto_completo: Todo el texto extraído
                - confianza: Score promedio de confianza (0-1)
                - num_lineas: Cantidad de líneas detectadas
        """
        print(f"🔍 Procesando imagen: {ruta_imagen}")

        # Ejecutar OCR
        resultado = self.ocr.ocr(ruta_imagen)

        # Extraer texto y confianzas
        texto_lineas = []
        confianzas = []

        for pagina in resultado:
            if pagina is None:
                continue

            for linea in pagina:
                texto = linea[1][0]  # El texto
                confianza = linea[1][1]  # Score de confianza

                texto_lineas.append(texto)
                confianzas.append(confianza)

        # Calcular confianza promedio
        confianza_promedio = sum(confianzas) / len(confianzas) if confianzas else 0

        # Unir todo el texto
        texto_completo = "\n".join(texto_lineas)

        print(f"✅ Extraídas {len(texto_lineas)} líneas")
        print(f"📊 Confianza: {confianza_promedio:.2%}")

        return {
            "texto_completo": texto_completo,
            "confianza": confianza_promedio,
            "num_lineas": len(texto_lineas)
        }