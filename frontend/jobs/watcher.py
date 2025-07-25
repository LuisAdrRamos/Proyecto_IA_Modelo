from pathlib import Path
import requests
import json

def watch_and_train(raw_dir: str, backend_url: str):
    """
    Escanea raw_dir buscando nuevos .csv y los entrena automáticamente.
    Para no re-entrenar siempre, se podría crear un archivo .trained o una BD/JSON.
    Para simplificar, este ejemplo se entrena siempre que vea el archivo.
    """
    p = Path(raw_dir)
    p.mkdir(parents=True, exist_ok=True)

    for csv_path in p.glob("*.csv"):
        try:
            with csv_path.open("rb") as f:
                data = {
                    "test_size": "0.2",
                    "random_state": "42",
                    "model_type": "rf",
                    "model_params": json.dumps({"n_estimators": 500, "max_depth": 15})
                }
                files = {"file": (csv_path.name, f, "text/csv")}
                r = requests.post(f"{backend_url}/train", data=data, files=files, timeout=None)
                r.raise_for_status()
                print(f"[watcher] Entrenado con {csv_path.name}: {r.json()}")
        except Exception as e:
            print(f"[watcher] Error entrenando {csv_path.name}: {e}")
