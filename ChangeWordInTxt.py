import tkinter as tk
from tkinter import filedialog
import os

# --- CONFIGURACIÓN ---
palabra_a_buscar = "PiaAzure, is a  "
palabra_nueva = "PiaAzure, "

# Crear ventana oculta
root = tk.Tk()
root.withdraw()

# Abrir explorador para seleccionar múltiples archivos
archivos = filedialog.askopenfilenames(
    title="Selecciona los archivos a modificar",
    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
)

if not archivos:
    print("No se seleccionaron archivos.")
    exit()

# Procesar cada archivo
for archivo in archivos:
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    contenido_nuevo = contenido.replace(palabra_a_buscar, palabra_nueva)

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido_nuevo)

    print(f"Modificado: {os.path.basename(archivo)}")

print("\n✅ Reemplazo terminado en todos los archivos.")
