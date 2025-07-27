import requests
import pandas as pd

# URL base del backend FastAPI
BACKEND_URL = "http://localhost:8000"

# 🔮 Función para predecir un solo teclado
def predict_price(data):
    try:
        # Importante: la ruta debe ser /predict
        response = requests.post(f"{BACKEND_URL}/predict", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Error del servidor de modelo", "status": response.status_code}
    except Exception as e:
        return {"error": str(e)}

# 📂 Función para predecir varios teclados desde un CSV
def predict_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        resultados = []
        for _, row in df.iterrows():
            try:
                data = {
                    'nombre': row['nombre'],
                    'precio': float(row['precio']),
                    'Type': row.get('Type', ''),
                    'Connection': row.get('Connection', ''),
                    'Switches': row.get('Switches', '')
                }
                pred = predict_price(data)
                resultados.append(pred)
            except Exception as e:
                resultados.append({"error": f"Fila con error: {str(e)}"})
        return resultados
    except Exception as e:
        return [{"error": f"Error al leer CSV: {str(e)}"}]
