#!/bin/bash
# Run LED SAP Demo Enhanced with hardware support
# This version supports both physical LEDs and GUI fallback

cd /home/rasqberry

# Check if running with sudo (needed for NeoPixel)
if [ "$EUID" -ne 0 ]; then
    # Try to run with sudo
    sudo -E DISPLAY=:0 python3 /home/rasqberry/led_sap_demo.py
else
    # Already running as root
    DISPLAY=:0 python3 /home/rasqberry/led_sap_demo.py
fi