## ✅ Resoluciones · Fase 3 — Escritura en archivo con y sin Lock

---

### 🔸 Reto 1 — ¿Qué pasa cuando escribes sin Lock?

#### 🧠 Proceso mental

Varios procesos escriben a la vez en el mismo archivo. Sin sincronización, el sistema operativo puede mezclar sus llamadas a `write()`. Aunque parezca que no falla, **las líneas pueden aparecer rotas, duplicadas o incompletas**.

#### 🧩 Pasos:

1. Llama a `demo_log_sin_lock()` desde `main.py` (o directamente desde `__main__`).
2. Asegúrate de que `N_PROCESOS` y `N_LINEAS_POR_PROCESO` están altos (p. ej. 8 procesos × 500 líneas).
3. Abre el archivo `log_sin_lock.txt` después de la ejecución.
4. Busca líneas como:

   * Truncadas: `P03 L015` sin salto de línea.
   * Mezcladas: `P02 L014P04 L023`.
   * Mal formateadas: caracteres superpuestos o sin formato.

#### 🧪 Validación esperada:

```bash
Fase 3A (sin lock) → revisa log_sin_lock.txt
```

Y en el archivo algo como:

```txt
[PID?] P00 L0000
[PID?] P01 L0000
[PID?] P00 L0001[PID?] P02 L0001
[PID?] P01 L0001
```

(¡errores visibles!)

#### 💡 Aprendo que:

* Un archivo no garantiza consistencia entre procesos concurrentes.
* La E/S no es atómica → cada proceso debe proteger su bloque.

---

### 🔸 Reto 2 — ¿Y si usamos Lock?

#### 🧠 Proceso mental

Queremos proteger la escritura envolviéndola con `with lock:`. Así, **solo un proceso a la vez accede al archivo**, garantizando que cada línea se escriba completa.

#### 🧩 Pasos:

1. Llama a `demo_log_con_lock()` desde `main.py`.
2. Verifica que los procesos usan `escribir_log_seguro()`, que contiene:

```python
with lock:
    with open(path, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")
```

3. Comprueba que el archivo `log_con_lock.txt`:

   * Tiene exactamente `N_PROCESOS × N_LINEAS_POR_PROCESO` líneas.
   * Todas las líneas están completas y bien formateadas.

#### 🧪 Validación esperada:

```bash
Fase 3B (con lock) → revisa log_con_lock.txt
```

Y en el archivo:

```txt
[SEG] P00 L0000
[SEG] P00 L0001
[SEG] P00 L0002
...
```

✅ ¡Sin errores ni entremezclas!

#### 💡 Aprendo que:

* El `Lock` protege incluso operaciones con archivos.
* Es importante **envolver todo el bloque de apertura y escritura**, no solo `f.write()`.

---

### 🔸 Reto 3 — ¿Y si en lugar de Lock usamos un escritor central?

#### 🧠 Proceso mental

Usamos `Queue` como un buzón. Varios procesos productores envían mensajes, y un proceso único (escritor) los consume y escribe al archivo. **No se necesita Lock** porque solo 1 proceso accede al recurso.

#### 🧩 Pasos:

1. Importa:

```python
from multiprocessing import Process, Queue
```

2. Crea una cola y el proceso escritor:

```python
q = Queue()
path = Path("log_queue.txt")
if path.exists(): path.unlink()

def escritor(q, path, total_fin):
    recibidos = 0
    with path.open("a", encoding="utf-8") as f:
        while recibidos < total_fin:
            msg = q.get()
            if msg is None:
                recibidos += 1
            else:
                f.write(msg + "\n")
```

3. Crea los procesos productores:

```python
def productor(idx, q):
    for j in range(200):
        q.put(f"[Q] P{idx:02d} L{j:04d}")
    q.put(None)  # señal de fin

procesos = [Process(target=productor, args=(i, q)) for i in range(N_PROCESOS)]
```

4. Lanza todo:

```python
escritor_proc = Process(target=escritor, args=(q, path, N_PROCESOS))
escritor_proc.start()
for p in procesos: p.start()
for p in procesos: p.join()
escritor_proc.join()
```

#### 🧪 Validación esperada:

* El archivo `log_queue.txt` tiene todas las líneas completas.
* Mismo número de líneas que en el caso con Lock.

#### 💡 Aprendo que:

* `Queue` permite separar responsabilidades: muchos productores, un consumidor.
* Este patrón es más escalable y desacoplado que Lock si hay mucha escritura.