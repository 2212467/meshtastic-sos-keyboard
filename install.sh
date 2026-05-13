#!/bin/bash

echo "Updating system..."
sudo apt update

echo "Installing dependencies..."
sudo apt install -y python3-pip

echo "Installing Python packages..."
pip3 install -r requirements.txt

echo "Installing systemd service..."
sudo cp systemd/sos_keyboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sos_keyboard

echo "Done!"