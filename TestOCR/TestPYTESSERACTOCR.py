import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='es')

# El método correcto en esta versión es ocr()
resultado = ocr.ocr("test.png")

# Mostrar resultados
for línea in resultado:
    for elemento in línea:
        texto = elemento[1][0]
        confianza = elemento[1][1]
        print(f"Texto: {texto} | Confianza: {confianza:.2f}")