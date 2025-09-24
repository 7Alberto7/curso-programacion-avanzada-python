## ✅ Resoluciones · Fase 1 — Contador sin Lock

---

### 🔸 Reto 1 — Observa cómo falla un contador sin protección

#### 🧠 Proceso mental

Queremos probar que, sin protección, varios procesos escribiendo en el mismo `Value` provocan errores silenciosos. Esto es una condición de carrera. El valor final **no será fiable**.

#### 🧩 Pasos:

1. Asegúrate de tener la función `incrementar()` en `app/procesos.py` tal como está:

```python
def incrementar(contador: Value, n_iter: int = 100_000, lock=None) -> None:
    for _ in range(n_iter):
        contador.value += 1  # sin lock
```

2. En `main.py`, crea un `Value` entero compartido:

```python
contador = Value('i', 0)
```

3. Lanza 4 procesos que llamen a `incrementar_sin_lock(contador)`:

```python
procesos = [Process(target=incrementar_sin_lock, args=(contador,)) for _ in range(4)]
```

4. Llama a `.start()` y `.join()` como siempre:

```python
for p in procesos: p.start()
for p in procesos: p.join()
```

5. Imprime el valor final del contador:

```python
print(f"Fase 1 (sin lock) → contador: {contador.value} (esperado: 400000)")
```

#### 🧪 Validación:

* La salida mostrará un número **menor a 400000**, por ejemplo:

```
Fase 1 (sin lock) → contador: 274183 (esperado: 400000)
```

#### 💡 Aprendo que:

* Las condiciones de carrera **no se notan con errores**, pero destruyen los resultados.
* Python no protege los accesos a `Value` automáticamente → el programador debe hacerlo.

---

### 🔸 Reto 2 — Provoca más fallos aumentando la presión

#### 🧠 Proceso mental

Si aumentamos el número de iteraciones o procesos, **amplificamos el problema**. Con más competencia por el mismo recurso, hay más errores.

#### 🧩 Opciones:

**Opción A:** Aumenta `n_iter` en `incrementar()`:

```python
incrementar(contador, n_iter=1_000_000)
```

**Opción B:** Aumenta el número de procesos a 8:

```python
procesos = [Process(target=incrementar_sin_lock, args=(contador,)) for _ in range(8)]
```

**Opcional:** Cambia el tipo de dato a `long`:

```python
contador = Value('l', 0)  # también da error sin lock
```

#### 🧪 Validación:

* El valor final será **aún más incorrecto** (por ejemplo, 512393 en lugar de 800000).
* A veces cambia en cada ejecución → no hay estabilidad.

#### 💡 Aprendo que:

* El problema **se intensifica** con mayor paralelismo.
* Usar `long` en lugar de `int` **no soluciona nada**: el error está en la concurrencia.

---

### 🔸 Reto 3 — Mide el tiempo total sin Lock (baseline de rendimiento)

#### 🧠 Proceso mental

Queremos establecer un **tiempo base** de ejecución **sin lock**, para comparar después con la versión sincronizada en la Fase 2.

#### 🧩 Pasos:

1. Importa `perf_counter` al principio del archivo:

```python
from time import perf_counter
```

2. Rodea tu llamada a `fase1_contador_sin_lock()` con:

```python
inicio = perf_counter()
fase1_contador_sin_lock()
fin = perf_counter()
print(f"⏱️ Duración sin lock: {fin - inicio:.4f} segundos")
```

3. Ejecuta varias veces para tener un promedio orientativo.

#### 🧪 Validación:

```bash
Fase 1 (sin lock) → contador: 297001 (esperado: 400000)
⏱️ Duración sin lock: 0.2135 segundos
```

#### 💡 Aprendo que:

* La versión sin lock es **rápida pero incorrecta**.
* La comparación de rendimiento solo tiene sentido si la salida es válida.