from flask import Flask, render_template, request, redirect, url_for
import requests
from services.api import BACKEND_URL, predict_price, predict_csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "precio": float(request.form.get("precio")),
            "Type": request.form.get("type"),
            "Connection": request.form.get("connection"),
            "Switches": request.form.get("switch")
        }
        try:
            response = requests.post(BACKEND_URL, json=data)
            resultado = response.json()
            return render_template("predict.html", resultado=resultado, datos=data)
        except Exception as e:
            return render_template("predict.html", error=str(e), datos=data)
    return render_template("predict.html", resultado=None, datos={})


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



if __name__ == '__main__':
    app.run(debug=True)
