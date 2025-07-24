import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

def preprocesar_datos(df):
    """
    Preprocesa el DataFrame para entrenamiento:
    - Escala columnas numéricas
    - Codifica columnas categóricas
    - Codifica la etiqueta objetivo
    """
    # --- Variables numéricas ---
    num_cols = ["SimulatedPrice", "Rating", "Stores"]
    df[num_cols] = df[num_cols].fillna(0)
    X_num = StandardScaler().fit_transform(df[num_cols])
    scaler = StandardScaler()
    X_num = scaler.fit_transform(df[num_cols])

    # --- Variables categóricas ---
    cat_cols = ["Name", "Type", "Connection", "Switches"]
    df[cat_cols] = df[cat_cols].fillna("Desconocido")
    encoder_cat = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_cat = encoder_cat.fit_transform(df[cat_cols])

    # --- Etiquetas ---
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["EtiquetaPrecio"])

    # --- Concatenación final ---
    X = np.hstack([X_num, X_cat])

    return X, y, encoder_cat, label_encoder, scaler
