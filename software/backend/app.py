"""Local HTTP API for simulated optical glucose monitoring.

This application does NOT communicate with physical hardware.
It is not intended for clinical use.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import mimetypes
import threading
import time

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ML = ROOT / "software" / "machine_learning"
DATA = ROOT / "data" / "synthetic_glucose_demo.csv"
MODEL = ML / "outputs" / "glucose_rf.joblib"

bundle = joblib.load(MODEL)
model = bundle["model"]
features = bundle["features"]

df = pd.read_csv(DATA)
cursor = 0
lock = threading.Lock()

def predict(values):
    if not isinstance(values, list) or len(values) != 6:
        raise ValueError("Exactly six absorbance values required.")

    numbers = [float(v) for v in values]

    import math
    if not all(math.isfinite(v) for v in numbers):
        raise ValueError("All values must be finite.")

    row = pd.DataFrame([numbers], columns=features)
    return float(model.predict(row)[0])

def next_simulated_sample():
    global cursor

    with lock:
        row = df.iloc[cursor % len(df)]
        cursor += 1

    values = [float(row[name]) for name in features]

    return {
        "source": "synthetic_simulator",
        "wavelengths_nm": [420,460,520,570,610,630],
        "absorbance": values,
        "reference_mg_dl": float(row["glucose_mg_dl"]),
        "prediction_mg_dl": predict(values),
        "timestamp_ms": int(time.time() * 1000),
        "clinical_use": False
    }

class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/health":
            return self.send_json({
                "status": "ok",
                "mode": "simulation",
                "model_loaded": True
            })

        if path == "/api/sample":
            return self.send_json(next_simulated_sample())

        if path == "/":
            path = "/index.html"

        # Only serve selected public assets.
        allowed = (
            path in (
                "/index.html",
                "/overview.html",
                "/architecture.html",
                "/sensing.html",
                "/results.html",
                "/prototype.html",
                "/style.css",
                "/media/glucose-hardware-cover.png",
            )
            or path.startswith("/media/results/")
        )
            or (path.startswith("/media/results/") or path == "/media/glucose-hero.png")
        )

        if not allowed:
            return self.send_json({"error": "Not found"}, 404)

        file_path = (ROOT / path.lstrip("/")).resolve()

        if not file_path.is_relative_to(ROOT.resolve()):
            return self.send_json({"error": "Invalid path"}, 403)

        if not file_path.is_file():
            return self.send_json({"error": "Not found"}, 404)

        payload = file_path.read_bytes()
        mime = mimetypes.guess_type(str(file_path))[0]
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        if urlparse(self.path).path != "/api/predict":
            return self.send_json({"error": "Not found"}, 404)

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > 10000:
                raise ValueError("Invalid request size.")

            body = json.loads(self.rfile.read(size))
            result = predict(body["absorbance"])

            return self.send_json({
                "prediction_mg_dl": result,
                "mode": "demonstration",
                "clinical_use": False
            })

        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            return self.send_json({"error": str(exc)}, 400)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("Local demo: http://127.0.0.1:8765", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()




