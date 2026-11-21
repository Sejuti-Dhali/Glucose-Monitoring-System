# Data

The original experimental dataset was not supplied.

## Expected CSV format

The reference Python implementation expects:

- abs_420
- abs_460
- abs_520
- abs_570
- abs_610
- abs_630
- glucose_mg_dl

These columns are a new standardized interface,
not a claim about the original dataset schema.

No experimental measurements are fabricated.

## Calibration

Convert raw optical readings to absorbance using
a blank reference and, when available, a dark
baseline measurement.

The source report describes prepared glucose
solutions with GOD-POD reagent.

## Data Leakage

Repeated measurements from the same prepared
sample should be grouped during validation.
The current reference training script uses
a random row-level split and should be adapted
when sample-group identifiers are available.
