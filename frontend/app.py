from flask import Flask, render_template, request
from services.api import (
    get_status,
    send_csv_to_train,
    predict_from_texts
)
from config import BACKEND_URL, AUTO_WATCH, DATA_RAW_DIR, WATCH_INTERVAL

# Opcional: scheduler para el watcher
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.watcher import watch_and_train

app = Flask(__name__, template_folder="templates", static_folder="static")

# ------- Watcher opcional --------
scheduler = None
if AUTO_WATCH:
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(watch_and_train, "interval", seconds=WATCH_INTERVAL, args=[DATA_RAW_DIR, BACKEND_URL])
    scheduler.start()
# ---------------------------------

@app.route("/")
def index():
    status = {}
    try:
        status = get_status(BACKEND_URL)
    except Exception as e:
        status = {"error": str(e)}
    return render_template("index.html", status=status)

@app.route("/train", methods=["GET", "POST"])
def train():
    if request.method == "GET":
        return render_template("train.html")

    # POST
    file = request.files.get("file")
    if not file:
        return "Debes subir un CSV", 400

    test_size = request.form.get("test_size", "0.2")
    random_state = request.form.get("random_state", "42")
    model_type = request.form.get("model_type", "logreg")
    model_params_raw = request.form.get("model_params", "{}")  # JSON string

    result = send_csv_to_train(
        backend_url=BACKEND_URL,
        csv_file=file,
        test_size=test_size,
        random_state=random_state,
        model_type=model_type,
        model_params_raw=model_params_raw
    )

    # Si la llamada viene de HTMX devuelvo solo el parcial
    if request.headers.get("HX-Request"):
        return render_template("partials/train_result.html", result=result)

    # Si no, devuelvo la página completa
    return render_template("train.html", result=result)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    text_block = request.form.get("texts", "")
    texts = [t.strip() for t in text_block.split("\n") if t.strip()]

    result = predict_from_texts(BACKEND_URL, texts)

    if request.headers.get("HX-Request"):
        return render_template("partials/predict_result.html", texts=texts, result=result)

    return render_template("predict.html", texts=texts, result=result)

@app.route("/runs")
def runs():
    # Consumo de un endpoint /runs o /metrics/latest de tu backend
    runs_list = []
    return render_template("runs.html", runs=runs_list)

if __name__ == "__main__":
    app.run(port=9000, debug=True)
