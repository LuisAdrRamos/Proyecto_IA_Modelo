import importlib.util
import sys
import os
import joblib
import pandas as pd
import traceback
import math

# --- 🔧 Cargar test_model.py dinámicamente ---
test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test', 'test_model.py'))
spec = importlib.util.spec_from_file_location("test_model", test_path)
test_model = importlib.util.module_from_spec(spec)
sys.modules["test_model"] = test_model
spec.loader.exec_module(test_model)

predecir_categoria = test_model.predecir_categoria

# --- 📄 Cargar dataset base para info adicional ---
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
try:
    df_info = pd.read_csv(os.path.join(base_path, 'data', 'teclados_limpio_sinMembrana.csv'))
    df_info.fillna("", inplace=True)
except Exception as e:
    print(f"❌ Error cargando CSV de info adicional: {e}")
    df_info = pd.DataFrame()

# --- ✅ Función para limpiar valores numéricos ---
def limpiar_valor(valor, default=0.0):
    try:
        num = float(valor)
        return num if math.isfinite(num) else default
    except:
        return default

# --- 🚀 Función principal que usa el backend ---
def predict_categoria(nombre_teclado, precio):
    try:
        resultado = predecir_categoria(nombre_teclado, precio)

        if isinstance(resultado, str) or "error" in resultado:
            return {"error": f"No se pudo predecir '{nombre_teclado}'"}

        info_fila = df_info[df_info["Name"] == nombre_teclado].iloc[0] if not df_info.empty and nombre_teclado in df_info["Name"].values else {}

        resultado_limpio = {
            "nombre": str(resultado.get("Teclado", nombre_teclado)),
            "precio_ingresado": limpiar_valor(resultado.get("Precio ingresado", precio)),
            "precio_real_estimado": limpiar_valor(resultado.get("Precio real", 0)),
            "porcentaje": round(limpiar_valor(resultado.get("Porcentaje del real", 0)), 2),
            "clasificacion": str(resultado.get("Categoría", "Desconocido")),
            "Type": info_fila.get("Type", "Desconocido") if isinstance(info_fila, pd.Series) else "Desconocido",
            "Connection": info_fila.get("Connection", "Desconocido") if isinstance(info_fila, pd.Series) else "Desconocido",
            "Switches": info_fila.get("Switches", "Desconocido") if isinstance(info_fila, pd.Series) else "Desconocido"
        }

        return resultado_limpio

    except Exception as e:
        print("❌ Error durante la predicción:")
        traceback.print_exc()
        return {"error": f"Error interno al predecir '{nombre_teclado}'"}
