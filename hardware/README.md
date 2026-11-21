# Hardware Reference Configuration

## Documented components

- Arduino UNO
- Six visible-wavelength LEDs
- Six phototransistors
- HC-05 Bluetooth module
- Optical sample holder
- Light-shielded enclosure
- 100-ohm LED resistors
- 10-kilohm phototransistor resistors

## Wavelengths

| Channel | Wavelength |
|---|---:|
| Violet | 420 nm |
| Blue | 460 nm |
| Green | 520 nm |
| Yellow | 570 nm |
| Orange | 610 nm |
| Red | 630 nm |

## Proposed firmware pin configuration

| Channel | LED pin | Sensor pin |
|---|---|---|
| 420 nm | D2 | A0 |
| 460 nm | D3 | A1 |
| 520 nm | D4 | A2 |
| 570 nm | D5 | A3 |
| 610 nm | D6 | A4 |
| 630 nm | D7 | A5 |

**Important:** This pin mapping is proposed for the
new reference firmware. It is not verified against
the original hardware.

The firmware transmits six raw ADC readings over
serial. The report also describes HC-05 Bluetooth;
however, complete Bluetooth application integration
has not been reconstructed.

Electrical wiring, resistor values, sensor response,
and supply requirements must be verified before use.
