import easyocr
import torch


print("PyTorch:", torch.__version__)
print("CUDA disponible:", torch.cuda.is_available())
print("CUDA versión (PyTorch):", torch.version.cuda)


# Crear el lector (es la primera vez que descarga los modelos del idioma)
reader = easyocr.Reader(['es', 'en'], gpu=False)

# Leer texto de una imagen
result = reader.readtext('test.png')

# Mostrar resultados
for (bbox, texto, confianza) in result:
    print(f"Texto: {texto}")
    print(f"Confianza: {confianza:.2f}")
    print(f"Posición: {bbox}")
    print("---")

