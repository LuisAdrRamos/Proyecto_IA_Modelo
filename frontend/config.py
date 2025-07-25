import os

# Puedes sobreescribir esto con un .env o variables de entorno del sistema
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Opcional (solo si quieres activar el watcher)
AUTO_WATCH = os.getenv("AUTO_WATCH", "false").lower() == "true"
DATA_RAW_DIR = os.getenv("DATA_RAW_DIR", "../data/raw")
WATCH_INTERVAL = int(os.getenv("WATCH_INTERVAL", "60"))  # segundos
