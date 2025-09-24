# 🔹 Fase 1: Contador compartido **sin Lock** (reproduce la condición de carrera)

### 🎯 Objetivo

Demostrar una **condición de carrera** usando varios procesos que incrementan un **entero compartido** sin sincronización. El valor final **será menor** que el esperado.

---

## 🧱 Scaffold

```
lab8_multiprocessing/
├─ app/
│  ├─ __init__.py
│  └─ procesos.py
└─ main.py
```

---

## 🧭 Código

**app/procesos.py**

```python
# app/procesos.py
from multiprocessing import Value

def incrementar(contador: Value, n_iter: int = 100_000, lock=None) -> None:
    """
    Incrementa un entero compartido n_iter veces.
    En Fase 1 ignoramos 'lock' para forzar condición de carrera.
    """
    for _ in range(n_iter):
        # ¡SIN protección! (esto provoca race condition)
        contador.value += 1
```

**main.py**

```python
# main.py
from multiprocessing import Process, Value

def fase1_contador_sin_lock():
    # entero compartido con tipo 'i' (int)
    contador = Value('i', 0)
    procesos = [Process(target=incrementar_sin_lock, args=(contador,)) for _ in range(4)]

    for p in procesos: p.start()
    for p in procesos: p.join()

    esperado = 4 * 100_000
    print(f"Fase 1 (sin lock) → contador: {contador.value}  (esperado: {esperado})")

def incrementar_sin_lock(contador):
    # función wrapper para importar menos en el ejemplo
    from app.procesos import incrementar
    incrementar(contador, 100_000, lock=None)

if __name__ == "__main__":
    fase1_contador_sin_lock()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida típica (varía por carrera):**

```
Fase 1 (sin lock) → contador: 271893  (esperado: 400000)
```

> Lo normal es que el valor sea **menor que 400000**, evidenciando la **condición de carrera**.

---

## ✅ Criterios de aceptación

* Se crean **4 procesos** que incrementan el **mismo `Value('i', 0)`**.
* El resultado final es **inferior** al esperado (`400000`) en la mayoría de ejecuciones.
* No se usa ningún `Lock` ni mecanismo de sincronización.


---

## 🔁 Retos 

---

🔸 **Reto 1 — Observa cómo falla un contador sin protección**
**🎯 Objetivo:** Ver que el resultado final es incorrecto al no usar `Lock`.

🔧 **Qué hacer:**

* Ejecuta la función `fase1_contador_sin_lock()` que lanza 4 procesos, cada uno sumando 100.000 al mismo `multiprocessing.Value`.
* Comprueba que el resultado final **casi nunca** es 400.000.

```python
print(f"Fase 1 (sin lock) → contador: {contador.value} (esperado: 400000)")
```

🧠 **Qué aprendo:**

* Qué es una condición de carrera: varios procesos acceden y modifican la misma variable sin coordinación.
* Que este tipo de errores **no lanzan excepciones**, pero invalidan los resultados.

---

🔸 **Reto 2 — Provoca más fallos aumentando la presión**
**🎯 Objetivo:** Aumentar la probabilidad de que ocurra el error modificando la carga o el número de procesos.

🔧 **Qué hacer:**

* Cambia `n_iter` a 1\_000\_000 en la función `incrementar`.
* O aumenta a 8 procesos en lugar de 4.

```python
procesos = [Process(target=incrementar_sin_lock, args=(contador,)) for _ in range(8)]
```

🧠 **Qué aprendo:**

* Que las condiciones de carrera son más frecuentes cuando hay **más procesos o iteraciones**.
* Que el problema no se resuelve “por suerte”: siempre está presente, aunque no siempre visible.

---

🔸 **Reto 3 — Mide el tiempo total sin Lock (baseline de rendimiento)**
**🎯 Objetivo:** Registrar cuánto tarda la versión sin `Lock` para compararlo luego con la versión sincronizada.

🔧 **Qué hacer:**

* Usa `time.perf_counter()` para medir cuánto dura `fase1_contador_sin_lock()`:

```python
from time import perf_counter
inicio = perf_counter()
fase1_contador_sin_lock()
fin = perf_counter()
print(f"⏱️ Duración sin lock: {fin - inicio:.4f} segundos")
```

🧠 **Qué aprendo:**

* Que la falta de sincronización puede ser rápida… pero **insegura**.
* Que la sincronización con `Lock` **aumenta la seguridad a costa de algo de rendimiento** (lo veremos en la Fase 2).
