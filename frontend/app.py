from flask import Flask, render_template, request
import requests
import pandas as pd
import os
from services.api import BACKEND_URL, predict_csv
from services.api import predict_price
import math
from flask import Flask

# --- Configuración de Flask ---
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Ruta absoluta al CSV de teclados ---
TECLADOS_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'teclados_limpio_sinMembrana.csv'))

# --- Función para cargar teclados desde el CSV ---
def cargar_teclados_desde_csv():
    try:
        df = pd.read_csv(TECLADOS_CSV)
        df = df[["Name", "Type", "Connection", "Switches", "Price"]].dropna()

        teclados = []
        for _, row in df.iterrows():
            teclado = {
                "nombre": row["Name"],
                "type": row["Type"],
                "connection": row["Connection"],
                "switches": row["Switches"]
            }
            teclados.append(teclado)

        # Eliminar duplicados por nombre
        teclados_unicos = {t["nombre"]: t for t in teclados}
        return list(teclados_unicos.values())
    except Exception as e:
        print(f"❌ Error al cargar teclados: {e}")
        return []

# --- Página de inicio ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Página de predicción ---
@app.route("/predict", methods=["GET", "POST"])
def predict():
    teclados = cargar_teclados_desde_csv()

    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "precio": float(request.form.get("precio")),
            "Type": request.form.get("type"),
            "Connection": request.form.get("connection"),
            "Switches": request.form.get("switch")
        }

        try:
            response = requests.post(f"{BACKEND_URL}/predict", json=data)
            resultado = response.json()
            return render_template("predict.html", resultado=resultado, datos=data, teclados=teclados)
        except Exception as e:
            return render_template("predict.html", error=str(e), datos=data, teclados=teclados)

    return render_template("predict.html", resultado=None, datos={}, teclados=teclados)

# --- Carga de archivos CSV para predicciones múltiples ---
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['csv_file']
        if file.filename.endswith('.csv'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            resultados = predict_csv(path)
            return render_template('partials/predict_result.html', resultados=resultados)
        return "Archivo inválido. Solo se aceptan .csv"

    return render_template("upload.html", resultados=[])

@app.template_filter("moneda")
def moneda(valor):
    try:
        num = float(valor)
        return f"${round(num, 2)}" if math.isfinite(num) else "—"
    except:
        return "—"

# --- Iniciar app ---
if __name__ == '__main__':
    app.run(debug=True)
