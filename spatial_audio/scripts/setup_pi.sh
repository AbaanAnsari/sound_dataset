#!/bin/bash

echo "================================"
echo "   SPATIAL AUDIO RPI 5 SETUP    "
echo "================================"

# 1. Detect OS and Model
MODEL=$(cat /sys/firmware/devicetree/base/model 2>/dev/null)
echo "Detected Model: $MODEL"
if [[ "$MODEL" != *"Raspberry Pi 5"* ]]; then
    echo "WARNING: This script is optimized for Raspberry Pi 5. You are running: $MODEL"
fi

# 2. Dependencies
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv libportaudio2 libasound2-dev git pinctrl arecord

# 3. Virtual Environment
echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Check ALSA & I2S Configuration
echo "Checking /boot/firmware/config.txt for I2S configuration..."
CONFIG_FILE="/boot/firmware/config.txt"
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="/boot/config.txt"
fi

if grep -q "^dtparam=i2s=on" "$CONFIG_FILE"; then
    echo "I2S appears to be enabled in $CONFIG_FILE."
else
    echo "I2S is NOT enabled in $CONFIG_FILE."
    echo "Backing up config and appending dtparam=i2s=on..."
    sudo cp $CONFIG_FILE ${CONFIG_FILE}.bak
    echo "dtparam=i2s=on" | sudo tee -a $CONFIG_FILE
    echo "A REBOOT will be required."
fi

# 5. Run Hardware Diagnostics
echo "Running Hardware Diagnostics..."
python3 scripts/hardware_diagnostic.py

echo "Setup script completed. If I2S was just enabled, please reboot."
