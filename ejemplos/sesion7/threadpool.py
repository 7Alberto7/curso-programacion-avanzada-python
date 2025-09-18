from concurrent.futures import ThreadPoolExecutor
import math


# --- Función para calcular el factorial de un número ---
def calcular_factorial(n):
    print(f"[🧮] Calculando factorial({n})")
    return (n, math.factorial(n))


# --- Lista de números para calcular ---
numeros = [5, 10, 15, 20, 25]


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
            resultados = executor.map(calcular_factorial, numeros)

    

    for n, resultado in resultados:
        print(f" factorial {{n}} = {resultado}")
