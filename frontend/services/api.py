import json
import requests

def get_status(backend_url: str):
    resp = requests.get(f"{backend_url}/")
    resp.raise_for_status()
    return resp.json()

def send_csv_to_train(
    backend_url: str,
    csv_file,
    test_size: str,
    random_state: str,
    model_type: str,
    model_params_raw: str
):
    # model_params_raw es un string JSON enviado desde el formulario
    # el backend (FastAPI) acepta str para form-data.
    data = {
        "test_size": test_size,
        "random_state": random_state,
        "model_type": model_type,
        "model_params": model_params_raw
    }
    files = {
        "file": (csv_file.filename, csv_file.stream, "text/csv")
    }
    resp = requests.post(f"{backend_url}/train", data=data, files=files)
    resp.raise_for_status()
    return resp.json()

def predict_from_texts(backend_url: str, texts: list[str]):
    payload = {"texts": texts}
    resp = requests.post(f"{backend_url}/predict", json=payload)
    resp.raise_for_status()
    return resp.json()
