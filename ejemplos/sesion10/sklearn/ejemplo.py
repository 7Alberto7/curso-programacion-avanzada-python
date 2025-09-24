import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression



# Dataset de ejemplo
df = pd.DataFrame({
    "precio": [50, 100, 200],
    "cantidad": [5, 2, 8]
})

X = df[["precio", "cantidad"]]

scaler = StandardScaler()
X_norm = scaler.fit_transform(X)

print(X_norm)


# Etiqueta: producto caro si precio > 100
y = (df["precio"] > 100).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.3, random_state=42)

modelo = LogisticRegression()
modelo.fit(X_train, y_train)

print("Accuracy:", modelo.score(X_test, y_test))

nuevo_producto = pd.DataFrame([[1200, 3]], columns=["precio", "cantidad"])


prediccion = modelo.predict(scaler.transform(nuevo_producto))



print('es caro??', "Si" if prediccion[0] ==1 else "No" )