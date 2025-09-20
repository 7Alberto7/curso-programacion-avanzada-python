## ✅ Resoluciones · Fase 2 — Organizar ficheros por fecha (YYYY-MM)

---

### 🔸 Reto 1 — Organiza los archivos por fecha de modificación

#### 🧩 Qué hacer paso a paso:

1. En `app/organizador.py`, añade la función `organizar_por_fecha(base: Path)`.

2. Dentro de esta función:

   * Recorre todas las subcarpetas de `base` (`carpeta_tipo`).
   * Para cada archivo:

     * Usa `archivo.stat().st_mtime` para obtener la fecha de modificación.

     * Convierte el timestamp a una cadena `YYYY-MM` con:

       ```python
       from datetime import datetime
       fecha = datetime.fromtimestamp(ts).strftime("%Y-%m")
       ```

     * Crea la carpeta destino: `carpeta_tipo / fecha`

     * Mueve el archivo allí con `shutil.move(...)`.

3. Ejemplo completo (ya incluido en el scaffold):

```python
def organizar_por_fecha(base: Path) -> None:
    for carpeta_tipo in base.iterdir():
        if not carpeta_tipo.is_dir():
            continue

        for archivo in list(carpeta_tipo.iterdir()):
            if not archivo.is_file():
                continue

            ts = archivo.stat().st_mtime
            yyyymm = datetime.fromtimestamp(ts).strftime("%Y-%m")
            destino = carpeta_tipo / yyyymm
            destino.mkdir(parents=True, exist_ok=True)
            shutil.move(str(archivo), destino / archivo.name)
```

#### ✅ Resultado esperado:

```text
data/organizado/
├─ txt/
│  └─ 2025-09/
│      └─ informe.txt
├─ jpg/
│  └─ 2024-07/
│      └─ foto.jpg
```

#### 💡 Puntos clave:

* `stat().st_mtime` te da el tiempo en segundos desde epoch.
* Siempre usa `Path` para manipular rutas, es más limpio que concatenar strings.

---

### 🔸 Reto 2 — Ignora archivos ya en carpetas YYYY-MM

#### 🧩 Qué hacer paso a paso:

1. Dentro del bucle que recorre archivos en `carpeta_tipo`, antes de moverlos:

```python
if archivo.parent.name.count("-") == 1 and len(archivo.parent.name) == 7:
    continue
```

2. O bien, si usas `regex`, puedes hacerlo más explícito con `re.match()` para detectar carpetas `YYYY-MM`.

3. Esto evitará que archivos ya ubicados correctamente vuelvan a moverse o aniden `YYYY-MM/YYYY-MM`.

#### ✅ Resultado esperado:

* Si ya está en `txt/2025-09/`, no lo vuelve a mover.
* Si está en `txt/`, sí lo mueve.

#### 💡 Puntos clave:

* Esto hace que tu script sea **seguro de ejecutar más de una vez**.
* Evitas errores como mover archivos múltiples veces o crear rutas como `txt/2025-09/2025-09/archivo`.

---

### 🔸 Reto 3 — Borra carpetas vacías después de mover

#### 🧩 Qué hacer paso a paso:

1. Al final del bucle de `carpeta_tipo`, después de mover todos los archivos:

```python
if not any(carpeta_tipo.iterdir()):
    carpeta_tipo.rmdir()
```

2. Esto verifica si no quedan archivos directamente en `carpeta_tipo`.

#### ✅ Resultado esperado:

Si `data/organizado/txt/` queda así:

```text
txt/
└── 2025-09/
    └── informe.txt
```

...entonces `txt/` NO se borra porque contiene `2025-09`.

Pero si quedara vacío (por ejemplo porque todos los archivos se movieron a subcarpetas y no quedaron más dentro del tipo), entonces se eliminaría.

💡 Si quieres borrar solo si **no hay nada en la jerarquía**, deberías hacerlo de forma recursiva, pero para este caso, basta con borrar si está directamente vacío.