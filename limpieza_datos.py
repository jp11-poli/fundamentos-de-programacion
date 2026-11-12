import pandas as pd

ruta = "https://raw.githubusercontent.com/jp11-poli/datos_concreto.csv/refs/heads/main/Datos_Concreto%20(4).csv"
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
print(df["Cemento (kg/m³)"])
print("="*50)

print("="*50)
print(df[["Cemento (kg/m³)","Escoria de alto horno (kg/m³)"]])
print("="*50)

print("="*50)
print(df["Cemento (kg/m³)"]== "Resistencia a la compresión (MPa)")
print("="*50)