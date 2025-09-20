# 🔹 Fase 2: Contador compartido **con `multiprocessing.Lock`**

### 🎯 Objetivo

Eliminar la condición de carrera usando un **`Lock`** para proteger la sección crítica al incrementar el entero compartido. El valor final debe ser **exactamente** el esperado.

---

## 🧱 Qué cambia respecto a Fase 1

* Creamos un **`Lock()`** y lo pasamos a cada proceso.
* En la función de trabajo, envolvemos el incremento con `with lock:`.

---

## 🧭 Código

**app/procesos.py** (amplía la función para usar `lock` si se provee)

```python
# app/procesos.py
from multiprocessing import Value, Lock

def incrementar(contador: Value, n_iter: int = 100_000, lock: Lock | None = None) -> None:
    """
    Incrementa un entero compartido n_iter veces.
    Si se proporciona lock, protege la sección crítica.
    """
    if lock is None:
        # SIN protección (Fase 1)
        for _ in range(n_iter):
            contador.value += 1
    else:
        # CON protección (Fase 2)
        for _ in range(n_iter):
            with lock:
                contador.value += 1
```

**main.py** (añade una función nueva para Fase 2)

```python
# main.py
from multiprocessing import Process, Value, Lock
from app.procesos import incrementar

N_PROCESOS = 4
N_ITER = 100_000

def fase2_contador_con_lock():
    contador = Value('i', 0)
    lock = Lock()

    procesos = [
        Process(target=incrementar, args=(contador, N_ITER, lock))
        for _ in range(N_PROCESOS)
    ]

    for p in procesos: p.start()
    for p in procesos: p.join()

    esperado = N_PROCESOS * N_ITER
    print(f"Fase 2 (con lock) → contador: {contador.value}  (esperado: {esperado})")

if __name__ == "__main__":
    # Puedes ejecutar solo Fase 2, o llamar también a la Fase 1 si la mantienes.
    fase2_contador_con_lock()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada:**

```
Fase 2 (con lock) → contador: 400000  (esperado: 400000)
```

---

## ✅ Criterios de aceptación

* Se crean **N\_PROCESOS** procesos que incrementan el mismo `Value('i', 0)` con **`Lock`** compartido.
* El resultado final **coincide** con `N_PROCESOS * N_ITER` en **todas** las ejecuciones.
* El incremento está protegido con `with lock:` (exclusión mutua real).



## 🔁 Retos · Fase 2

> 🎯 Objetivo global: Garantizar la **consistencia de los datos compartidos** usando `multiprocessing.Lock`
> 💡 En esta fase **evitamos por completo** la condición de carrera.

---

### 🔸 Reto 1 — ¿Funciona el Lock? Verifica el resultado exacto

**🎯 Objetivo:** Usar `Lock` correctamente para obtener **exactamente** el valor esperado en todas las ejecuciones.

🔧 **Qué hacer:**

* En `main.py`, crea un `Lock()` y pásalo a todos los procesos.
* Asegúrate de proteger la suma con `with lock:` en la función `incrementar`.

```python
with lock:
    contador.value += 1
```

🧠 **Qué aprendo:**

* Que `Lock` fuerza la **exclusión mutua**: solo un proceso accede al recurso compartido a la vez.
* Que el resultado deja de ser aleatorio y se vuelve **confiable**.

---

### 🔸 Reto 2 — ¿Cuánto cuesta el Lock? Mide el tiempo

**🎯 Objetivo:** Comparar el rendimiento de la ejecución **con y sin lock**.

🔧 **Qué hacer:**

* Usa `time.perf_counter()` alrededor de `fase2_contador_con_lock()` para medir duración.
* Compara con el tiempo medido en la Fase 1 (sin lock).

```python
inicio = perf_counter()
fase2_contador_con_lock()
fin = perf_counter()
print(f"⏱️ Duración con lock: {fin - inicio:.4f} segundos")
```

🧠 **Qué aprendo:**

* Que usar `Lock` introduce una penalización en rendimiento…
* …pero lo **compensa al asegurar la precisión del resultado**.

---

### 🔸 Reto 3 — ¿Qué pasa si optimizas la sección crítica?

**🎯 Objetivo:** Reducir el impacto del `Lock` acotando mejor la sección crítica.

🔧 **Qué hacer:**

* Cambia la función `incrementar` para que:

  * Acumule en una variable local (`local_sum`)
  * Solo actualice `contador.value` **una vez cada 1000 iteraciones** (dentro del `lock`)

```python
local_sum = 0
for i in range(n_iter):
    local_sum += 1
    if i % 1000 == 0:
        with lock:
            contador.value += local_sum
            local_sum = 0
# Al final del bucle, escribe lo que quede:
if local_sum:
    with lock:
        contador.value += local_sum
```

🧠 **Qué aprendo:**

* Que reducir la sección crítica mejora el rendimiento.
* Que podemos mantener la exactitud **optimizando** cómo usamos el `Lock`.