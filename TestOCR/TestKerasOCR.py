import keras_ocr
import matplotlib.pyplot as plt

pipeline = keras_ocr.pipeline.Pipeline()

# Puedes procesar varias imágenes a la vez
images = [
    keras_ocr.tools.read('imagen1.jpg'),
    keras_ocr.tools.read('imagen2.jpg'),
]

prediction_groups = pipeline.recognize(images)

# Dibuja las cajas de texto sobre las imágenes
fig, axes = plt.subplots(1, len(images), figsize=(12, 4))

for ax, image, predictions in zip(axes, images, prediction_groups):
    keras_ocr.tools.draw_predictions(predictions, image, ax)

plt.tight_layout()
plt.savefig('resultado_ocr.png')
plt.show()