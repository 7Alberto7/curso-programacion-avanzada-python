from organizador import organizar_por_tipo
from pathlib import Path

def fase1():
    entrada = Path(".")
    salida = Path("./output")
    organizar_por_tipo(entrada, salida)