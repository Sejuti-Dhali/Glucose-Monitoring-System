"""Generate synthetic data for software demonstration only.

NOT original experimental data.
NOT clinical data.
NOT suitable for validating glucose-monitoring accuracy.
"""

from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 300
glucose = rng.uniform(50, 250, size=n)

wavelengths = [420, 460, 520, 570, 610, 630]

# Arbitrary demonstration coefficients.
# These are not experimentally calibrated.
coefficients = [0.0007, 0.0010, 0.0017, 0.0012, 0.0008, 0.0006]

data = {}

for wavelength, coefficient in zip(wavelengths, coefficients):
    absorbance = (
        0.08
        + coefficient * glucose
        + rng.normal(0, 0.015, size=n)
    )
    data[f"abs_{wavelength}"] = absorbance

data["glucose_mg_dl"] = glucose

df = pd.DataFrame(data)

output = Path("data/synthetic_glucose_demo.csv")
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)

print(f"Created {output} with {len(df)} synthetic rows.")
print(df.head())
