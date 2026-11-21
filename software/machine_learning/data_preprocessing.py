"""Data validation and feature extraction.

The original dataset was not supplied.
Expected columns are documented in data/README.md.
"""

import pandas as pd

FEATURES = [
    "abs_420",
    "abs_460",
    "abs_520",
    "abs_570",
    "abs_610",
    "abs_630",
]

TARGET = "glucose_mg_dl"


def load_dataset(path):
    df = pd.read_csv(path)

    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in df]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()

    for column in required:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna().drop_duplicates()

    if len(df) < 10:
        raise ValueError("At least 10 valid rows are required.")

    return df


def get_features_target(df):
    return df[FEATURES], df[TARGET]
