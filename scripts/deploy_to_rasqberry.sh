#!/bin/bash
################################################################################
# deploy_to_rasqberry.sh - Complete Deployment Script for SAP LED Demo
#
# Description:
#   Deploys the SAP LED demo to RasQberry with desktop icon.
#   Includes verification and testing steps.
#
# Usage:
#   ./scripts/deploy_to_rasqberry.sh <RASQBERRY_IP>
#
# Arguments:
#   RASQBERRY_IP - IP address of the target RasQberry device
#
# Example:
#   ./scripts/deploy_to_rasqberry.sh 192.168.1.100
#
# Requirements:
#   - SSH access to RasQberry device
#   - RasQberry device with RasQberry-Two installed
#   - Source files in src/ and scripts/ directories
#
# Author: SAP-IBM Quantum LED Demo Project
# License: Apache 2.0
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Configuration - can be overridden by environment variables
readonly RASQBERRY_IP="${1:-}"
readonly RASQBERRY_USER="${RASQBERRY_USER:-rasqberry}"
readonly RASQBERRY_HOST="${RASQBERRY_USER}@${RASQBERRY_IP}"
readonly RASQBERRY_HOME="/home/${RASQBERRY_USER}"
readonly VENV_PATH="${RASQBERRY_HOME}/RasQberry-Two/venv/RQB2"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        print_success "$1"
    else
        print_error "$2"
        exit 1
    fi
}

# Validate input
if [ -z "$RASQBERRY_IP" ]; then
    print_error "Usage: $0 <RASQBERRY_IP>"
    echo "Example: $0 100.67.33.252"
    exit 1
fi

echo ""
echo "=========================================="
echo "  SAP LED Demo Deployment to RasQberry"
echo "=========================================="
echo ""
print_info "Target: ${RASQBERRY_HOST}"
echo ""

# Step 1: Test connection
print_info "Step 1/7: Testing connection to RasQberry..."
ssh -o ConnectTimeout=5 "${RASQBERRY_HOST}" "echo 'Connection successful'" > /dev/null 2>&1
check_status "Connection established" "Cannot connect to ${RASQBERRY_HOST}"

# Step 2: Backup existing files
print_info "Step 2/8: Creating backups..."
ssh "${RASQBERRY_HOST}" "cp ${RASQBERRY_HOME}/led_sap_demo.py ${RASQBERRY_HOME}/led_sap_demo.py.backup 2>/dev/null || true"
print_success "Backups created (if files existed)"

# Step 3: Deploy main demo
print_info "Step 3/8: Deploying main demo script..."
scp src/sap_led_demo.py "${RASQBERRY_HOST}:${RASQBERRY_HOME}/led_sap_demo.py"
check_status "Main demo deployed" "Failed to deploy main demo"

ssh "${RASQBERRY_HOST}" "chmod +x ${RASQBERRY_HOME}/led_sap_demo.py"

# Step 4: Deploy launcher script
print_info "Step 4/8: Deploying launcher script..."
scp scripts/rq_led_sap_demo.sh "${RASQBERRY_HOST}:/tmp/"
ssh "${RASQBERRY_HOST}" "sudo cp /tmp/rq_led_sap_demo.sh /usr/bin/ && sudo chmod +x /usr/bin/rq_led_sap_demo.sh"
check_status "Launcher script deployed" "Failed to deploy launcher script"

# Step 5: Deploy custom icon (if available)
print_info "Step 5/8: Checking for custom SAP icon..."
if [ -f "desktop/icons/sap-logo.png" ]; then
    print_info "Custom SAP icon found, deploying..."
    scp desktop/icons/sap-logo.png "${RASQBERRY_HOST}:/tmp/"
    ssh "${RASQBERRY_HOST}" "sudo cp /tmp/sap-logo.png /usr/share/pixmaps/sap-logo.png && sudo chmod 644 /usr/share/pixmaps/sap-logo.png"
    check_status "Custom SAP icon deployed" "Failed to deploy custom icon"
else
    print_warning "No custom icon found at desktop/icons/sap-logo.png"
    print_info "Using default RasQberry icon as fallback"
    # Create a fallback by copying rasqberry icon
    ssh "${RASQBERRY_HOST}" "sudo cp /usr/share/pixmaps/rasqberry.png /usr/share/pixmaps/sap-logo.png 2>/dev/null || true"
fi

# Step 6: Deploy desktop icon
print_info "Step 6/8: Installing desktop icon..."
scp desktop/sap-led-demo.desktop "${RASQBERRY_HOST}:/tmp/"
scp scripts/install_desktop_icon.sh "${RASQBERRY_HOST}:/tmp/"
ssh "${RASQBERRY_HOST}" "cd /tmp && chmod +x install_desktop_icon.sh && sudo ./install_desktop_icon.sh"
check_status "Desktop icon installed" "Failed to install desktop icon"

# Step 7: Deploy quantum version (optional)
print_info "Step 7/8: Deploying quantum version..."
scp src/sap_quantum_led_demo.py "${RASQBERRY_HOST}:${RASQBERRY_HOME}/"
ssh "${RASQBERRY_HOST}" "chmod +x ${RASQBERRY_HOME}/sap_quantum_led_demo.py"
print_success "Quantum version deployed"

# Step 8: Verify deployment
print_info "Step 8/8: Verifying deployment..."
echo ""

# Check files exist
print_info "Checking deployed files..."
ssh "${RASQBERRY_HOST}" "test -f ${RASQBERRY_HOME}/led_sap_demo.py" && print_success "✓ Main demo script" || print_error "✗ Main demo script missing"
ssh "${RASQBERRY_HOST}" "test -f /usr/bin/rq_led_sap_demo.sh" && print_success "✓ Launcher script" || print_error "✗ Launcher script missing"
ssh "${RASQBERRY_HOST}" "test -f ${RASQBERRY_HOME}/Desktop/sap-led-demo.desktop" && print_success "✓ Desktop icon file" || print_warning "⚠ Desktop icon missing"
ssh "${RASQBERRY_HOST}" "test -f /usr/share/pixmaps/sap-logo.png" && print_success "✓ SAP logo icon" || print_warning "⚠ SAP logo missing"
ssh "${RASQBERRY_HOST}" "test -f ${RASQBERRY_HOME}/sap_quantum_led_demo.py" && print_success "✓ Quantum version" || print_warning "⚠ Quantum version missing"

echo ""
print_info "Checking Python syntax..."
ssh "${RASQBERRY_HOST}" "${VENV_PATH}/bin/python3 -m py_compile ${RASQBERRY_HOME}/led_sap_demo.py" 2>/dev/null
check_status "✓ Python syntax valid" "✗ Python syntax error"

echo ""
echo "=========================================="
print_success "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Look for 'SAP LED Demo' icon on RasQberry desktop"
echo "   - Icon should display SAP logo (if custom icon was provided)"
echo "2. Double-click the icon to launch the demo"
echo "3. Or run from terminal: sudo /usr/bin/rq_led_sap_demo.sh"
echo ""
echo "Custom Icon:"
if [ -f "desktop/icons/sap-logo.png" ]; then
    echo "  ✓ Custom SAP logo deployed"
else
    echo "  ⚠ No custom icon - using RasQberry logo as fallback"
    echo "  To add custom icon: Save your logo as desktop/icons/sap-logo.png and re-run deployment"
fi
echo ""
echo "Testing:"
echo "  ssh ${RASQBERRY_HOST}"
echo "  sudo /usr/bin/rq_led_sap_demo.sh"
echo ""
echo "Rollback (if needed):"
echo "  ssh ${RASQBERRY_HOST} 'cp ${RASQBERRY_HOME}/led_sap_demo.py.backup ${RASQBERRY_HOME}/led_sap_demo.py'"
echo ""
print_warning "Note: You may need to apply virtual display patches for correct text orientation"
echo "See docs/DEPLOYMENT_GUIDE.md for details"
echo ""