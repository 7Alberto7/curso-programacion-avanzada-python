import shutil,os

with open("notas.txt","w") as archivo:
    archivo.write("linea 1\n")
    archivo.write("linea 2\n")
    archivo.write("linea 3\n")

with open("notas.txt","r") as archivo:
    for i, linea in enumerate(archivo):
        print(f"{i}: {linea.strip()}")



os.makedirs("data", exist_ok=True)
shutil.move("notas.txt", "data/ejemplo_copia.txt")




import os

# Directorio actual
print("Directorio actual:", os.getcwd())

# Listar contenido de un directorio
for nombre in os.listdir("."):
    print(" -", nombre)

# Comprobar existencia
print("¿existe main.py?", os.path.exists("/home/david/main.py"))

# Información de rutas
print("Es archivo?", os.path.isfile("main.py"))
print("Es carpeta?", os.path.isdir("app"))


os.rmdir()  # eliminado de carpeta vacia
shutil.rmtree() # eliminado recursivo de carpeta





import shutil
import os

carpeta = "carpeta_a_borrar"

# Verificar si existe antes de borrar
if os.path.isdir(carpeta):   
    shutil.rmtree(carpeta)
    print(f"Carpeta '{carpeta}' eliminada completamente.")
else:
    print(f"La carpeta '{carpeta}' no existe.")


import yaml
with open('yamel.yml', 'r') as f:
    datos = yaml.safe_load(f)

with open('yamel.yml', 'w') as f:
    yaml.dump(objeto, f, default_flow_style=True)


nombre, extension = os.path.splitext(archivo)



from pathlib import Path

archivo = Path("reporte.final.pdf")
print(archivo.suffix)      # .pdf
print(archivo.suffixes)    # ['.final', '.pdf']  (lista si hay varias extensiones)




from pathlib import Path
import shutil

def organizar_por_tipo(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    
    for archivo in src.iterdir():
        if archivo.is_file():
            ext = archivo.suffix.lstrip(".").lower() or "otros"
            carpeta = dst / ext
            carpeta.mkdir(parents=True, exist_ok=True)
            shutil.move(str(archivo), carpeta / archivo.name)
