import pandas as pd

ruta = "https://raw.githubusercontent.com/VMjavier/claseAnalisisDatos/refs/heads/main/veterinaria_colombia.csv"

df = pd.read_csv(ruta)
print("="*50)
print(df.head())
print("="*50)

print("="*50)
print(df.info())
print("="*50)

print("="*50)
print(df.describe())
print("="*50)

print("="*50)
print(df.columns)
print("="*50)

print("="*50)
print(df.isnull().sum())
print("="*50)

print("="*50)
print(df.shape)
print("="*50)

print("="*50)
print(df['Raza'])
print("="*50)

print("="*50)
print(df[['Raza','Especie']])
print("="*50)

print("="*50)
print(df[['Raza','Especie']])
print("="*50)

print("="*50)
print(df[df['Raza'] == 'Criollo'])
print("="*50)

print("="*50)
print(df.columns)
print("="*50)

#Limpieza

print("="*50)
print(df.columns)
print("="*50)

print("="*50)
df.columns = (df.columns.str.strip().str.lower().str.replace(' ','_'))
print("="*50)

print("="*50)
print(df.columns)
print("="*50)

print("="*50)
df.rename(columns = {"nombre": "nombre_mascota"}, inplace = True)
print("="*50)

print("="*50)
print(df.columns)
print("="*50)

#Eliminar filas o columnas completamente vacias

print("="*50)
print(df.dropna(axis = 0, how = "all", inplace = True))
print("="*50)

print("="*50)
print(df.dropna(axis = 1, how = "all", inplace = True))
print("="*50)

print("="*50)
print(df.shape)
print("="*50)

# Eliminar filas o columnas a eleccion

print("="*50)
print(df["nombre_mascota"])
print("="*50)

print("="*50)
print(df.drop(columns = ["nombre_mascota"], inplace = True))
print("="*50)

print("="*50)
print(df.columns)
print("="*50)

