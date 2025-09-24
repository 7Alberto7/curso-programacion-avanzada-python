
## 🔸 Reto 1 — Normalizar booleanos XML → Python

### 🎯 Objetivo

Convertir los valores `"true"` y `"false"` (strings) del XML en los booleanos `True` y `False`.

---

### 🧩 Paso a paso

#### 1. Detectar las cadenas `"true"` y `"false"` (ignorando mayúsculas)

```python
if isinstance(v, str) and v.lower() in ("true", "false"):
```

#### 2. Convertirlas a booleanos reales

```python
conv[k] = v.lower() == "true"
```

#### 3. Integrar en `normalizar_tipos`

```python
def normalizar_tipos(dataset: list[dict]) -> list[dict]:
    norm = []
    for row in dataset:
        conv = {}
        for k, v in row.items():
            if isinstance(v, str):
                if v.isdigit():
                    conv[k] = int(v)
                elif v.lower() in ("true", "false"):
                    conv[k] = v.lower() == "true"
                else:
                    conv[k] = v
            else:
                conv[k] = v
        norm.append(conv)
    return norm
```

---

## 🔸 Reto 2 — Añadir campo de fecha y convertirlo a `datetime.date`

### 🎯 Objetivo

Agregar fechas al dataset y convertirlas a objetos `datetime.date` tras cargar XML (donde se guarda como string).

---

### 🧩 Paso a paso

#### 1. Añadir fechas al dataset (en `main.py`)

```python
usuarios = [
    {"nombre": "Ana", "edad": 30, "activo": True, "fecha_registro": "2025-09-20"},
    {"nombre": "Luis", "edad": 25, "activo": False, "fecha_registro": "2025-08-15"},
    {"nombre": "Marta", "edad": 28, "activo": True, "fecha_registro": "2025-07-01"},
]
```

#### 2. Importar `datetime.date` y parsear fechas ISO

```python
from datetime import datetime, date

def normalizar_tipos(dataset: list[dict]) -> list[dict]:
    norm = []
    for row in dataset:
        conv = {}
        for k, v in row.items():
            if isinstance(v, str):
                if v.isdigit():
                    conv[k] = int(v)
                elif v.lower() in ("true", "false"):
                    conv[k] = v.lower() == "true"
                elif k == "fecha_registro":
                    try:
                        conv[k] = datetime.strptime(v, "%Y-%m-%d").date()
                    except ValueError:
                        conv[k] = v  # deja la string si falla
                else:
                    conv[k] = v
            else:
                conv[k] = v
        norm.append(conv)
    return norm
```

---

## 🔸 Reto 3 — Añadir soporte para CSV y convertirlo a JSON

### 🎯 Objetivo

Leer y escribir CSV como lista de diccionarios, y convertirlo a JSON.

---

### 🧩 Paso a paso

#### 1. Añadir funciones en `app/conversion.py`

```python
import csv

def guardar_csv(datos: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)

def cargar_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
```

#### 2. Guardar y cargar CSV desde `main.py`

```python
from app.conversion import guardar_csv, cargar_csv

def fase3():
    ...
    guardar_csv(usuarios, ds_dir / "usuarios.csv")
    data_csv = cargar_csv(ds_dir / "usuarios.csv")
    print("CSV →", data_csv)
```

#### 3. (Opcional) Convertir CSV ⇄ JSON

Ya puedes:

* Cargar un `.csv` → guardar como `.json`:

```python
data_csv = cargar_csv(Path("usuarios.csv"))
guardar_json(data_csv, Path("usuarios_from_csv.json"))
```

* Y a la inversa:

```python
data_json = cargar_json(Path("usuarios.json"))
guardar_csv(data_json, Path("usuarios_from_json.csv"))
```

---

## ✅ Validación

Tras estos cambios puedes:

* Confirmar que las equivalencias entre formatos se mantienen.
* Imprimir los tipos en consola para verificar que booleanos y fechas se interpretan correctamente.
* Usar el CSV como entrada o salida alternativa a JSON.
