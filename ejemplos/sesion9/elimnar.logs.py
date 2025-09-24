import os

carpeta = "/var/logs"  # Cambia por la ruta de tu carpeta

# Recorremos todos los archivos de la carpeta
for archivo in os.listdir(carpeta):
    ruta_completa = os.path.join(carpeta, archivo)
    
    # Verificamos si es un archivo .log
    if os.path.isfile(ruta_completa) and archivo.endswith(".log"):
        os.remove(ruta_completa)
        print(f"Archivo eliminado: {ruta_completa}")
