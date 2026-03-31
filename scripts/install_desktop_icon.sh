#!/bin/bash
################################################################################
# install_desktop_icon.sh - Install SAP LED Demo Desktop Icon
#
# Description:
#   Creates a desktop icon for the SAP LED demo on RasQberry.
#   Must be run on the RasQberry device.
#
# Usage:
#   sudo ./install_desktop_icon.sh
#
# Requirements:
#   - Must be run as root
#   - Desktop file must be in current directory
#   - RasQberry user account must exist
#
# Author: SAP-IBM Quantum LED Demo Project
# License: Apache 2.0
################################################################################

set -e  # Exit on error

# Configuration - can be overridden by environment variables
readonly RASQBERRY_USER="${RASQBERRY_USER:-rasqberry}"
readonly DESKTOP_FILE="sap-led-demo.desktop"
readonly DESKTOP_DIR="/home/${RASQBERRY_USER}/Desktop"
readonly APPLICATIONS_DIR="/usr/share/applications"

echo "=========================================="
echo "  SAP LED Demo Desktop Icon Installer"
echo "=========================================="
echo ""

# Check if desktop file exists in current directory
if [ ! -f "${DESKTOP_FILE}" ]; then
    echo "[ERROR] Desktop file not found: ${DESKTOP_FILE}"
    echo "Please run this script from the directory containing ${DESKTOP_FILE}"
    exit 1
fi

echo "[INFO] Installing SAP LED Demo desktop icon..."
echo ""

# Create Desktop directory if it doesn't exist
if [ ! -d "${DESKTOP_DIR}" ]; then
    echo "[INFO] Creating Desktop directory..."
    mkdir -p "${DESKTOP_DIR}"
    chown ${RASQBERRY_USER}:${RASQBERRY_USER} "${DESKTOP_DIR}"
fi

# Copy to Desktop
echo "[INFO] Installing to Desktop..."
cp "${DESKTOP_FILE}" "${DESKTOP_DIR}/"
chown ${RASQBERRY_USER}:${RASQBERRY_USER} "${DESKTOP_DIR}/${DESKTOP_FILE}"
chmod +x "${DESKTOP_DIR}/${DESKTOP_FILE}"

# Copy to applications directory (optional, for menu)
echo "[INFO] Installing to applications menu..."
cp "${DESKTOP_FILE}" "${APPLICATIONS_DIR}/"
chmod 644 "${APPLICATIONS_DIR}/${DESKTOP_FILE}"

echo ""
echo "=========================================="
echo "[SUCCESS] Desktop icon installed!"
echo "=========================================="
echo ""
echo "You should now see 'SAP LED Demo' icon on the desktop."
echo "Double-click the icon to launch the demo."
echo ""