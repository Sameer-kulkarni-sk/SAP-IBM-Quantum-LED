#!/bin/bash
# Test script for SAP LED Demo Enhanced
# Run this on the Rasqberry device

echo "=========================================="
echo "SAP LED Demo - Test Script"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Warning: Not running on Raspberry Pi"
else
    echo "✓ Running on: $(cat /proc/device-tree/model)"
fi
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Check required libraries
echo "Checking required libraries..."
echo -n "  - board/neopixel: "
python3 -c "import board, neopixel; print('✓ Installed')" 2>/dev/null || echo "✗ Not installed"

echo -n "  - sense_hat: "
python3 -c "from sense_hat import SenseHat; print('✓ Installed')" 2>/dev/null || echo "✗ Not installed"

echo -n "  - RPi.GPIO: "
python3 -c "import RPi.GPIO; print('✓ Installed')" 2>/dev/null || echo "✗ Not installed"

echo -n "  - rq_led_utils: "
python3 -c "import sys; sys.path.insert(0, '/usr/bin'); from rq_led_utils import get_led_config; print('✓ Installed')" 2>/dev/null || echo "✗ Not installed"
echo ""

# Check file permissions
echo "Checking file permissions..."
if [ -x "/home/rasqberry/led_sap_demo.py" ]; then
    echo "✓ led_sap_demo.py is executable"
else
    echo "✗ led_sap_demo.py is not executable"
    echo "  Run: chmod +x /home/rasqberry/led_sap_demo.py"
fi
echo ""

# Check GPIO permissions
echo "Checking GPIO permissions..."
if groups | grep -q gpio; then
    echo "✓ User is in gpio group"
else
    echo "✗ User is not in gpio group"
    echo "  Run: sudo usermod -a -G gpio $USER"
    echo "  Then logout and login again"
fi
echo ""

# List available demo files
echo "Available demo files:"
ls -lh /home/rasqberry/led_sap_demo*.py 2>/dev/null
echo ""

# Offer to run the demo
echo "=========================================="
echo "Ready to test!"
echo "=========================================="
echo ""
echo "To run the enhanced SAP LED demo:"
echo "  python3 /home/rasqberry/led_sap_demo.py"
echo ""
echo "Or simply:"
echo "  ./led_sap_demo.py"
echo ""
echo "Controls:"
echo "  - Joystick UP (or GPIO17): Rainbow mode"
echo "  - Joystick DOWN (or GPIO27): Blink mode"
echo "  - Joystick LEFT/RIGHT (or GPIO22): SAP X IBM mode"
echo "  - Joystick CENTER (or GPIO23): Exit"
echo "  - Ctrl+C: Force exit"
echo ""
echo "=========================================="
echo ""

read -p "Would you like to run the demo now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting SAP LED Demo..."
    echo ""
    python3 /home/rasqberry/led_sap_demo.py
fi