#!/bin/bash
set -euo pipefail

################################################################################
# rq_led_sap_demo.sh - RasQberry LED SAP Demo Launcher
#
# Description:
#   Launches the SAP LED demo with joystick controls
#   Displays SAP logo with interactive color changes
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${SCRIPT_DIR}/rq_common.sh"

# Ensure running as root (PWM/PIO drivers require GPIO access)
ensure_root "$@"

# Load environment and verify required variables
load_rqb2_env
verify_env_vars USER_HOME REPO BIN_DIR STD_VENV

# Use the integrated demo with joystick controls
LED_SCRIPT="$USER_HOME/led_sap_demo.py"

[ -f "$LED_SCRIPT" ] || die "LED demo script not found at: $LED_SCRIPT"

info "Starting LED SAP Demo with Joystick Controls..."
debug "Script location: $LED_SCRIPT"
echo

# Activate virtual environment if available
activate_venv || warn "Virtual environment not available, continuing anyway..."

# Set PYTHONPATH to include RQB2-bin for imports
export PYTHONPATH="$BIN_DIR:$PYTHONPATH"

# Run the script
python3 "$LED_SCRIPT"

# Script handles its own exit prompt now
echo
read -p "Press Enter to close this window..."