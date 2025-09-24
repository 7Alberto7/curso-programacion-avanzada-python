# 🔹 Fase 1 — Organizar ficheros por tipo

### 🎯 Objetivo

Mover los archivos desde la carpeta `data/entrada/` a subcarpetas en `data/organizado/` según su **extensión** (`.txt`, `.csv`, `.jpg`, etc.).

---

## 🧱 Scaffold inicial

```
lab9_files_serialization/
├─ data/
│  ├─ entrada/
│  │   ├─ informe.txt
│  │   ├─ ventas.csv
│  │   ├─ foto.jpg
│  │   └─ script.py
│  └─ organizado/       # aquí se crearán subcarpetas
└─ app/
   ├─ __init__.py
   └─ organizador.py
```

---

## 🧭 Código

**app/organizador.py**

```python
from pathlib import Path
import shutil

def organizar_por_tipo(src: Path, dst: Path) -> None:
    """
    Organiza archivos de src en carpetas según su extensión dentro de dst.
    """
    dst.mkdir(parents=True, exist_ok=True)

    for archivo in src.iterdir():
        if archivo.is_file():
            # obtener extensión sin el punto
            ext = archivo.suffix.lstrip(".").lower() or "otros"
            carpeta_destino = dst / ext
            carpeta_destino.mkdir(parents=True, exist_ok=True)

            # mover archivo
            shutil.move(str(archivo), carpeta_destino / archivo.name)
            print(f"Movido: {archivo.name} → {carpeta_destino}/")
```

**main.py**

```python
from pathlib import Path
from app.organizador import organizar_por_tipo

def fase1():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")

    print("== Fase 1: organizar por tipo ==")
    organizar_por_tipo(entrada, salida)
    print("✔ Archivos organizados por extensión")

if __name__ == "__main__":
    fase1()
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
Movido: ventas.csv → data/organizado/csv/
Movido: foto.jpg → data/organizado/jpg/
Movido: script.py → data/organizado/py/
✔ Archivos organizados por extensión
```

---

## ✅ Resultado esperado en disco

```
data/organizado/
├─ txt/
│  └─ informe.txt
├─ csv/
│  └─ ventas.csv
├─ jpg/
│  └─ foto.jpg
└─ py/
   └─ script.py
```


## 🔁 Retos

---

### 🔸 Reto 1 — Clasifica archivos por extensión

**🎯 Objetivo:** Mover los archivos a carpetas nombradas según su tipo (extensión).

🔧 **Qué hacer:**

* Recorre `data/entrada/`.
* Detecta la extensión del archivo (`Path.suffix`).
* Crea una subcarpeta en `data/organizado/{extensión}`.
* Mueve el archivo a su carpeta correspondiente.

🧠 **Qué aprendo:**

* A trabajar con rutas (`Path`).
* A usar `shutil.move()` para reorganizar archivos por tipo.

---

### 🔸 Reto 2 — Maneja archivos sin extensión

**🎯 Objetivo:** Detectar archivos sin extensión y organizarlos correctamente.

🔧 **Qué hacer:**

* Si un archivo no tiene extensión (`archivo.suffix == ""`), colócalo en la subcarpeta `otros/`.

🧠 **Qué aprendo:**

* A cubrir casos especiales y prevenir errores.
* A hacer el script más robusto.

---

### 🔸 Reto 3 — Ignora archivos ocultos

**🎯 Objetivo:** Evitar mover archivos que empiezan por `"."` (como `.DS_Store`, `.gitkeep`, etc.).

🔧 **Qué hacer:**

* Añade una condición que descarte archivos cuyo nombre comienza con `"."`.

```python
if archivo.name.startswith("."):
    continue
```

🧠 **Qué aprendo:**

* A evitar errores molestos por archivos ocultos del sistema o de Git.
* A filtrar adecuadamente archivos que no deben procesarse.
