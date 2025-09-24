from multiprocessing import Process, Queue



def suma_rango(inicio, fin, cola):
    """Suma los números entre inicio y fin (ambos inclusive) y lo mete en la cola."""
    resultado = sum(range(inicio, fin + 1))
    cola.put(resultado)


if __name__ = "__main__":
    cola = Queue()

     # Definir los rangos
    rangos = [
        (1, 100),     # Primer proceso suma del 1 al 100
        (101, 200),   # Segundo proceso suma del 101 al 200
        (201, 300)    # Tercer proceso suma del 201 al 300
    ]   

    procesos = []

    for ini, fin in rangos:
        p = Process(target=suma_rango, args=(ini,fin,cola))
        procesos.append(p)
        p.start()
        
    for p in procesos:
        p.join()

    # Recoger resultados de la cola
    suma_total = 0
    while not cola.empty():
        suma_total += cola.get()

    print(f"Suma total de los tres rangos: {suma_total}")    