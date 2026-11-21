"""Reference optical calibration utilities.

Inputs:
    sample: measured phototransistor readings
    blank: reference readings without absorbing sample
    dark: readings with illumination off

All arrays must contain six aligned wavelength channels.
"""

import numpy as np

WAVELENGTHS = [420, 460, 520, 570, 610, 630]


def calculate_absorbance(sample, blank, dark=None):
    sample = np.asarray(sample, dtype=float)
    blank = np.asarray(blank, dtype=float)

    if dark is None:
        dark = np.zeros_like(sample)
    else:
        dark = np.asarray(dark, dtype=float)

    if sample.shape != (6,) or blank.shape != (6,):
        raise ValueError("Six sample and blank readings are required.")

    if dark.shape != (6,):
        raise ValueError("Six dark readings are required.")

    corrected_sample = sample - dark
    corrected_blank = blank - dark

    if np.any(corrected_sample <= 0):
        raise ValueError("Sample intensity must exceed dark baseline.")

    if np.any(corrected_blank <= 0):
        raise ValueError("Blank intensity must exceed dark baseline.")

    return -np.log10(corrected_sample / corrected_blank)


def feature_dictionary(absorbance):
    return {
        f"abs_{wavelength}": float(value)
        for wavelength, value in zip(WAVELENGTHS, absorbance)
    }
