from multiprocessing import Process, Lock
import time

def proceso_a(L1, L2, L3, L4):
    print("Proceso A: esperando L1")
    with L1:
        print("Proceso A: obtuvo L1")
        time.sleep(0.5)

        print("Proceso A: esperando L2")
        with L2:
            print("Proceso A: obtuvo L2")
            time.sleep(0.5)

            print("Proceso A: esperando L3")
            with L3:
                print("Proceso A: obtuvo L3")
                time.sleep(0.5)

                print("Proceso A: esperando L4")
                with L4:
                    print("Proceso A: obtuvo L4")
                    time.sleep(0.5)

    print("Proceso A: terminó")

def proceso_b(L1, L2, L3, L4):
    print("Proceso B: esperando L4")
    with L4:
        print("Proceso B: obtuvo L4")
        time.sleep(0.5)

        print("Proceso B: esperando L3")
        with L3:
            print("Proceso B: obtuvo L3")
            time.sleep(0.5)

            print("Proceso B: esperando L2")
            with L2:
                print("Proceso B: obtuvo L2")
                time.sleep(0.5)

                print("Proceso B: esperando L1")
                with L1:
                    print("Proceso B: obtuvo L1")
                    time.sleep(0.5)

    print("Proceso B: terminó")

if __name__ == "__main__":
    # Crear 4 locks
    L1 = Lock()
    L2 = Lock()
    L3 = Lock()
    L4 = Lock()

    # Crear procesos con orden inverso de adquisición
    A = Process(target=proceso_a, args=(L1, L2, L3, L4))
    B = Process(target=proceso_b, args=(L1, L2, L3, L4))

    A.start()
    B.start()

    A.join()
    B.join()

    print("Ambos procesos finalizados (o bloqueados si hay deadlock)")
