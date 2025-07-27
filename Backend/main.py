from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # ✅ Esto faltaba
import pandas as pd  # ✅ Esto también faltaba
import os
import shutil
from pydantic import BaseModel  # 👈 Esto es nuevo


from Backend.predict import predict_categoria
from Backend.train import reentrenar_modelo
from Backend.metrics import obtener_metricas
class EntradaPrediccion(BaseModel):
    teclado: str
    precio: float


# 🌐 Inicializar FastAPI
app = FastAPI()

# 🛡️ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitarlo a ["http://localhost:3000"] si lo sabes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📥 Obtener lista de teclados para dropdown en frontend
@app.get("/teclados")
def obtener_teclados():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base_path, 'data', 'teclados_limpio_sinMembrana.csv')

    try:
        df = pd.read_csv(data_path)
        nombres_teclados = sorted(df["Name"].dropna().unique().tolist())
        return JSONResponse(content=nombres_teclados)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 🏠 Ruta base
@app.get("/")
def root():
    return {"mensaje": "API de clasificación de teclados operativa"}

# 🧠 Predicción
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        resultado = predict_categoria(data["nombre"], data["precio"])
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# 🧪 Reentrenar modelo
@app.post("/train")
async def train(csv: UploadFile = File(...)):
    ruta_destino = f"data/{csv.filename}"
    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(csv.file, buffer)
    return reentrenar_modelo(ruta_destino)

# 📊 Métricas del modelo
@app.get("/metrics")
def metrics():
    return obtener_metricas()
