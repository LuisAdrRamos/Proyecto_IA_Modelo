import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from sklearn.metrics import classification_report
import joblib
from utils.preprocesar import preprocesar_datos  

def obtener_metricas():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base_path, 'data', 'train_dataset.csv')
    model_path = os.path.join(base_path, 'model', 'modelo_multiclase_v3.pkl')

    df = pd.read_csv(data_path)
    X, y, encoder_cat, encoder_labels, scaler = preprocesar_datos(df)

    model = joblib.load(model_path)
    y_pred = model.predict(X)

    report = classification_report(y, y_pred, output_dict=True)
    return report
