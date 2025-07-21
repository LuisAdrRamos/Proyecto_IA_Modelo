import pandas as pd
import numpy as np
import os
from collections import Counter

# 📁 Rutas
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
input_path = os.path.join(base_path, 'teclados_limpio_sinMembrana.csv')
output_path = os.path.join(base_path, 'train_dataset2.csv')

# 📄 Cargar CSV limpio
df = pd.read_csv(input_path)
print("✅ Archivo base cargado:")
print(df.head())

# 🧠 Función para categorizar el precio
def categorizar_precio(simulado, real):
    porcentaje = (simulado / real) * 100

    if porcentaje <= 60:
        return "Oferton"
    elif porcentaje <= 75:
        return "ExcelenteOferta"
    elif porcentaje <= 90:
        return "BuenPrecio"
    elif 95 <= porcentaje <= 105:
        return "Normal"
    elif porcentaje >= 140:
        return "Estafa"
    elif porcentaje >= 125:
        return "PesimaCompra"
    elif porcentaje >= 110:
        return "MalaCompra"
    else:
        return "Normal"  # entre 91%-94% o 106%-109%

# 🧪 Generar 10 precios simulados por teclado
training_data = []
contador_etiquetas = Counter()

for _, row in df.iterrows():
    nombre = row["Name"]
    real_price = round(row["Price"], 2)

    # Simular precios con mayor variedad (más posibilidad de extremos)
    precios_bajos = np.random.uniform(real_price * 0.4, real_price * 0.7, size=25)
    precios_altos = np.random.uniform(real_price * 0.7, real_price * 1.5, size=25)
    precios_simulados = np.concatenate([precios_bajos, precios_altos])

    for simulated_price in precios_simulados:
        simulated_price = round(simulated_price, 2)
        etiqueta = categorizar_precio(simulated_price, real_price)
        contador_etiquetas[etiqueta] += 1

        training_data.append({
            "Name": nombre,
            "SimulatedPrice": simulated_price,
            "RealPrice": real_price,
            "Type": row.get("Type", ""),
            "Connection": row.get("Connection", ""),
            "Switches": row.get("Switches", ""),
            "Rating": row.get("Rating", np.nan),
            "Stores": row.get("Stores", np.nan),
            "EtiquetaPrecio": etiqueta
        })

# 📊 Crear DataFrame final
train_df = pd.DataFrame(training_data)

# 💾 Guardar dataset para entrenamiento
train_df.to_csv(output_path, index=False)
print(f"\n✅ Dataset de entrenamiento multiclase generado con éxito en: {output_path}")
print(train_df.head())

# 📈 Mostrar conteo de etiquetas generadas
print("\n📊 Cantidad de etiquetas generadas:")
for etiqueta, cantidad in contador_etiquetas.items():
    print(f" - {etiqueta}: {cantidad} muestras")
