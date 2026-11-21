/*
  Glucose Optical Sensor - Reference Firmware

  Reconstructed from the documented six-channel
  optical acquisition methodology.

  IMPORTANT:
  - Pin assignments below are proposed, not verified.
  - Check actual wiring and electrical limits.
  - Not a clinical glucose-monitoring device.
*/

const byte NUM_CHANNELS = 6;

const byte ledPins[NUM_CHANNELS] = {
  2, 3, 4, 5, 6, 7
};

const byte sensorPins[NUM_CHANNELS] = {
  A0, A1, A2, A3, A4, A5
};

const int wavelengths[NUM_CHANNELS] = {
  420, 460, 520, 570, 610, 630
};

const byte SAMPLES_PER_CHANNEL = 20;

float readChannel(byte channel) {
  long total = 0;

  for (byte i = 0; i < NUM_CHANNELS; i++) {
    digitalWrite(ledPins[i], LOW);
  }

  delay(20);

  digitalWrite(ledPins[channel], HIGH);
  delay(100);

  for (byte sample = 0; sample < SAMPLES_PER_CHANNEL; sample++) {
    total += analogRead(sensorPins[channel]);
    delay(5);
  }

  digitalWrite(ledPins[channel], LOW);

  return float(total) / SAMPLES_PER_CHANNEL;
}

void setup() {
  Serial.begin(9600);

  for (byte i = 0; i < NUM_CHANNELS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  Serial.println(
    "raw_420,raw_460,raw_520,raw_570,raw_610,raw_630"
  );
}

void loop() {
  for (byte channel = 0; channel < NUM_CHANNELS; channel++) {
    float reading = readChannel(channel);

    Serial.print(reading, 2);

    if (channel < NUM_CHANNELS - 1) {
      Serial.print(",");
    }
  }

  Serial.println();
  delay(1000);
}
