# app/procesos.py
from multiprocessing import Value, Lock
from pathlib import Path
import os
import time

def incrementar(contador: Value, n_iter: int = 100_000, lock: Lock | None = None) -> None:
    if lock is None:
        for _ in range(n_iter):
            contador.value += 1
    else:
        for _ in range(n_iter):
            with lock:
                contador.value += 1

# --- NUEVO: escritura concurrente ---
def escribir_log(path: str | Path, mensaje: str) -> None:
    """
    Escribe una línea en un archivo compartido SIN sincronización.
    Bajo contención, pueden aparecer líneas mezcladas o truncadas.
    """
    p = Path(path)
    # Simula trabajo para aumentar la probabilidad de intercalado
    time.sleep(0.001)
    with p.open("a", encoding="utf-8") as f:
        f.write(mensaje + "\n")

def escribir_log_seguro(path: str | Path, mensaje: str, lock: Lock) -> None:
    """
    Escribe una línea en un archivo compartido con protección por Lock.
    Garantiza atomicidad a nivel lógico para cada línea.
    """
    p = Path(path)
    time.sleep(0.001)
    with lock:
        with p.open("a", encoding="utf-8") as f:
            f.write(mensaje + "\n")



q = Queue()
path = Path("log_queue.txt")
if path.exists(): path.unlink()

def escribe_log(q, path, total_fin): 
    with path.open("a", encoding="utf-8") as f:
         mensaje = q.get()
         f.write(mensaje + "\n")




def ecribirlog(idx, q):
    for j in range(200):
        q.put(f"[Q] P{idx:02d} L{j:04d}")
    q.put(None)  # señal de fin




escritor_proc = Process(target=escribe_log, args=(q, path, 6))

def productor(idx, q):
    for j in range(200):
        q.put(f"[Q] P{idx:02d} L{j:04d}")
    q.put(None)  # señal de fin

procesos = [Process(target=productor, args=(i, q)) for i in range(34)]