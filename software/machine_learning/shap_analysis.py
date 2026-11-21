"""Generate SHAP feature-importance visualization.

Usage:
    python shap_analysis.py path/to/measurements.csv
"""

import sys
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap

from data_preprocessing import load_dataset, FEATURES


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python shap_analysis.py path/to/measurements.csv"
        )

    bundle = joblib.load("outputs/glucose_rf.joblib")
    model = bundle["model"]

    df = load_dataset(sys.argv[1])
    X = df[FEATURES].sample(
        n=min(200, len(df)),
        random_state=42,
    )

    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(X)

    importance = np.abs(values).mean(axis=0)

    order = np.argsort(importance)

    plt.figure(figsize=(9, 5))
    plt.barh(
        np.array(FEATURES)[order],
        importance[order],
    )

    plt.xlabel("Mean absolute SHAP value")
    plt.title("Wavelength Feature Importance")
    plt.tight_layout()

    output = Path("outputs")
    output.mkdir(exist_ok=True)

    plt.savefig(
        output / "shap_importance.png",
        dpi=200,
    )

    plt.close()
    print("Saved outputs/shap_importance.png")


if __name__ == "__main__":
    main()
