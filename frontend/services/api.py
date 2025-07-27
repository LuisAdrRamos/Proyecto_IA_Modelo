import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000/predict"

def predict_price(data):
    try:
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Error del servidor de modelo", "status": response.status_code}
    except Exception as e:
        return {"error": str(e)}

def predict_csv(csv_path):
    df = pd.read_csv(csv_path)
    resultados = []
    for _, row in df.iterrows():
        try:
            data = {
                'nombre': row['nombre'],
                'precio': float(row['precio'])
            }
            pred = predict_price(data)
            resultados.append(pred)
        except Exception as e:
            resultados.append({"error": f"Fila con error: {str(e)}"})
    return resultados
