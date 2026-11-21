import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "software" / "backend"))

from app import Handler, predict, next_simulated_sample

class IntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), Handler
        )
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get_json(self, endpoint):
        with urlopen(
            f"http://127.0.0.1:{self.port}{endpoint}",
            timeout=5
        ) as response:
            return json.load(response)

    def test_health(self):
        result = self.get_json("/api/health")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["model_loaded"])

    def test_simulated_sensor(self):
        result = self.get_json("/api/sample")
        self.assertEqual(len(result["absorbance"]), 6)
        self.assertEqual(result["source"], "synthetic_simulator")
        self.assertFalse(result["clinical_use"])

    def test_prediction_endpoint(self):
        sample = next_simulated_sample()
        payload = json.dumps({
            "absorbance": sample["absorbance"]
        }).encode()

        request = Request(
            f"http://127.0.0.1:{self.port}/api/predict",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urlopen(request, timeout=5) as response:
            result = json.load(response)

        self.assertAlmostEqual(
            result["prediction_mg_dl"],
            predict(sample["absorbance"]),
            places=6
        )

    def test_homepage(self):
        with urlopen(
            f"http://127.0.0.1:{self.port}/",
            timeout=5
        ) as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"<html", response.read().lower())

if __name__ == "__main__":
    unittest.main(verbosity=2)
