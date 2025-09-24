import threading


contador = 0
# lock = threading.Lock()

def incrementar(n_veces):
    global contador
    for _ in range(n_veces):
        # with lock:
        contador += 1



if __name__ == "__main__":
    contador = 0
    hilos = []
    for _ in range(5):
        t = threading.Thread(target=incrementar, args=(10000000,))
        hilos.append(t)
        t.start()

    for _ in hilos:
        t.join()


    print(" sin Lock el valor final es:", contador)