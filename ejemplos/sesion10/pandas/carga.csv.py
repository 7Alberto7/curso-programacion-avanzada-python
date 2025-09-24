import pandas as pd

ventas = pd.read_csv('ventas.csv')
clientes = pd.read_csv('clientes.csv')

ventas_enero = pd.read_csv('ventas.enero.csv')
ventas_febrero = pd.read_csv('ventas.febrero.csv')

print (ventas)


# calcular importe total

ventas["total"] = ventas["precio"] * ventas["cantidad"]


print(ventas)

# merge de ventas por cliente

ventas_cliente = pd.merge(ventas, clientes, on='id_cliente')


print(ventas_cliente)


 # ejemplo de groupby   total vendido por cliente


total_por_cliente = ventas_cliente.groupby("nombre")["total"].sum().reset_index()

print(total_por_cliente)




# concatena meses


ventas_full = pd.concat([ventas_enero,ventas_febrero], ignore_index=True)


print(ventas_full)


consolidado = ventas_full.groupby(['producto','id_cliente'])[["cantidad","precio"]].sum().reset_index()

print(consolidado)


consolidado["total"] = consolidado["precio"] * consolidado["cantidad"]

print (consolidado)
