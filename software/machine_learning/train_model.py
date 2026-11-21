"""Train a reference Random Forest regression model.

Configuration follows the source report:
150 estimators, maximum depth 8, approximate 80/20 split.

The original report's MixUp and noise augmentation
are not reproduced here because the exact procedure,
parameters, and split order were not provided.

Usage:
    python train_model.py path/to/measurements.csv
"""

import json
import sys
from pathlib import Path

import joblib
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, KFold, cross_val_score

from data_preprocessing import load_dataset, get_features_target, FEATURES


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python train_model.py path/to/measurements.csv"
        )

    dataset_path = Path(sys.argv[1])

    if not dataset_path.is_file():
        raise FileNotFoundError(dataset_path)

    df = load_dataset(dataset_path)
    X, y = get_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results = {
        "test_r2": float(r2_score(y_test, predictions)),
        "test_rmse": float(
            np.sqrt(mean_squared_error(y_test, predictions))
        ),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
    }

    # Cross-validation uses only training data.
    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    cv_scores = cross_val_score(
        RandomForestRegressor(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            n_jobs=-1,
        ),
        X_train,
        y_train,
        cv=cv,
        scoring="r2",
    )

    results["train_cv_r2_mean"] = float(cv_scores.mean())
    results["train_cv_r2_std"] = float(cv_scores.std())

    output = Path("outputs")
    output.mkdir(exist_ok=True)

    joblib.dump(
        {"model": model, "features": FEATURES},
        output / "glucose_rf.joblib",
    )

    (output / "metrics.json").write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(results, indent=2))
    print("Model saved to outputs/glucose_rf.joblib")


if __name__ == "__main__":
    main()
