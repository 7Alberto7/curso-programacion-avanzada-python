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