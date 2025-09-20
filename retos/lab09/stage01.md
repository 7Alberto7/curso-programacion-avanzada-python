## ✅ Resoluciones · Fase 1 — Organizar ficheros por tipo

---

### 🔸 Reto 1 — Clasifica archivos por extensión

#### 🧠 Proceso

Queremos mover archivos desde `data/entrada/` a subcarpetas en `data/organizado/`, agrupándolos según su **extensión** (`.txt`, `.csv`, etc.). Para eso:

* Extraemos `.suffix` del archivo (incluye el punto, como `.txt`).
* Lo usamos como nombre de carpeta (sin el punto).
* Creamos la carpeta si no existe.
* Movemos el archivo allí.

#### 🧩 Pasos:

1. En `organizador.py`, define la función:

```python
from pathlib import Path
import shutil

def organizar_por_tipo(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    
    for archivo in src.iterdir():
        if archivo.is_file():
            ext = archivo.suffix.lstrip(".").lower() or "otros"
            carpeta = dst / ext
            carpeta.mkdir(parents=True, exist_ok=True)
            shutil.move(str(archivo), carpeta / archivo.name)
```

2. En `main.py`, llama a esta función desde `fase1()`:

```python
from app.organizador import organizar_por_tipo
from pathlib import Path

def fase1():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")
    organizar_por_tipo(entrada, salida)
```

3. Ejecuta:

```bash
python main.py
```

#### 🧪 Validación esperada:

Si hay estos archivos:

```
data/entrada/
├─ informe.txt
├─ ventas.csv
├─ foto.jpg
```

Se moverán a:

```
data/organizado/
├─ txt/informe.txt
├─ csv/ventas.csv
├─ jpg/foto.jpg
```

#### 💡 Aprendo que:

* `Path.suffix` es ideal para detectar tipos de archivo.
* `shutil.move` mueve archivos de forma segura y crea el destino si lo preparamos.

---

### 🔸 Reto 2 — Maneja archivos sin extensión

#### 🧠 Proceso mental

Si un archivo no tiene extensión (`.suffix == ""`), `.lstrip(".")` da `""`.
Debemos usar una carpeta por defecto como `"otros"`.

#### 🧩 Pasos:

1. En el mismo bucle, asegúrate de usar:

```python
ext = archivo.suffix.lstrip(".").lower() or "otros"
```

Esto garantiza que si `.suffix` es vacío, `ext` será `"otros"`.

2. El resto del código no cambia: el archivo se moverá a `data/organizado/otros/`.

#### 🧪 Validación esperada:

Si hay un archivo `README` (sin extensión):

```
data/entrada/
├─ README
```

Se moverá a:

```
data/organizado/otros/README
```

#### 💡 Aprendo que:

* Hay que pensar en todos los casos reales, no solo los “bonitos”.
* Python permite manejar estos casos con una expresión simple (`or "otros"`).

---

### 🔸 Reto 3 — Ignora archivos ocultos

#### 🧠 Proceso mental

Los archivos que comienzan por `"."` (como `.DS_Store` o `.gitkeep`) **no deberían moverse**.
Podrían romper el comportamiento del programa o no tener extensión útil.

#### 🧩 Pasos:

1. Añade esta condición antes de procesar cada archivo:

```python
if archivo.name.startswith("."):
    continue
```

2. Eso descartará cualquier archivo oculto.

#### 🧪 Validación esperada:

Dado:

```
data/entrada/
├─ informe.txt
├─ .DS_Store
```

Solo se moverá `informe.txt`, y `.DS_Store` quedará en su sitio.

#### 💡 Aprendo que:

* Filtrar archivos ocultos es buena práctica para evitar efectos secundarios.
* A veces el sistema operativo o Git crea archivos no deseados.