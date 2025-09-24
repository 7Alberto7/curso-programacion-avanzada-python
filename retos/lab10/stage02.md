## ✅ Reto 1 — ¿Existe cliente por email?

**Enunciado:**

> Crea una función `existe_cliente(email: str) -> bool` que devuelva `True` si hay un cliente con ese email.

---

### Paso 1: Importar las colecciones

Necesitamos acceso a la colección `clientes`, usando la función ya existente `get_collections()`:

```python
clientes, _, _ = get_collections()
```

---

### Paso 2: Buscar cliente por email

Usamos `find_one()` con filtro `{"email": email}`. Si devuelve un documento, existe.

---

### Paso 3: Implementar función completa

```python
def existe_cliente(email: str) -> bool:
    clientes, _, _ = get_collections()
    return clientes.find_one({"email": email}) is not None
```

---

### Paso 4: Probar desde `demo_crud()`

```python
print("\n→ ¿Existe cliente 'ana@test.com'?")
print("   Resultado:", existe_cliente("ana@test.com"))  # True

print("\n→ ¿Existe cliente 'noexiste@test.com'?")
print("   Resultado:", existe_cliente("noexiste@test.com"))  # False
```

---

## ✅ Reto 2 — Importes totales por cliente

**Enunciado:**

> Crea una función `totales_por_cliente() -> list[dict]` que devuelva cliente + total facturado.

---

### Paso 1: Recordar estructura de ventas

Cada documento en `ventas` tiene `id_cliente`, `id_producto`, `cantidad`.

Necesitamos:

* `lookup` a `productos` para obtener precio.
* `lookup` a `clientes` para obtener nombre.
* `$group` por cliente para sumar importe (`cantidad × precio`).

---

### Paso 2: Escribir aggregation pipeline

```python
pipeline = [
    {"$lookup": {
        "from": "clientes",
        "localField": "id_cliente",
        "foreignField": "_id",
        "as": "cliente"
    }},
    {"$lookup": {
        "from": "productos",
        "localField": "id_producto",
        "foreignField": "_id",
        "as": "producto"
    }},
    {"$unwind": "$cliente"},
    {"$unwind": "$producto"},
    {"$addFields": {
        "importe": {"$multiply": ["$cantidad", "$producto.precio"]}
    }},
    {"$group": {
        "_id": "$cliente.nombre",
        "total": {"$sum": "$importe"}
    }},
    {"$sort": {"total": -1}}
]
```

---

### Paso 3: Implementar función

```python
def totales_por_cliente() -> list[dict]:
    _, _, ventas = get_collections()
    pipeline = [ ... ]  # como el anterior
    return list(ventas.aggregate(pipeline))
```

---

### Paso 4: Probar desde `demo_crud()`

```python
print("\n→ Totales por cliente:")
for doc in totales_por_cliente():
    print("   ", doc)
```

✔️ Ejemplo de salida:

```txt
→ Totales por cliente:
    {'_id': 'Ana', 'total': 1080.0}
    {'_id': 'Marta', 'total': 190.0}
    {'_id': 'Luis', 'total': 50.0}
```

---

## ✅ Reto 3 — Insertar venta validando IDs

**Enunciado:**

> Crea una función `insertar_venta(id_cliente, id_producto, cantidad)` que:
>
> * compruebe que existen cliente y producto,
> * y si es así, inserte la venta.

---

### Paso 1: Validar existencia previa

Usamos `find_one()` con `_id` tanto en `clientes` como `productos`.

---

### Paso 2: Insertar solo si es válido

```python
def insertar_venta(id_cliente: int, id_producto: int, cantidad: int = 1) -> bool:
    clientes, productos, ventas = get_collections()
    
    if not clientes.find_one({"_id": id_cliente}):
        print(f"⚠️ Cliente {id_cliente} no existe.")
        return False
    
    if not productos.find_one({"_id": id_producto}):
        print(f"⚠️ Producto {id_producto} no existe.")
        return False
    
    if cantidad <= 0:
        print(f"⚠️ Cantidad inválida: {cantidad}")
        return False

    ventas.insert_one({
        "id_cliente": id_cliente,
        "id_producto": id_producto,
        "cantidad": cantidad
    })
    print(f"✅ Venta insertada correctamente.")
    return True
```

---

### Paso 3: Probar con casos reales

```python
print("\n→ Insertar venta válida")
insertar_venta(1, 2, 1)

print("\n→ Insertar venta con cliente inexistente")
insertar_venta(99, 2, 1)

print("\n→ Insertar venta con cantidad negativa")
insertar_venta(1, 2, -5)
```

✔️ Esto demuestra validaciones básicas y control de errores.