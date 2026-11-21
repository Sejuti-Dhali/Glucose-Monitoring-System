# AI-Driven Glucose Monitoring System

A biomedical engineering project investigating
glucose concentration estimation using optical
sensing and machine learning.

## Project Overview

The documented experimental system combines:

- Six-wavelength optical acquisition
- Arduino UNO
- LED and phototransistor arrays
- HC-05 Bluetooth communication
- Random Forest regression
- SHAP feature interpretation
- OpTose Android application

## Wavelengths

420, 460, 520, 570, 610, and 630 nm.

## Machine Learning

The source report describes a Random Forest
regressor with:

- 150 estimators
- Maximum depth 8
- Approximately 80/20 train/test split
- Five-fold cross-validation
- MixUp and Gaussian-noise augmentation

The new reference training script implements
the documented Random Forest configuration,
but does not reproduce the unspecified
augmentation procedure.

## Reported Results

| Metric | Reported value |
|---|---:|
| Test R-squared | 0.960 |
| RMSE | 12.511 |
| Five-fold CV R-squared | 0.928 |

These numbers are taken from the project report.
They are not outputs from the newly written code.

The report identifies 520 nm as an influential
wavelength in its feature-importance and SHAP
analyses.

## Repository Structure

```text
Glucose-Monitoring-System/
  README.md
  index.html
  hardware/
    README.md
  data/
    README.md
  docs/
    provenance.md
  software/
    arduino/
      glucose_sensor.ino
    machine_learning/
      requirements.txt
      sensor_calibration.py
      data_preprocessing.py
      train_model.py
      shap_analysis.py
      predict.py
    android/
      MainActivity.kt
      activity_main.xml
```

## Run the Python Reference Pipeline

```powershell
cd software/machine_learning

python -m pip install -r requirements.txt

python train_model.py path/to/measurements.csv

python shap_analysis.py path/to/measurements.csv

python predict.py 0.1 0.2 0.3 0.4 0.5 0.6
```

The prediction example is a syntax demonstration,
not a clinically meaningful input.

Training requires a real dataset with the
documented column names.

## Hardware Status

The Arduino firmware is a newly developed
reference implementation. Proposed pin
assignments require physical verification.

## Android Status

The Kotlin/XML files illustrate a basic
interface. They do not constitute a complete
buildable Android Studio application.

## Provenance

The underlying experimental methodology and
reported findings originate from the supplied
May 2026 BME 4232 group project report.

The source code in this repository is a newly
written reference reconstruction, not the
original source code from the report.

Repository ownership does not imply sole
authorship of the underlying group project.

## Limitations

- Original experimental dataset unavailable
- Original firmware and Android source unavailable
- Reported results not independently reproduced
- Proposed pin mapping not hardware-verified
- No independent clinical validation

**Not intended for diagnosis, insulin dosing,
or other medical decisions.**
