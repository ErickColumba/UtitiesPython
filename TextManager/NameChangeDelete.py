import tkinter as tk
from tkinter import filedialog
import os

# --- PARTE A ELIMINAR DEL NOMBRE ---
parte_a_borrar = ".png_0001"

# Crear ventana oculta
root = tk.Tk()
root.withdraw()

# Seleccionar carpeta
carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos")

if not carpeta:
    print("No se seleccionó ninguna carpeta.")
    exit()

# Procesar archivos
for nombre_archivo in os.listdir(carpeta):
    if parte_a_borrar in nombre_archivo:
        nombre_nuevo = nombre_archivo.replace(parte_a_borrar, "")
        ruta_vieja = os.path.join(carpeta, nombre_archivo)
        ruta_nueva = os.path.join(carpeta, nombre_nuevo)

        os.rename(ruta_vieja, ruta_nueva)
        print(f"✅ Renombrado: {nombre_archivo} → {nombre_nuevo}")

print("\n🎉 Renombrado terminado.")
