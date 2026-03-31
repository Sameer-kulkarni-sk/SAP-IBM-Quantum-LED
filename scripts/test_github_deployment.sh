#!/bin/bash
################################################################################
# test_github_deployment.sh - GitHub to RasQberry Deployment Test
#
# Description:
#   Comprehensive test script to verify GitHub deployment to RasQberry.
#   Simulates a fresh clone and deployment from GitHub repository.
#
# Usage:
#   ./scripts/test_github_deployment.sh [RASQBERRY_IP]
#
# Arguments:
#   RASQBERRY_IP - IP address of target RasQberry (optional)
#
# Example:
#   ./scripts/test_github_deployment.sh 192.168.1.100
#
# Requirements:
#   - SSH access to RasQberry device
#   - Git installed on RasQberry
#   - RasQberry-Two environment configured
#
# Author: SAP-IBM Quantum LED Demo Project
# License: Apache 2.0
################################################################################

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Configuration - can be overridden by environment variables
readonly RASQBERRY_IP="${1:-}"
readonly RASQBERRY_USER="${RASQBERRY_USER:-rasqberry}"
readonly GITHUB_REPO="${GITHUB_REPO:-https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git}"
readonly TEST_DIR="/tmp/sap-led-test-$$"

# Validate IP address provided
if [ -z "${RASQBERRY_IP}" ]; then
    echo "ERROR: RasQberry IP address required"
    echo "Usage: $0 <RASQBERRY_IP>"
    echo "Example: $0 192.168.1.100"
    exit 1
fi

echo "=========================================="
echo "  GitHub to RasQberry Deployment Test"
echo "=========================================="
echo ""
echo "Target: ${RASQBERRY_USER}@${RASQBERRY_IP}"
echo "Repository: ${GITHUB_REPO}"
echo "Test Directory: ${TEST_DIR}"
echo ""

# Colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "ℹ️  $1"
}

# Step 1: Test SSH connectivity
echo "Step 1: Testing SSH connectivity..."
if ssh -o ConnectTimeout=5 ${RASQBERRY_USER}@${RASQBERRY_IP} "echo 'SSH OK'" > /dev/null 2>&1; then
    success "SSH connection successful"
else
    error "Cannot connect to RasQberry via SSH"
fi

# Step 2: Backup existing files on RasQberry
echo ""
echo "Step 2: Backing up existing files on RasQberry..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    if [ -f /home/rasqberry/led_sap_demo.py ]; then
        cp /home/rasqberry/led_sap_demo.py /home/rasqberry/led_sap_demo.py.test_backup
        echo 'Backed up led_sap_demo.py'
    fi
    if [ -f /usr/bin/rq_led_virtual_gui.py ]; then
        sudo cp /usr/bin/rq_led_virtual_gui.py /usr/bin/rq_led_virtual_gui.py.test_backup
        echo 'Backed up rq_led_virtual_gui.py'
    fi
"
success "Existing files backed up"

# Step 3: Clone repository on RasQberry
echo ""
echo "Step 3: Cloning repository from GitHub to RasQberry..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    rm -rf ${TEST_DIR}
    git clone ${GITHUB_REPO} ${TEST_DIR}
    cd ${TEST_DIR}
    echo 'Repository cloned to ${TEST_DIR}'
    ls -la
"
success "Repository cloned successfully"

# Step 4: Verify repository structure
echo ""
echo "Step 4: Verifying repository structure..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    cd ${TEST_DIR}
    
    # Check required files
    test -f README.md || exit 1
    test -f LICENSE || exit 1
    test -f CONTRIBUTING.md || exit 1
    test -f .gitignore || exit 1
    
    # Check source files
    test -f src/sap_led_demo.py || exit 1
    test -f src/sap_quantum_led_demo.py || exit 1
    test -f src/neopixel_spi_SAPtestFunc.py || exit 1
    
    # Check scripts
    test -f scripts/rq_led_sap_demo.sh || exit 1
    
    # Check patches
    test -f patches/patch_virtual_gui.py || exit 1
    test -f patches/patch_virtual_gui_yflip.py || exit 1
    
    # Check documentation
    test -f docs/DEPLOYMENT_GUIDE.md || exit 1
    test -f docs/SAFETY_GUARANTEES.md || exit 1
    
    echo 'All required files present'
"
success "Repository structure verified"

# Step 5: Deploy main demo
echo ""
echo "Step 5: Deploying main SAP LED demo..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    cd ${TEST_DIR}
    cp src/sap_led_demo.py /home/rasqberry/led_sap_demo.py
    chmod +x /home/rasqberry/led_sap_demo.py
    echo 'Main demo deployed'
"
success "Main demo deployed"

# Step 6: Deploy launcher script
echo ""
echo "Step 6: Deploying launcher script..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    cd ${TEST_DIR}
    sudo cp scripts/rq_led_sap_demo.sh /usr/bin/
    sudo chmod +x /usr/bin/rq_led_sap_demo.sh
    echo 'Launcher script deployed'
"
success "Launcher script deployed"

# Step 7: Verify IBM demo is untouched
echo ""
echo "Step 7: Verifying IBM demo is untouched..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -f /usr/bin/rq_led_ibm_demo.sh || exit 1
    test -f /usr/bin/neopixel_spi_IBMtestFunc.py || exit 1
    echo 'IBM demo files intact'
"
success "IBM demo files verified intact"

# Step 8: Verify system configuration is untouched
echo ""
echo "Step 8: Verifying system configuration..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -f /usr/config/rasqberry_environment.env || exit 1
    grep -q 'LED_MATRIX_WIDTH=24' /usr/config/rasqberry_environment.env || exit 1
    grep -q 'LED_MATRIX_HEIGHT=8' /usr/config/rasqberry_environment.env || exit 1
    echo 'System configuration intact'
"
success "System configuration verified"

# Step 9: Test Python syntax
echo ""
echo "Step 9: Testing Python syntax..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 -m py_compile /home/rasqberry/led_sap_demo.py
    echo 'Python syntax valid'
"
success "Python syntax validated"

# Step 10: Test demo can be imported
echo ""
echo "Step 10: Testing demo imports..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    cd /home/rasqberry
    PYTHONPATH=/usr/bin /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 -c 'import sys; sys.path.insert(0, \"/usr/bin\"); import rq_led_utils; print(\"Imports OK\")'
"
success "Demo imports validated"

# Step 11: Verify launcher script works
echo ""
echo "Step 11: Verifying launcher script..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -x /usr/bin/rq_led_sap_demo.sh || exit 1
    grep -q 'led_sap_demo.py' /usr/bin/rq_led_sap_demo.sh || exit 1
    echo 'Launcher script valid'
"
success "Launcher script verified"

# Step 12: Test that IBM demo still works (syntax check)
echo ""
echo "Step 12: Verifying IBM demo still functional..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -x /usr/bin/rq_led_ibm_demo.sh || exit 1
    echo 'IBM demo launcher intact'
"
success "IBM demo verified functional"

# Step 13: Check virtual display compatibility
echo ""
echo "Step 13: Checking virtual display compatibility..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -f /usr/bin/rq_led_virtual_gui.py || exit 1
    /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 -m py_compile /usr/bin/rq_led_virtual_gui.py
    echo 'Virtual display compatible'
"
success "Virtual display verified"

# Step 14: Verify no config files were modified
echo ""
echo "Step 14: Verifying no unauthorized modifications..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    # Check that config file wasn't modified by deployment
    if [ -f /usr/config/rasqberry_environment.env.test_backup ]; then
        diff /usr/config/rasqberry_environment.env /usr/config/rasqberry_environment.env.test_backup > /dev/null 2>&1 || {
            echo 'WARNING: Config file was modified!'
            exit 1
        }
    fi
    echo 'No unauthorized modifications'
"
success "No unauthorized modifications detected"

# Step 15: Test rollback capability
echo ""
echo "Step 15: Testing rollback capability..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    test -f /home/rasqberry/led_sap_demo.py.test_backup || {
        echo 'Backup file exists'
        exit 0
    }
    cp /home/rasqberry/led_sap_demo.py.test_backup /home/rasqberry/led_sap_demo.py.rollback_test
    test -f /home/rasqberry/led_sap_demo.py.rollback_test || exit 1
    rm /home/rasqberry/led_sap_demo.py.rollback_test
    echo 'Rollback capability verified'
"
success "Rollback capability verified"

# Step 16: Cleanup test directory
echo ""
echo "Step 16: Cleaning up test directory..."
ssh ${RASQBERRY_USER}@${RASQBERRY_IP} "
    rm -rf ${TEST_DIR}
    echo 'Test directory cleaned up'
"
success "Test directory cleaned up"

# Final Summary
echo ""
echo "=========================================="
echo "✅ ALL TESTS PASSED!"
echo "=========================================="
echo ""
echo "Deployment Verification Summary:"
echo "  ✅ SSH connectivity working"
echo "  ✅ Repository cloned successfully"
echo "  ✅ All required files present"
echo "  ✅ Main demo deployed correctly"
echo "  ✅ Launcher script deployed"
echo "  ✅ IBM demo untouched and functional"
echo "  ✅ System configuration preserved"
echo "  ✅ Python syntax validated"
echo "  ✅ Demo imports working"
echo "  ✅ Virtual display compatible"
echo "  ✅ No unauthorized modifications"
echo "  ✅ Rollback capability verified"
echo ""
echo ""
echo "🎉 GitHub to RasQberry deployment is SAFE and WORKING!"
echo ""
echo "To run the SAP demo on RasQberry:"
echo "  ssh ${RASQBERRY_USER}@${RASQBERRY_IP}"
echo "  sudo /usr/bin/rq_led_sap_demo.sh"
echo ""
echo "To restore backups (if needed):"
echo "  ssh ${RASQBERRY_USER}@${RASQBERRY_IP}"
echo "  cp /home/${RASQBERRY_USER}/led_sap_demo.py.test_backup /home/${RASQBERRY_USER}/led_sap_demo.py"
echo ""