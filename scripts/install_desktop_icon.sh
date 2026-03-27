#!/bin/bash
################################################################################
# install_desktop_icon.sh - Install SAP LED Demo Desktop Icon
#
# Description:
#   Creates a desktop icon for the SAP LED demo on RasQberry
#   Must be run on the RasQberry device
################################################################################

# Configuration
DESKTOP_FILE="sap-led-demo.desktop"
DESKTOP_DIR="/home/rasqberry/Desktop"
APPLICATIONS_DIR="/usr/share/applications"

echo "Installing SAP LED Demo desktop icon..."

# Check if desktop file exists in current directory
if [ ! -f "$DESKTOP_FILE" ]; then
    echo "[ERROR] Desktop file not found: $DESKTOP_FILE"
    echo "Please run this script from the directory containing $DESKTOP_FILE"
    exit 1
fi

# Create Desktop directory if it doesn't exist
if [ ! -d "$DESKTOP_DIR" ]; then
    echo "[INFO] Creating Desktop directory..."
    mkdir -p "$DESKTOP_DIR"
    chown rasqberry:rasqberry "$DESKTOP_DIR"
fi

# Copy to Desktop
echo "[INFO] Installing to Desktop..."
cp "$DESKTOP_FILE" "$DESKTOP_DIR/"
chown rasqberry:rasqberry "$DESKTOP_DIR/$DESKTOP_FILE"
chmod +x "$DESKTOP_DIR/$DESKTOP_FILE"

# Copy to applications directory (optional, for menu)
echo "[INFO] Installing to applications menu..."
sudo cp "$DESKTOP_FILE" "$APPLICATIONS_DIR/"
sudo chmod 644 "$APPLICATIONS_DIR/$DESKTOP_FILE"

echo ""
echo "[SUCCESS] Desktop icon installed successfully!"
echo ""
echo "You should now see 'SAP LED Demo' icon on the desktop."
echo "Double-click the icon to launch the demo."
echo ""