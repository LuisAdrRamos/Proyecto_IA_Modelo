import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from utils.preprocesar import preprocesar_datos  # ✅ Import corregido

def reentrenar_modelo(csv_path):
    df = pd.read_csv(csv_path)
    X, y, encoder_cat, encoder_labels, scaler = preprocesar_datos(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=3000, random_state=42)
    model.fit(X_train, y_train)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))

    joblib.dump(model, os.path.join(base_path, "modelo_multiclase_v3.pkl"))
    joblib.dump(encoder_cat, os.path.join(base_path, "encoder_categoricos.pkl"))
    joblib.dump(encoder_labels, os.path.join(base_path, "encoder_etiquetas.pkl"))
    joblib.dump(scaler, os.path.join(base_path, "scaler_full.pkl"))

    return "Modelo reentrenado correctamente."
