# 4-Microphone Spatial Audio for Raspberry Pi 5

Production-quality synchronized spatial audio system utilizing four INMP441 digital I²S microphones.

## Hardware Requirements
- Raspberry Pi 5
- Raspberry Pi OS
- 4x INMP441 Microphones

## Pinout
| Signal   | Raspberry Pi GPIO | Physical Pin | MIC1 | MIC2 | MIC3 | MIC4 |
| -------- | ----------------: | -----------: | ---- | ---- | ---- | ---- |
| 3.3 V    |                 — |      1 or 17 | VDD  | VDD  | VDD  | VDD  |
| GND      |                 — |    6/9/14/20 | GND  | GND  | GND  | GND  |
| BCLK/SCK |            GPIO18 |           12 | SCK  | SCK  | SCK  | SCK  |
| WS/LRCLK |            GPIO19 |           35 | WS   | WS   | WS   | WS   |
| SD1      |            GPIO20 |           38 | SD   | —    | —    | —    |
| SD2      |            GPIO22 |           15 | —    | SD   | —    | —    |
| SD3      |            GPIO24 |           18 | —    | —    | SD   | —    |
| SD4      |            GPIO26 |           37 | —    | —    | —    | SD   |

## Installation

```bash
git clone <repository>
cd spatial_audio

bash scripts/setup_pi.sh
```

## Running Diagnostics
After installing dependencies and rebooting (if I2S was enabled), run:
```bash
python3 scripts/hardware_diagnostic.py
```
This is **Phase 1**. Do not proceed until hardware diagnostic passes and I2S hardware is properly exposed as a 4-channel device via ALSA.
