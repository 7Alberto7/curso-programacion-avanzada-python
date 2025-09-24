## ✅ Reto 1 — Clasificación binaria con distinto umbral (300 €)

**Paso 1 — Editar la función `clasificacion_importe()`**

Abre el archivo `app/ml_models.py` y localiza esta función:

```python
def clasificacion_importe(umbral: float = 200.0) -> float:
```

**Paso 2 — Cambiar el umbral a 300.0 al llamarla**

En la función `main()` cambia la llamada así:

```python
acc = clasificacion_importe(umbral=300.0)
```

**Paso 3 — Ejecutar y observar resultados**

```bash
python -m app.ml_models
```

Revisa si el `accuracy` aumenta o disminuye. Esto te ayuda a entender cómo afecta el umbral a la distribución de clases (`alto = 1` o `0`).

---

## ✅ Reto 2 — ¿Cuál es el impacto de normalizar?

**Paso 1 — Crear una nueva función `regresion_sin_escalar()`**

Dentro del archivo `ml_models.py`, añade debajo de `regresion_precio()`:

```python
def regresion_sin_escalar() -> float:
    """Regresión sin escalar la variable 'cantidad'."""
    df = load_dataset()
    X = df[["cantidad"]].values
    y = df["precio"].values

    reg = LinearRegression()
    reg.fit(X, y)
    r2 = reg.score(X, y)
    return r2
```

**Paso 2 — Llamar a esta función desde `main()`**

Añade esto en `main()`:

```python
print("\n== Regresión sin escalar ==")
r2_sin = regresion_sin_escalar()
print(f"R² sin escalar = {r2_sin:.2f}")
```

**Paso 3 — Ejecutar y comparar**

Ejecuta:

```bash
python -m app.ml_models
```

Compara los valores `R²` de la regresión normal y sin escalar. Comprobarás que para **modelos lineales simples**, el escalado no altera el resultado, pero es importante para modelos que usan distancias (p. ej., KNN, SVM).

---

## ✅ Reto 3 — Predice el precio para cantidad=12

**Paso 1 — Editar `regresion_precio()`**

Añade una predicción extra al final de la función:

```python
pred_12 = reg.predict([[12]])[0]
return r2, coef, inter, pred_10, pred_12
```

Y cambia el encabezado a:

```python
def regresion_precio() -> tuple[float, float, float, float, float]:
```

**Paso 2 — Ajustar el `main()`**

Actualiza la llamada y el `print()`:

```python
r2, coef, inter, pred_10, pred_12 = regresion_precio()
print(f"Predicción para cantidad=10 → {pred_10:.2f}")
print(f"Predicción para cantidad=12 → {pred_12:.2f}")
```

**Paso 3 — Ejecutar y reflexionar**

```bash
python -m app.ml_models
```

Verás la predicción para `cantidad=12`. Evalúa si el precio proyectado tiene sentido, especialmente si la relación entre cantidad y precio en tus datos reales es fuerte.