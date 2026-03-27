#!/bin/bash
################################################################################
# verify_icon.sh - Verify SAP Icon Setup
#
# Description:
#   Checks if the SAP logo is properly configured for deployment
################################################################################

echo "=========================================="
echo "  SAP Icon Verification"
echo "=========================================="
echo ""

# Check if icon file exists
if [ -f "desktop/icons/sap-logo.png" ]; then
    echo " SAP logo found: desktop/icons/sap-logo.png"
    
    # Get file size
    SIZE=$(ls -lh desktop/icons/sap-logo.png | awk '{print $5}')
    echo "   Size: $SIZE"
    
    # Check if it's a valid PNG
    if file desktop/icons/sap-logo.png | grep -q "PNG image data"; then
        echo " Valid PNG image"
        
        # Get dimensions
        if command -v identify &> /dev/null; then
            DIMS=$(identify desktop/icons/sap-logo.png | awk '{print $3}')
            echo "   Dimensions: $DIMS"
        fi
    else
        echo " Not a valid PNG image"
        exit 1
    fi
else
    echo " SAP logo not found at desktop/icons/sap-logo.png"
    echo ""
    echo "Please add your SAP logo as desktop/icons/sap-logo.png"
    exit 1
fi

echo ""

# Check desktop file
if [ -f "desktop/sap-led-demo.desktop" ]; then
    echo "✅ Desktop file found"
    
    # Check if it references the correct icon
    if grep -q "Icon=/usr/share/pixmaps/sap-logo.png" desktop/sap-led-demo.desktop; then
        echo "Desktop file references sap-logo.png"
    else
        echo "  Desktop file may not reference correct icon"
    fi
else
    echo " Desktop file not found"
    exit 1
fi

echo ""

# Check deployment script
if [ -f "scripts/deploy_to_rasqberry.sh" ]; then
    echo " Deployment script found"
    
    if grep -q "sap-logo.png" scripts/deploy_to_rasqberry.sh; then
        echo " Deployment script includes icon deployment"
    else
        echo "  Deployment script may not deploy icon"
    fi
else
    echo " Deployment script not found"
    exit 1
fi

echo ""
echo "=========================================="
echo " Icon setup verified!"
echo "=========================================="
echo ""
echo "Ready to deploy with custom SAP logo!"
echo ""
echo "Next step:"
echo "  ./scripts/deploy_to_rasqberry.sh YOUR_RASQBERRY_IP"
echo ""