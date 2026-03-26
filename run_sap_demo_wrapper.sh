#!/bin/bash
# Wrapper script to run SAP LED demo and keep terminal open

echo "=========================================="
echo "SAP LED Demo - Starting..."
echo "=========================================="
echo ""

# Run the demo with sudo
sudo python3 /home/rasqberry/led_sap_demo.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "Demo exited successfully"
else
    echo "Demo exited with error code: $EXIT_CODE"
fi
echo "=========================================="
echo ""
echo "Press Enter to close this window..."
read