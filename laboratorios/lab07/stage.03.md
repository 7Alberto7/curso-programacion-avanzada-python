

# 🔹 Fase 3: Simulación de *deadlock* y prevención

### 🎯 Objetivo

Provocar un **deadlock** entre hilos utilizando dos `Lock` adquiridos en orden inverso, y luego **prevenirlo** mediante dos estrategias:

1. Adquisición con **orden global predefinido**.
2. Uso de `acquire(timeout=…)` y manejo del fallo para **evitar el bloqueo mutuo**.

---

## 🧱 Qué vas a añadir

Implementarás nuevas funciones en `app/procesador.py` para:

* Simular un deadlock real entre hilos.
* Resolverlo con orden global (adquisición A → B).
* Resolverlo usando `timeout` y liberación segura.

Además, crearás un script de pruebas para visualizar los distintos escenarios.

---

## 🧭 Código

### 1) `app/procesador.py` — utilidades de deadlock

Añade al final del archivo `app/procesador.py` las siguientes funciones:

```python
from time import sleep
import threading

def _trabajo_breve():
    sleep(0.1)

def simular_deadlock(lock1: threading.Lock, lock2: threading.Lock):
    def t1():
        with lock1:
            print("[t1] tomó lock1, esperando lock2…")
            sleep(0.2)
            with lock2:
                print("[t1] tomó lock2")
                _trabajo_breve()

    def t2():
        with lock2:
            print("[t2] tomó lock2, esperando lock1…")
            sleep(0.2)
            with lock1:
                print("[t2] tomó lock1")
                _trabajo_breve()

    h1 = threading.Thread(target=t1, name="t1")
    h2 = threading.Thread(target=t2, name="t2")
    h1.start(); h2.start()
    h1.join(timeout=2.0)
    h2.join(timeout=2.0)

    if h1.is_alive() and h2.is_alive():
        print("⚠️  DEADLOCK confirmado: ambos hilos están bloqueados")
    else:
        print("✔ No hubo deadlock (esta vez)")

def trabajo_ordenado(lock_a: threading.Lock, lock_b: threading.Lock):
    with lock_a:
        print(f"[{threading.current_thread().name}] tomó A")
        sleep(0.1)
        with lock_b:
            print(f"[{threading.current_thread().name}] tomó B")
            _trabajo_breve()

def resolver_con_orden_global():
    A = threading.Lock()
    B = threading.Lock()
    h1 = threading.Thread(target=trabajo_ordenado, args=(A, B), name="r1")
    h2 = threading.Thread(target=trabajo_ordenado, args=(A, B), name="r2")
    h1.start(); h2.start()
    h1.join(); h2.join()
    print("✔ Finalizado sin deadlock (orden global)")

def resolver_con_timeout(lock1: threading.Lock, lock2: threading.Lock, who: str):
    acquired1 = lock1.acquire(timeout=1.0)
    if not acquired1:
        print(f"[{who}] no pudo tomar lock1, reintentará…")
        return

    print(f"[{who}] tomó lock1, intentando lock2 con timeout…")
    try:
        acquired2 = lock2.acquire(timeout=0.5)
        if not acquired2:
            print(f"[{who}] 💡 Deadlock evitado: liberando lock1 y abortando")
            return
        try:
            print(f"[{who}] tomó lock2, trabajando…")
            _trabajo_breve()
        finally:
            lock2.release()
    finally:
        lock1.release()
```

---

### 2) `deadlock_demo.py` — pruebas de demostración

Crea un archivo separado para probar los casos:

```python
# deadlock_demo.py
import threading
from app.procesador import (
    simular_deadlock,
    resolver_con_orden_global,
    resolver_con_timeout,
)

def demo_deadlock():
    print("\n=== DEMO: Posible deadlock ===")
    L1 = threading.Lock()
    L2 = threading.Lock()
    simular_deadlock(L1, L2)

def demo_orden_global():
    print("\n=== DEMO: Prevención por orden global A→B ===")
    resolver_con_orden_global()

def demo_timeout():
    print("\n=== DEMO: Prevención con timeouts ===")
    L1 = threading.Lock()
    L2 = threading.Lock()
    t1 = threading.Thread(target=resolver_con_timeout, args=(L1, L2, "X"))
    t2 = threading.Thread(target=resolver_con_timeout, args=(L2, L1, "Y"))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print("✔ Finalizado sin deadlock (timeouts)")

if __name__ == "__main__":
    demo_deadlock()
    demo_orden_global()
    demo_timeout()
```

---

## ▶️ Ejecución

```bash
python deadlock_demo.py
```

---

## ✅ Criterios de validación

* Se observa un posible **deadlock** cuando ambos hilos se quedan esperando: `join(timeout)` lo detecta.
* La estrategia con **orden global A→B** ejecuta sin bloqueos.
* La estrategia con **timeout** evita el bloqueo: uno de los hilos desiste, mostrando el mensaje correspondiente.

---

## 🔁 Retos opcionales

### 🔸 Reto 1 — Mensaje claro al evitar el deadlock

Añade esta línea al abortar por timeout:

```python
print(f"[{who}] 💡 Deadlock evitado: liberando lock1 y abortando")
```

### 🔸 Reto 2 — Mostrar nombres de locks

Permite pasar nombres a los locks y visualiza:

```python
print(f"[{who}] intentando {nombre_lock2} tras tomar {nombre_lock1}")
```

### 🔸 Reto 3 — Confirmar deadlock solo si ambos hilos siguen vivos

```python
if h1.is_alive() and h2.is_alive():
    print("⚠️  DEADLOCK confirmado: ambos hilos están bloqueados")
```

---

## ✅ Conclusión

En esta fase has aprendido a:

* Reproducir un **deadlock realista** entre hilos.
* Detectarlo mediante `join(timeout)`.
* Prevenirlo con dos enfoques clave:

  * **Orden global fijo** en la adquisición.
  * **Timeout + manejo de error** para desistir de forma segura.

Estos patrones son esenciales para diseñar sistemas concurrentes **seguros y robustos**.


