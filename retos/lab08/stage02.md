## ✅ Resoluciones · Fase 2 — Contador con Lock

---

### 🔸 Reto 1 — ¿Funciona el Lock? Verifica el resultado exacto

#### 🧠 Proceso mental

Queremos comprobar que, si usamos `multiprocessing.Lock`, **la condición de carrera desaparece** y el contador llega siempre al valor esperado. Es lo mínimo que deberíamos garantizar.

#### 🧩 Pasos:

1. Asegúrate de que en `main.py` estás usando:

```python
contador = Value('i', 0)
lock = Lock()
```

2. Al crear cada proceso, pásale el `lock`:

```python
procesos = [
    Process(target=incrementar, args=(contador, 100_000, lock))
    for _ in range(4)
]
```

3. En `app/procesos.py`, protege el incremento:

```python
for _ in range(n_iter):
    with lock:
        contador.value += 1
```

4. Ejecuta `fase2_contador_con_lock()` y compara con `esperado = 400000`.

#### 🧪 Validación:

```bash
Fase 2 (con lock) → contador: 400000  (esperado: 400000)
```

✅ **Siempre coincide**, incluso al repetir múltiples veces.

#### 💡 Aprendo que:

* El `Lock` impide que dos procesos accedan a la misma sección crítica al mismo tiempo.
* Concurrencia sin sincronización = resultados no confiables.

---

### 🔸 Reto 2 — ¿Cuánto cuesta el Lock? Mide el tiempo

#### 🧠 Proceso mental

Ahora que sabemos que `Lock` resuelve el problema, queremos saber **qué impacto tiene en el rendimiento** respecto a la versión sin lock (Fase 1).

#### 🧩 Pasos:

1. Importa al inicio:

```python
from time import perf_counter
```

2. Rodea tu llamada a la Fase 2 con medición:

```python
inicio = perf_counter()
fase2_contador_con_lock()
fin = perf_counter()
print(f"⏱️ Duración con lock: {fin - inicio:.4f} segundos")
```

3. Compara con el tiempo registrado en la Fase 1.

#### 🧪 Ejemplo:

```
Fase 2 (con lock) → contador: 400000  (esperado: 400000)
⏱️ Duración con lock: 0.8012 segundos
```

(Si Fase 1 tardaba \~0.2 s → **4× más lento**, pero correcto.)

#### 💡 Aprendo que:

* El uso de locks es **seguro pero más lento**.
* Hay que evaluar **seguridad vs rendimiento** según el caso.

---

### 🔸 Reto 3 — ¿Qué pasa si optimizas la sección crítica?

#### 🧠 Proceso mental

Bloquear cada incremento con `with lock:` es seguro, pero caro. Podemos **acumular en local** y actualizar el contador global cada cierto tiempo → menos bloqueos, mismo resultado.

#### 🧩 Pasos:

1. En `app/procesos.py`, reemplaza esta parte:

```python
for _ in range(n_iter):
    with lock:
        contador.value += 1
```

2. Por esta versión optimizada:

```python
local_sum = 0
for i in range(n_iter):
    local_sum += 1
    if i % 1000 == 0:
        with lock:
            contador.value += local_sum
            local_sum = 0

if local_sum:
    with lock:
        contador.value += local_sum
```

3. Ejecuta como siempre. El valor debe seguir siendo correcto.

#### 🧪 Validación:

```
Fase 2 (con lock optimizado) → contador: 400000  (esperado: 400000)
⏱️ Duración con lock: 0.4253 segundos
```

(¡Más rápido que el lock tradicional!)

#### 💡 Aprendo que:

* **No todo debe estar protegido** con lock: solo lo crítico.
* Optimizar la sección crítica mejora mucho el rendimiento sin sacrificar seguridad.