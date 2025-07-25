import requests

class BackendClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def train_model(self, file, payload):
        files = {"file": file}
        res = requests.post(f"{self.base_url}/train", data=payload, files=files)
        res.raise_for_status()
        return res.json()

    def predict_text(self, textos: list):
        res = requests.post(f"{self.base_url}/predict", json={"texts": textos})
        res.raise_for_status()
        return res.json()

    def ping(self):
        return requests.get(f"{self.base_url}/").json()
