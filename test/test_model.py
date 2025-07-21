import pandas as pd
import numpy as np
import joblib
import json

print("🔄 Cargando archivos del modelo...")

try:
    modelo = joblib.load('model/modelo_multiclase_v3.pkl')
    scaler = joblib.load('model/scaler_full_v2.pkl')
    cat_encoder = joblib.load('model/encoder_categoricos_v2.pkl')
    label_encoder = joblib.load('model/encoder_etiquetas_v2.pkl')
except FileNotFoundError as e:
    print(f"❌ Archivo no encontrado: {e}")
    exit()
except Exception as e:
    print(f"❌ Error cargando modelos: {e}")
    exit()

# Cargar CSV
try:
    df_base = pd.read_csv('data/teclados_limpio_sinMembrana.csv')
    df_base.fillna(0, inplace=True)
except Exception as e:
    print(f"❌ Error cargando el dataset base: {e}")
    exit()

def predecir_categoria(teclado_nombre, precio_usuario):
    fila = df_base[df_base["Name"] == teclado_nombre]
    if fila.empty:
        return f"❌ Teclado '{teclado_nombre}' no encontrado."

    fila = fila.iloc[0]
    tipo = fila.get("Type", "")
    conexion = fila.get("Connection", "")
    switches = fila.get("Switches", "")
    rating = fila.get("Rating", 0)
    stores = fila.get("Stores", 0)

    # Escalar numéricos con nombres
    num_df = pd.DataFrame([[precio_usuario, rating, stores]], columns=["SimulatedPrice", "Rating", "Stores"])
    num_features = scaler.transform(num_df)

    # Codificar categóricos con nombres
    cat_df = pd.DataFrame([[teclado_nombre, tipo, conexion, switches]], 
                        columns=["Name", "Type", "Connection", "Switches"])
    cat_features = cat_encoder.transform(cat_df)

    # Concatenar
    X_input = np.hstack([num_features, cat_features])

    # Predecir
    y_pred = modelo.predict(X_input)
    etiqueta = label_encoder.inverse_transform(y_pred)[0]

    # Construir resultado
    resultado = {
        "Teclado": teclado_nombre,
        "Precio ingresado": round(precio_usuario, 2),
        "Precio real": round(fila["Price"], 2),
        "Porcentaje del real": round((precio_usuario / fila["Price"]) * 100, 2),
        "Categoría": etiqueta
    }

    # 🧾 Imprimir bonito
    print("\n🧾 Resultado de la evaluación:\n")
    print(f"🖥️  Teclado            : {resultado['Teclado']}")
    print(f"💵 Precio ingresado   : ${resultado['Precio ingresado']}")
    print(f"🏷️  Precio real        : ${resultado['Precio real']}")
    print(f"📈 Porcentaje del real: {resultado['Porcentaje del real']}%")
    print(f"📊 Categoría           : {resultado['Categoría']}")

    return resultado

# 🔍 Ejecutar prueba
if __name__ == "__main__":
    resultado = predecir_categoria("Corsair K63 Wireless", 129.99)
    print("\n📦 Resultado en formato JSON:\n")
    print(json.dumps(resultado, indent=4))