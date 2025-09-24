

## ✅ Reto 1 — Validación de duplicados

> Crea una función `existe_cliente(email: str) -> bool` que devuelva si ya existe un cliente con ese email.

### 🧭 Paso a paso

1. **Define la función** en `sql_demo.py`, preferentemente debajo de `read_clientes`.
2. **Realiza una consulta `SELECT 1` con `WHERE email = ?`.**
3. **Devuelve `True` si hay resultado, `False` si no.**

### ✅ Código

```python
def existe_cliente(email: str) -> bool:
    with closing(connect()) as conn:
        row = conn.execute(
            "SELECT 1 FROM clientes WHERE email = ? LIMIT 1", (email,)
        ).fetchone()
        return row is not None
```

### 🧪 Prueba opcional

Agrega a `demo()` para probarlo:

```python
print("\n→ ¿Existe 'ana@test.com'? →", existe_cliente("ana@test.com"))
print("→ ¿Existe 'otro@test.com'? →", existe_cliente("otro@test.com"))
```

---

## ✅ Reto 2 — Consulta: top ventas por cliente

> Crea una función `ventas_totales_por_cliente() -> list[Row]` con total facturado por cliente.

### 🧭 Paso a paso

1. **Define la función en `sql_demo.py`**, justo debajo de `ventas_detalle`.
2. Escribe una consulta que:

   * haga `JOIN` de ventas con clientes y productos,
   * calcule el `importe = cantidad * precio`,
   * agrupe por cliente,
   * y ordene de mayor a menor.

### ✅ Código

```python
def ventas_totales_por_cliente() -> list[sqlite3.Row]:
    sql = """
    SELECT
        c.nombre AS cliente,
        SUM(v.cantidad * p.precio) AS total
    FROM ventas v
    JOIN clientes c ON c.id = v.id_cliente
    JOIN productos p ON p.id = v.id_producto
    GROUP BY c.id
    ORDER BY total DESC;
    """
    with closing(connect()) as conn:
        return conn.execute(sql).fetchall()
```

### 🧪 Prueba opcional

Agrega en `demo()`:

```python
print("\n→ Totales por cliente:")
for row in ventas_totales_por_cliente():
    print(f"   {row['cliente']:<6} | total = {row['total']:.2f}")
```

---

## ✅ Reto 3 — Alta de venta con validación

> Crea `registrar_venta(id_cliente, id_producto, cantidad)` con validación previa.

### 🧭 Paso a paso

1. **Define la función debajo de `delete_cliente`.**
2. Usa `SELECT` para comprobar que existe `id_cliente` y `id_producto`.
3. Solo si ambos existen, haz un `INSERT INTO ventas(...)`.

### ✅ Código

```python
def registrar_venta(id_cliente: int, id_producto: int, cantidad: int) -> bool:
    with closing(connect()) as conn, conn:
        cur = conn.cursor()

        # Validar existencia
        c = cur.execute("SELECT 1 FROM clientes WHERE id = ?", (id_cliente,)).fetchone()
        p = cur.execute("SELECT 1 FROM productos WHERE id = ?", (id_producto,)).fetchone()

        if c is None or p is None:
            return False

        cur.execute(
            "INSERT INTO ventas(id_cliente, id_producto, cantidad) VALUES (?, ?, ?)",
            (id_cliente, id_producto, cantidad)
        )
        return True
```

### 🧪 Prueba opcional

Agrega en `demo()`:

```python
print("\n→ Registrar nueva venta (cliente 2, producto 1, cantidad 2):")
ok = registrar_venta(2, 1, 2)
print("   OK" if ok else "   Falló")

print("\n→ Registrar venta con cliente inexistente (id=99):")
ok = registrar_venta(99, 1, 1)
print("   OK" if ok else "   Falló")
```

