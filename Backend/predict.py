import importlib.util
import sys
import os
import joblib

# Ruta absoluta hacia test_model.py
test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test', 'test_model.py'))

# Cargar el módulo dinámicamente
spec = importlib.util.spec_from_file_location("test_model", test_path)
test_model = importlib.util.module_from_spec(spec)
sys.modules["test_model"] = test_model
spec.loader.exec_module(test_model)

# Importamos la función
predecir_categoria = test_model.predecir_categoria

# Función que usaremos desde la API
def predict_categoria(nombre_teclado, precio):
    resultado = predecir_categoria(nombre_teclado, precio)

    # Convertimos todos los valores a tipos nativos de Python
    resultado_limpio = {
        "nombre": str(resultado.get("Teclado", nombre_teclado)),
        "precio_ingresado": float(resultado.get("Precio ingresado", precio)),
        "precio_real_estimado": float(resultado.get("Precio real", 0)),
        "porcentaje": float(resultado.get("Porcentaje del real", 0)),
        "clasificacion": str(resultado.get("Categoría", "Desconocido"))
    }
    return resultado_limpio


# Ejemplo de uso
print(predict_categoria("Corsair K63 Wireless", 129.99))