"""Predict glucose concentration from six absorbance features.

Usage:
    python predict.py 0.1 0.2 0.3 0.4 0.5 0.6

The example values above demonstrate command syntax only.
They are not experimental observations.
"""

import sys

import joblib
import pandas as pd


def main():
    if len(sys.argv) != 7:
        raise SystemExit(
            "Provide six absorbance values in wavelength order."
        )

    bundle = joblib.load("outputs/glucose_rf.joblib")
    features = bundle["features"]
    model = bundle["model"]

    values = [float(value) for value in sys.argv[1:]]

    X = pd.DataFrame([values], columns=features)
    prediction = model.predict(X)[0]

    print(f"Estimated glucose: {prediction:.2f} mg/dL")
    print("Research estimate only; not for clinical use.")


if __name__ == "__main__":
    main()
