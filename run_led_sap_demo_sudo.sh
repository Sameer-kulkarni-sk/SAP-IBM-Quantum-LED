#!/bin/bash
# Run LED SAP Demo with sudo for GPIO access
# This matches how the IBM demo runs with physical LEDs

cd /home/rasqberry

# Run with sudo for GPIO/NeoPixel access
sudo python3 /home/rasqberry/led_sap_demo.py