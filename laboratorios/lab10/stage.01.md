# 🔹 Fase 1 — CRUD en SQLite con `sqlite3`

### 🎯 Objetivo

Crear una BD SQLite con tablas `clientes`, `productos`, `ventas`; poblarla; y realizar **CRUD + consultas** (incluye `JOIN` y cálculo de importes).

---

## 🧱 Estructura mínima

```
lab10_db_ml/
├─ data/
│  └─ sqlite/          # se creará la BD aquí
└─ app/
   └─ sql_demo.py
```

---

## 🧭 Código (app/sql\_demo.py)

```python
# app/sql_demo.py
from __future__ import annotations
import sqlite3
from pathlib import Path
from contextlib import closing

DB_PATH = Path("data/sqlite/usuarios.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DDL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  precio REAL NOT NULL CHECK (precio >= 0)
);
CREATE TABLE IF NOT EXISTS ventas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL,
  id_producto INTEGER NOT NULL,
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  FOREIGN KEY(id_cliente)  REFERENCES clientes(id)  ON DELETE CASCADE,
  FOREIGN KEY(id_producto) REFERENCES productos(id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS ix_ventas_cliente ON ventas(id_cliente);
CREATE INDEX IF NOT EXISTS ix_ventas_producto ON ventas(id_producto);
"""

def connect():
    conn = sqlite3.connect(DB_PATH)
    # devolver filas como dict-like (acceso por nombre de columna)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    with closing(connect()) as conn, conn:  # autocommit/rollback
        cur = conn.cursor()
        for stmt in [s.strip() for s in DDL.split(";") if s.strip()]:
            cur.execute(stmt)

def seed():
    with closing(connect()) as conn, conn:
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO clientes(nombre, email) VALUES (?, ?)",
            [("Ana","ana@test.com"), ("Luis","luis@test.com"), ("Marta","marta@test.com")]
        )
        cur.executemany(
            "INSERT OR IGNORE INTO productos(nombre, precio) VALUES (?, ?)",
            [("Portátil", 900.0), ("Monitor", 180.0), ("Teclado", 25.0)]
        )
        # ventas (id_cliente, id_producto, cantidad)
        cur.executemany(
            "INSERT INTO ventas(id_cliente, id_producto, cantidad) VALUES (?, ?, ?)",
            [(1,1,1), (1,2,1), (2,3,2), (3,2,1)]
        )

def create_cliente(nombre: str, email: str) -> int:
    with closing(connect()) as conn, conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes(nombre, email) VALUES (?,?)", (nombre, email))
        return cur.lastrowid

def read_clientes() -> list[sqlite3.Row]:
    with closing(connect()) as conn:
        return conn.execute("SELECT * FROM clientes ORDER BY id").fetchall()

def update_email_cliente(cliente_id: int, nuevo_email: str) -> int:
    with closing(connect()) as conn, conn:
        cur = conn.cursor()
        cur.execute("UPDATE clientes SET email=? WHERE id=?", (nuevo_email, cliente_id))
        return cur.rowcount

def delete_cliente(cliente_id: int) -> int:
    with closing(connect()) as conn, conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        return cur.rowcount

def ventas_detalle() -> list[sqlite3.Row]:
    sql = """
    SELECT
      c.nombre   AS cliente,
      p.nombre   AS producto,
      v.cantidad,
      p.precio,
      (v.cantidad * p.precio) AS importe
    FROM ventas v
    JOIN clientes c  ON c.id = v.id_cliente
    JOIN productos p ON p.id = v.id_producto
    ORDER BY cliente, producto;
    """
    with closing(connect()) as conn:
        return conn.execute(sql).fetchall()

def demo():
    print("→ Inicializando BD y datos…")
    init_db()
    seed()

    print("\n→ CREATE: añadir cliente 'Carlos'")
    nuevo_id = create_cliente("Carlos", "carlos@test.com")
    print("   id nuevo:", nuevo_id)

    print("\n→ READ: listar clientes")
    for row in read_clientes():
        print(f"   {row['id']:>2} | {row['nombre']:<6} | {row['email']}")

    print("\n→ UPDATE: cambiar email de Carlos")
    update_email_cliente(nuevo_id, "carlos@example.com")

    print("\n→ Ventas (JOIN + importe):")
    for row in ventas_detalle():
        print(f"   {row['cliente']:<6} | {row['producto']:<8} | cant={row['cantidad']} | "
              f"precio={row['precio']:.2f} | importe={row['importe']:.2f}")

    print("\n→ DELETE: borrar cliente Carlos")
    delete_cliente(nuevo_id)

    print("\n✔ Fase 1 completada.")

if __name__ == "__main__":
    demo()
```

---

## ▶️ Cómo ejecutar

Desde la raíz del proyecto:

```bash
python -m app.sql_demo
```

**Salida esperada (aprox.):**

```
→ Inicializando BD y datos…

→ CREATE: añadir cliente 'Carlos'
   id nuevo: 4

→ READ: listar clientes
    1 | Ana    | ana@test.com
    2 | Luis   | luis@test.com
    3 | Marta  | marta@test.com
    4 | Carlos | carlos@test.com

→ UPDATE: cambiar email de Carlos

→ Ventas (JOIN + importe):
   Ana    | Portátil | cant=1 | precio=900.00 | importe=900.00
   Ana    | Monitor  | cant=1 | precio=180.00 | importe=180.00
   Luis   | Teclado  | cant=2 | precio=25.00  | importe=50.00
   Marta  | Monitor  | cant=1 | precio=180.00 | importe=180.00

→ DELETE: borrar cliente Carlos

✔ Fase 1 completada.
```

---

## ✅ Criterios de aceptación

* Se crea la BD en `data/sqlite/usuarios.db` con **foreign keys** activas.
* CRUD funcional sobre `clientes` (CREATE/READ/UPDATE/DELETE).
* Consulta con **JOIN** muestra `cliente, producto, cantidad, precio, importe`.
* Restricciones: `UNIQUE(email)`, `CHECK` de `cantidad > 0` y `precio >= 0`.
* Índices creados en `ventas(id_cliente)` y `ventas(id_producto)`.

---

## 🔧 Notas

* El uso de `with closing(connect()) as conn, conn:` asegura **commit/rollback** automático.
* `row_factory = sqlite3.Row` permite acceder por nombre de columna (`row["cliente"]`).
* Para MySQL en lugar de SQLite, migrar a **SQLAlchemy** con un `engine` `mysql+pymysql://…` (opcional).


## ✅ Retos 

### 🧩 Reto 1 — Validación de duplicados

> **Añade una función `existe_cliente(email: str) → bool` que devuelva si ya existe un cliente con ese email.**
> Úsala antes de llamar a `create_cliente` para evitar insertar duplicados manualmente.

🔍 Objetivo: aplicar una consulta `SELECT` con `WHERE` y reforzar la idea de restricciones únicas.

---

### 🧩 Reto 2 — Consulta: top ventas por cliente

> **Crea una función `ventas_totales_por_cliente() → list[Row]` que devuelva el total facturado por cada cliente, ordenado de mayor a menor.**

🔍 Objetivo: practicar `GROUP BY`, `SUM`, y consolidar el uso de joins + agregaciones.

---

### 🧩 Reto 3 — Alta de venta

> **Crea una función `registrar_venta(id_cliente: int, id_producto: int, cantidad: int)` que inserte una nueva fila en la tabla `ventas`.**
> Valida que el cliente y producto existen antes de insertar.

🔍 Objetivo: trabajar el flujo de inserción condicional con foreign keys y reforzar validación previa.
