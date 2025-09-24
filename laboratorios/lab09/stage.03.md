# 🔹 Fase 3 — Conversión entre formatos (JSON, Pickle, XML)

### 🎯 Objetivo

Crear utilidades para **guardar** y **cargar** datasets en **JSON**, **Pickle** y **XML**, y comprobar que el contenido es **equivalente** tras las conversiones.

---

## 🧭 Código

**app/conversion.py**

```python
from __future__ import annotations
from pathlib import Path
import json, pickle
import xml.etree.ElementTree as ET

# ---------- JSON ----------
def guardar_json(datos: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def cargar_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# ---------- Pickle ----------
def guardar_pickle(datos: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(datos, f)

def cargar_pickle(path: Path) -> list[dict]:
    with path.open("rb") as f:
        return pickle.load(f)

# ---------- XML ----------
def guardar_xml(datos: list[dict], path: Path, root_name: str = "items", item_name: str = "item") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    root = ET.Element(root_name)
    for row in datos:
        node = ET.SubElement(root, item_name)
        for k, v in row.items():
            el = ET.SubElement(node, str(k))
            el.text = "" if v is None else str(v)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

def cargar_xml(path: Path, item_name: str = "item") -> list[dict]:
    tree = ET.parse(path)
    root = tree.getroot()
    out: list[dict] = []
    for node in root.findall(item_name):
        row: dict = {}
        for child in list(node):
            row[child.tag] = child.text
        out.append(row)
    return out

# ---------- Utilidades de equivalencia ----------
def normalizar_tipos(dataset: list[dict]) -> list[dict]:
    """
    Normaliza valores para comparar equivalencia entre formatos (XML guarda todo como texto).
    Intento simple: convertir dígitos a int si procede.
    """
    norm = []
    for row in dataset:
        conv = {}
        for k, v in row.items():
            if isinstance(v, str) and v.isdigit():
                conv[k] = int(v)
            else:
                conv[k] = v
        norm.append(conv)
    return norm
```

**main.py** (añade una función para la Fase 3 y la llamada)

```python
from pathlib import Path
from app.organizador import organizar_por_tipo, organizar_por_fecha
from app.conversion import (
    guardar_json, cargar_json,
    guardar_pickle, cargar_pickle,
    guardar_xml, cargar_xml,
    normalizar_tipos,
)

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

def fase3():
    print("== Fase 3: conversión entre formatos (JSON, Pickle, XML) ==")
    ds_dir = Path("data/datasets")
    ds_dir.mkdir(parents=True, exist_ok=True)

    # Dataset de ejemplo
    usuarios = [
        {"nombre": "Ana", "edad": 30, "activo": True},
        {"nombre": "Luis", "edad": 25, "activo": False},
        {"nombre": "Marta", "edad": 28, "activo": True},
    ]

    # Guardar
    guardar_json(usuarios, ds_dir / "usuarios.json")
    guardar_pickle(usuarios, ds_dir / "usuarios.pkl")
    guardar_xml(usuarios, ds_dir / "usuarios.xml", root_name="usuarios", item_name="usuario")

    # Cargar
    data_json = cargar_json(ds_dir / "usuarios.json")
    data_pkl  = cargar_pickle(ds_dir / "usuarios.pkl")
    data_xml  = cargar_xml(ds_dir / "usuarios.xml", item_name="usuario")

    # Comprobación de equivalencia (XML convierte a texto; normalizamos)
    eq_json_pkl = data_json == data_pkl
    eq_json_xml = data_json == normalizar_tipos(data_xml)

    print(f"JSON ⇄ Pickle equivalentes: {eq_json_pkl}")
    print(f"JSON ⇄ XML equivalentes (normalizado): {eq_json_xml}")

if __name__ == "__main__":
    # Ejecuta las fases que quieras; aquí corremos la 3 directamente.
    # fase1(); fase2()
    fase3()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada (ejemplo):**

```
== Fase 3: conversión entre formatos (JSON, Pickle, XML) ==
JSON ⇄ Pickle equivalentes: True
JSON ⇄ XML equivalentes (normalizado): True
```

---

## ✅ Criterios de aceptación

* Se generan tres ficheros en `data/datasets`: `usuarios.json`, `usuarios.pkl`, `usuarios.xml`.
* Las cargas desde cada formato reconstruyen el dataset original (teniendo en cuenta la **normalización** para XML).
* Se imprime el estado de **equivalencia** entre formatos.



## ✅ Retos

### 🔸 Reto 1 — Normaliza booleanos XML → Python

**Objetivo:**
Extiende `normalizar_tipos` para que convierta `"true"` y `"false"` (como cadenas) en los booleanos `True` y `False` cuando sea posible.

> Esto te enseña a manejar casos típicos donde el tipo real se pierde durante la serialización, como ocurre con XML.

---

### 🔸 Reto 2 — Añade campo de fecha y conviértelo

**Objetivo:**
Agrega un campo `"fecha_registro"` al dataset con valores tipo `"2025-09-20"`, y adapta `normalizar_tipos` para convertirlo en `datetime.date`.

> Este reto es útil para validar fechas, usar formatos ISO y convertir correctamente cadenas a objetos `datetime.date`.

---

### 🔸 Reto 3 — Soporta CSV y convierte a JSON

**Objetivo:**
Agrega soporte básico para CSV:

* Guardar lista de diccionarios a `.csv`
* Leer desde `.csv` a lista de diccionarios
* Permitir conversión CSV ⇄ JSON

> Ideal para entender el formato más común en exportaciones de datos y cómo convertir entre texto tabular ↔ estructuras jerárquicas.


---

# ✅ Conclusión del Laboratorio 9

**Lo que has logrado:**

* **Organizaste** ficheros por **tipo** y **fecha** utilizando `pathlib`, `os` y `shutil`.
* **Serializaste** y **deserializaste** datasets con **JSON**, **Pickle** y **XML**.
* Definiste un criterio de **equivalencia** entre formatos, resolviendo diferencias de tipos (ej. strings en XML).

**Ideas clave:**

* `pathlib` simplifica el trabajo con rutas; `shutil` facilita operaciones de alto nivel (copiar/mover).
* El formato **JSON** es el candidato por defecto para **intercambio**; **Pickle** para **persistencia local** entre versiones/entornos controlados; **XML** cuando se necesita **estructura jerárquica** o compatibilidad **legacy**.
* En conversiones, define reglas de **normalización** para mantener integridad semántica (tipos, nulos, fechas, booleanos).

