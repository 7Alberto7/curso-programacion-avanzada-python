
## ✅ Reto 1 — ¿Qué productos compró un cliente?

**Objetivo:** permitir consultar los productos que ha comprado un cliente por su nombre.

---

### Paso 1 – Partimos del DataFrame ya unido

Asumimos que el alumno ya ejecutó:

```python
df = cargar_y_unir()
```

Esto genera un DataFrame con estas columnas:

```python
['id_cliente', 'nombre', 'email', 'producto', 'cantidad', 'precio', 'importe']
```

---

### Paso 2 – Crear la función

Creamos una función que recibe el nombre del cliente como argumento y devuelve una lista de productos distintos que ha comprado:

```python
def productos_por_cliente(nombre_cliente: str) -> list[str]:
    df = cargar_y_unir()  # volvemos a cargar si no lo tenemos
    productos = df.loc[df["nombre"] == nombre_cliente, "producto"].unique()
    return productos.tolist()
```

---

### Paso 3 – Probar la función

```python
print(productos_por_cliente("Ana"))
# Posible salida: ['Portátil', 'Monitor']
```

✅ Este reto refuerza el uso de filtros (`df.loc`) y extracción de columnas (`unique()`).

---

## ✅ Reto 2 — Clientes que compraron más de X €

**Objetivo:** generar una tabla de clientes cuyo importe total supere un umbral.

---

### Paso 1 – Agrupar por cliente y sumar importes

```python
def clientes_con_gasto_minimo(min_importe: float) -> pd.DataFrame:
    df = cargar_y_unir()
    resumen = (df.groupby(["nombre"], as_index=False)["importe"]
                  .sum()
                  .rename(columns={"importe": "total_gastado"}))
```

---

### Paso 2 – Filtrar por umbral

```python
    filtrado = resumen[resumen["total_gastado"] > min_importe]
    return filtrado.sort_values("total_gastado", ascending=False)
```

---

### Paso 3 – Probar con un ejemplo

```python
print(clientes_con_gasto_minimo(200))
# Posible salida:
#   nombre  total_gastado
#   Ana       1080.0
```

✅ Este reto practica `groupby`, `rename`, filtros booleanos y ordenación.

---

## ✅ Reto 3 — Añadir columna "caro/barato"

**Objetivo:** añadir una columna categórica según el precio unitario del producto.

---

### Paso 1 – Crear la función

```python
def etiquetar_segmento(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  # para no modificar el original
    df["segmento_precio"] = df["precio"].apply(lambda p: "caro" if p >= 200 else "barato")
    return df
```

🟰 Alternativa con `np.where()`:

```python
import numpy as np

df["segmento_precio"] = np.where(df["precio"] >= 200, "caro", "barato")
```

---

### Paso 2 – Usar la función y verificar

```python
df = cargar_y_unir()
df_segmentado = etiquetar_segmento(df)
print(df_segmentado[["producto", "precio", "segmento_precio"]].drop_duplicates())
```

✅ Este reto es útil para aprender a crear nuevas columnas con lógica condicional.
