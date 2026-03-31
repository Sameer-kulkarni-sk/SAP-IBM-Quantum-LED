#!/bin/bash
################################################################################
# rq_led_sap_demo.sh - RasQberry LED SAP Demo Launcher
#
# Description:
#   Launches the SAP LED demo with joystick controls.
#   Displays SAP logo with interactive color changes.
#
# Usage:
#   sudo /usr/bin/rq_led_sap_demo.sh
#
# Requirements:
#   - Must be run as root (for LED control)
#   - RasQberry-Two virtual environment
#   - led_sap_demo.py in user home directory
#
# Author: SAP-IBM Quantum LED Demo Project
# License: Apache 2.0
################################################################################

set -e  # Exit on error

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run as root (use sudo)"
    exit 1
fi

# Configuration - can be overridden by environment variables
readonly RASQBERRY_USER="${RASQBERRY_USER:-rasqberry}"
readonly USER_HOME="/home/${RASQBERRY_USER}"
readonly VENV_PATH="${USER_HOME}/RasQberry-Two/venv/RQB2"
readonly LED_SCRIPT="${USER_HOME}/led_sap_demo.py"
readonly BIN_DIR="/usr/bin"

# Check if demo script exists
if [ ! -f "$LED_SCRIPT" ]; then
    echo "ERROR: LED demo script not found at: $LED_SCRIPT"
    exit 1
fi

echo "=========================================="
echo "  SAP LED Demo Launcher"
echo "=========================================="
echo ""
echo "INFO: Starting LED SAP Demo with Joystick Controls..."
echo "Script location: ${LED_SCRIPT}"
echo ""

# Set PYTHONPATH to include RQB2-bin for imports
export PYTHONPATH="${BIN_DIR}${PYTHONPATH:+:${PYTHONPATH}}"

# Run with virtual environment Python if available
if [ -f "${VENV_PATH}/bin/python3" ]; then
    echo "Using RQB2 virtual environment..."
    "${VENV_PATH}/bin/python3" "${LED_SCRIPT}"
else
    echo "WARNING: RQB2 virtual environment not found at: ${VENV_PATH}"
    echo "Attempting to use system Python..."
    python3 "${LED_SCRIPT}"
fi

# Capture exit status
EXIT_CODE=$?
echo ""
echo "=========================================="
if [ ${EXIT_CODE} -eq 0 ]; then
    echo "✓ Demo completed successfully"
else
    echo "✗ Demo exited with code: ${EXIT_CODE}"
fi
echo "=========================================="
echo ""
read -p "Press Enter to close this window..."