# End-to-End Software Demonstration

## Architecture

Synthetic optical dataset
-> six absorbance features
-> local Python HTTP API
-> trained Random Forest
-> mobile-responsive browser interface

## Supported capabilities

- Reproducible synthetic dataset generation
- Random Forest training and evaluation
- Simulated sensor streaming
- HTTP prediction endpoint
- Browser-based result display
- Automated integration tests
- Static research results gallery

## Local execution

Run:

    .\.venv\Scripts\python.exe software\backend\app.py

Open:

    http://127.0.0.1:8765

API endpoints:

- GET /api/health
- GET /api/sample
- POST /api/predict

POST /api/predict expects JSON:

    {"absorbance":[0.1,0.2,0.3,0.4,0.5,0.6]}

## Deployment limitations

GitHub Pages hosts static files only.
The live prediction API runs locally and is
not deployed to GitHub Pages.

## Hardware limitations

No physical Arduino, HC-05 Bluetooth link,
LED/phototransistor circuit, or Android APK
has been verified by this implementation.

## Scientific limitations

All software demonstration data are synthetic.

The original report's numerical results are
reported findings, not independently reproduced
results.

The fitted-model scatter and residual figures
include training observations and therefore
must not be presented as held-out performance.

This system is not suitable for medical diagnosis,
treatment, or insulin dosing.
