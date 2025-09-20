# 🔹 Fase 2 — Organizar ficheros por **fecha** (YYYY-MM) dentro de cada tipo

### 🎯 Objetivo

Tomar lo ya organizado por **extensión** en `data/organizado/` y, **dentro de cada carpeta de tipo**, mover los archivos a subcarpetas por **año-mes** (`2025-09/`) usando la fecha de **modificación** del fichero.

---

## 🧭 Código

**app/organizador.py** (añade esta función debajo de `organizar_por_tipo`)

```python
from pathlib import Path
import shutil
from datetime import datetime

def organizar_por_fecha(base: Path) -> None:
    """
    Dentro de cada carpeta de tipo en `base`, mueve los archivos a subcarpetas YYYY-MM
    según su fecha de modificación (mtime).
    """
    if not base.exists():
        return

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
            print(f"Movido por fecha: {archivo.name} → {destino}/")
```

**main.py** (amplía para llamar a Fase 2 después de Fase 1)

```python
from pathlib import Path
from app.organizador import organizar_por_tipo, organizar_por_fecha

def fase1():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")
    print("== Fase 1: organizar por tipo ==")
    organizar_por_tipo(entrada, salida)
    print("✔ Archivos organizados por extensión")

def fase2():
    salida = Path("data/organizado")
    print("== Fase 2: organizar por fecha (YYYY-MM) ==")
    organizar_por_fecha(salida)
    print("✔ Archivos organizados por fecha dentro de cada tipo")

if __name__ == "__main__":
    # Ejecuta Fase 1 y luego Fase 2 (o solo Fase 2 si ya hiciste la 1)
    fase1()
    fase2()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada (ejemplo):**

```
== Fase 1: organizar por tipo ==
Movido: informe.txt → data/organizado/txt/
...
✔ Archivos organizados por extensión
== Fase 2: organizar por fecha (YYYY-MM) ==
Movido por fecha: informe.txt → data/organizado/txt/2025-09/
...
✔ Archivos organizados por fecha dentro de cada tipo
```

---

## ✅ Resultado esperado en disco

```
data/organizado/
├─ txt/
│  └─ 2025-09/
│      └─ informe.txt
├─ csv/
│  └─ 2024-12/
│      └─ ventas.csv
└─ jpg/
   └─ 2023-07/
       └─ foto.jpg
```

---

## 🔧 Notas y buenas prácticas

* Usamos **mtime** (fecha de modificación). Si prefieres **ctime**/creación, adapta `stat()`.
* Para **fechas forzadas** en pruebas, puedes tocar mtime con `os.utime(path, (atime, mtime))`.
* Si una carpeta de tipo queda **vacía** tras mover, puedes limpiarla con `carpeta_tipo.rmdir()` (opcional).

---

Perfecto, la **Fase 2** está clara y bien diseñada. Vamos a revisar y quedarnos con **solo 3 retos**, como acordamos, manteniendo:

* Claridad y brevedad
* Progresión lógica
* Alineación con los objetivos de la sesión 9.2
* Aplicación directa sobre el scaffold

---



## 🔁 Retos 

---

### 🔸 Reto 1 — Organiza los archivos por fecha de modificación

**🎯 Objetivo:**
Dentro de cada carpeta de tipo, agrupa los archivos por subcarpeta `YYYY-MM`.

🔧 **Qué hacer:**

* Usa `archivo.stat().st_mtime` para obtener la fecha de modificación.
* Convierte a formato `YYYY-MM` con `datetime.fromtimestamp()`.
* Crea subcarpetas por mes y mueve allí los archivos.

🧠 **Qué se trabaja:**

* Manipulación de fechas en base a timestamps.
* Agrupación de ficheros en estructuras cronológicas.
* Uso combinado de `Path`, `datetime`, `shutil`.

---

### 🔸 Reto 2 — Ignora archivos que ya están en carpetas `YYYY-MM`

**🎯 Objetivo:**
Evitar reordenar archivos que ya han sido movidos correctamente.

🔧 **Qué hacer:**

* Antes de mover un archivo, comprueba si su **padre ya es una carpeta tipo `YYYY-MM`** (suficiente con ver si el nombre coincide con el patrón `20XX-XX`).
* Si ya está allí, **sáltalo**.

🧠 **Qué se trabaja:**

* Validación previa al movimiento para evitar duplicidad o errores.
* Escritura de scripts **idempotentes** (pueden ejecutarse varias veces sin alterar el resultado).

---

### 🔸 Reto 3 — Borra carpetas de tipo que hayan quedado vacías

**🎯 Objetivo:**
Limpiar la estructura de carpetas para que solo queden las subcarpetas `YYYY-MM`.

🔧 **Qué hacer:**

* Tras mover todos los archivos, comprueba si cada carpeta de tipo está vacía.
* Si lo está, bórrala con `.rmdir()`.

```python
if not any(carpeta_tipo.iterdir()):
    carpeta_tipo.rmdir()
```

🧠 **Qué se trabaja:**

* Limpieza estructural post-operación.
* Gestión cuidadosa del sistema de ficheros para evitar errores.
