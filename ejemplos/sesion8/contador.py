from multiprocessing import Process, Value

def incrementar(contador):
    for _ in range(100000):
        contador.value += 1  # ⚠️ No es atómico

if __name__ == "__main__":
    contador = Value('i', 0)  # Entero entero compartido

    procesos = [Process(target=incrementar, args=(contador,)) for _ in range(4)]

    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    print("Contador final:", contador.value)  # Esperado: 400000, pero...
