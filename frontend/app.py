from flask import Flask, render_template, request, redirect, url_for
from services.api import predict_price, predict_csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'precio': float(request.form['precio'])
        }
        resultado = predict_price(data)
        return render_template('result.html', resultado=resultado)
    return render_template('predict.html')

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
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
