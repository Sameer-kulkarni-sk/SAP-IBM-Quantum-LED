#!/bin/bash
################################################################################
# verify_icon.sh - Verify SAP Icon Setup
#
# Description:
#   Checks if the SAP logo is properly configured for deployment.
#   Validates icon file, desktop file, and deployment script.
#
# Usage:
#   ./scripts/verify_icon.sh
#
# Requirements:
#   - Run from project root directory
#   - SAP logo at desktop/icons/sap-logo.png
#   - Desktop file at desktop/sap-led-demo.desktop
#
# Author: SAP-IBM Quantum LED Demo Project
# License: Apache 2.0
################################################################################

set -e  # Exit on error

# Colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

echo "=========================================="
echo "  SAP Icon Verification"
echo "=========================================="
echo ""

# Check if icon file exists
if [ -f "desktop/icons/sap-logo.png" ]; then
    echo -e "${GREEN}✓${NC} SAP logo found: desktop/icons/sap-logo.png"
    
    # Get file size
    SIZE=$(ls -lh desktop/icons/sap-logo.png | awk '{print $5}')
    echo "  Size: ${SIZE}"
    
    # Check if it's a valid PNG
    if file desktop/icons/sap-logo.png | grep -q "PNG image data"; then
        echo -e "${GREEN}✓${NC} Valid PNG image"
        
        # Get dimensions if ImageMagick is available
        if command -v identify &> /dev/null; then
            DIMS=$(identify desktop/icons/sap-logo.png | awk '{print $3}')
            echo "  Dimensions: ${DIMS}"
        fi
    else
        echo -e "${RED}✗${NC} Not a valid PNG image"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} SAP logo not found at desktop/icons/sap-logo.png"
    echo ""
    echo "Please add your SAP logo as desktop/icons/sap-logo.png"
    exit 1
fi

echo ""

# Check desktop file
if [ -f "desktop/sap-led-demo.desktop" ]; then
    echo -e "${GREEN}✓${NC} Desktop file found"
    
    # Check if it references the correct icon
    if grep -q "Icon=/usr/share/pixmaps/sap-logo.png" desktop/sap-led-demo.desktop; then
        echo -e "${GREEN}✓${NC} Desktop file references sap-logo.png"
    else
        echo -e "${YELLOW}⚠${NC} Desktop file may not reference correct icon"
    fi
else
    echo -e "${RED}✗${NC} Desktop file not found"
    exit 1
fi

echo ""

# Check deployment script
if [ -f "scripts/deploy_to_rasqberry.sh" ]; then
    echo -e "${GREEN}✓${NC} Deployment script found"
    
    if grep -q "sap-logo.png" scripts/deploy_to_rasqberry.sh; then
        echo -e "${GREEN}✓${NC} Deployment script includes icon deployment"
    else
        echo -e "${YELLOW}⚠${NC} Deployment script may not deploy icon"
    fi
else
    echo -e "${RED}✗${NC} Deployment script not found"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Icon setup verified!${NC}"
echo "=========================================="
echo ""
echo "Ready to deploy with custom SAP logo!"
echo ""
echo "Next step:"
echo "  ./scripts/deploy_to_rasqberry.sh <RASQBERRY_IP>"
echo ""
echo "Example:"
echo "  ./scripts/deploy_to_rasqberry.sh 192.168.1.100"
echo ""