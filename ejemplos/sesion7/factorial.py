import math
from multiprocessing import Pool
import sys


sys.set_int_max_str_digits(0)

def calcular_factorial(n):
    """Calcula el factorial de un número."""
    return (n, math.factorial(n))

if __name__ == "__main__":
    # Lista de números "grandes" (sin exagerar para no saturar CPU/RAM)
    numeros = [100_000, 50_000, 20_000, 10_000]

    with Pool(processes=4) as pool:
        resultados = pool.map(calcular_factorial, numeros)

    # Mostrar resultados parciales (solo la longitud del factorial para no saturar salida)
    for n, fact in resultados:
        print(f"{n}! tiene {len(str(fact))} dígitos")
