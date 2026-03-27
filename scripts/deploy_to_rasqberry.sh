#!/bin/bash
################################################################################
# deploy_to_rasqberry.sh - Complete Deployment Script for SAP LED Demo
#
# Description:
#   Deploys the SAP LED demo to RasQberry with desktop icon
#   Includes verification and testing steps
#
# Usage:
#   ./scripts/deploy_to_rasqberry.sh YOUR_RASQBERRY_IP
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RASQBERRY_IP="${1:-}"
RASQBERRY_USER="rasqberry"
RASQBERRY_HOST="${RASQBERRY_USER}@${RASQBERRY_IP}"

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
print_info "Step 2/7: Creating backups..."
ssh "${RASQBERRY_HOST}" "cp /home/rasqberry/led_sap_demo.py /home/rasqberry/led_sap_demo.py.backup 2>/dev/null || true"
print_success "Backups created (if files existed)"

# Step 3: Deploy main demo
print_info "Step 3/7: Deploying main demo script..."
scp src/sap_led_demo.py "${RASQBERRY_HOST}:/home/rasqberry/led_sap_demo.py"
check_status "Main demo deployed" "Failed to deploy main demo"

ssh "${RASQBERRY_HOST}" "chmod +x /home/rasqberry/led_sap_demo.py"

# Step 4: Deploy launcher script
print_info "Step 4/7: Deploying launcher script..."
scp scripts/rq_led_sap_demo.sh "${RASQBERRY_HOST}:/tmp/"
ssh "${RASQBERRY_HOST}" "sudo cp /tmp/rq_led_sap_demo.sh /usr/bin/ && sudo chmod +x /usr/bin/rq_led_sap_demo.sh"
check_status "Launcher script deployed" "Failed to deploy launcher script"

# Step 5: Deploy desktop icon
print_info "Step 5/7: Installing desktop icon..."
scp desktop/sap-led-demo.desktop "${RASQBERRY_HOST}:/tmp/"
scp scripts/install_desktop_icon.sh "${RASQBERRY_HOST}:/tmp/"
ssh "${RASQBERRY_HOST}" "cd /tmp && chmod +x install_desktop_icon.sh && sudo ./install_desktop_icon.sh"
check_status "Desktop icon installed" "Failed to install desktop icon"

# Step 6: Deploy quantum version (optional)
print_info "Step 6/7: Deploying quantum version..."
scp src/sap_quantum_led_demo.py "${RASQBERRY_HOST}:/home/rasqberry/"
ssh "${RASQBERRY_HOST}" "chmod +x /home/rasqberry/sap_quantum_led_demo.py"
print_success "Quantum version deployed"

# Step 7: Verify deployment
print_info "Step 7/7: Verifying deployment..."
echo ""

# Check files exist
print_info "Checking deployed files..."
ssh "${RASQBERRY_HOST}" "test -f /home/rasqberry/led_sap_demo.py" && print_success "✓ Main demo script" || print_error "✗ Main demo script missing"
ssh "${RASQBERRY_HOST}" "test -f /usr/bin/rq_led_sap_demo.sh" && print_success "✓ Launcher script" || print_error "✗ Launcher script missing"
ssh "${RASQBERRY_HOST}" "test -f /home/rasqberry/Desktop/sap-led-demo.desktop" && print_success "✓ Desktop icon" || print_warning "⚠ Desktop icon missing"
ssh "${RASQBERRY_HOST}" "test -f /home/rasqberry/sap_quantum_led_demo.py" && print_success "✓ Quantum version" || print_warning "⚠ Quantum version missing"

echo ""
print_info "Checking Python syntax..."
ssh "${RASQBERRY_HOST}" "/home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 -m py_compile /home/rasqberry/led_sap_demo.py" 2>/dev/null
check_status "✓ Python syntax valid" "✗ Python syntax error"

echo ""
echo "=========================================="
print_success "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Look for 'SAP LED Demo' icon on RasQberry desktop"
echo "2. Double-click the icon to launch the demo"
echo "3. Or run from terminal: sudo /usr/bin/rq_led_sap_demo.sh"
echo ""
echo "Testing:"
echo "  ssh ${RASQBERRY_HOST}"
echo "  sudo /usr/bin/rq_led_sap_demo.sh"
echo ""
echo "Rollback (if needed):"
echo "  ssh ${RASQBERRY_HOST} 'cp /home/rasqberry/led_sap_demo.py.backup /home/rasqberry/led_sap_demo.py'"
echo ""
print_warning "Note: You may need to apply virtual display patches for correct text orientation"
echo "See docs/DEPLOYMENT_GUIDE.md for details"
echo ""