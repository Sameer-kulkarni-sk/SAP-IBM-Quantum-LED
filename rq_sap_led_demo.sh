#!/bin/bash
#
# RasQberry: SAP LED Demo Launcher
# Matches IBM Quantum Raspberry Tie launcher structure
#

set -euo pipefail

# Ensure running as root (PWM/PIO LED drivers require GPIO access)
if [ "$EUID" -ne 0 ]; then
    echo "Restarting with sudo..."
    exec sudo -E "$0" "$@"
fi

# Demo configuration
DEMO_NAME="SAP LED Demo"
DEMO_FILE="/home/rasqberry/led_sap_demo.py"

# Variable to track the Python process
PYTHON_PID=""

# Function to clean up on exit
cleanup() {
    echo
    echo "Stopping SAP LED Demo..."

    # Kill the Python process if it's still running
    if [ -n "$PYTHON_PID" ] && kill -0 "$PYTHON_PID" 2>/dev/null; then
        kill "$PYTHON_PID" 2>/dev/null || true
        sleep 0.5

        # Force kill if still running
        if kill -0 "$PYTHON_PID" 2>/dev/null; then
            kill -9 "$PYTHON_PID" 2>/dev/null || true
        fi
    fi

    # Turn off LEDs
    python3 -c "
try:
    import board, neopixel
    pixels = neopixel.NeoPixel(board.D18, 192, auto_write=False)
    pixels.fill((0,0,0))
    pixels.show()
except: pass
" 2>/dev/null || true

    echo "Demo stopped."
}

# Set up trap to clean up on exit
trap cleanup EXIT INT TERM

# Check if demo file exists
if [ ! -f "$DEMO_FILE" ]; then
    echo "Error: Demo file not found: $DEMO_FILE"
    echo "Press Enter to close..."
    read
    exit 1
fi

# Launch the demo
echo "=========================================="
echo "Starting SAP LED Demo..."
echo "=========================================="
echo ""

cd /home/rasqberry || exit 1

# Run the demo in background
python3 "$DEMO_FILE" </dev/null &
PYTHON_PID=$!

echo "Demo is running (PID: $PYTHON_PID)"
echo ""
echo "Controls:"
echo "  - SenseHat Joystick UP: Rainbow mode"
echo "  - SenseHat Joystick DOWN: Blink mode"
echo "  - SenseHat Joystick LEFT/RIGHT: SAP X IBM mode"
echo "  - SenseHat Joystick CENTER: Exit demo"
echo ""
echo "To stop the demo:"
echo "  - Press 'q' and Enter"
echo "  - Or just press Enter"
echo "  - Or press Ctrl+C"
echo "=========================================="
echo ""

# Clear any buffered input
while read -t 0; do read -t 0.1 -n 1000; done 2>/dev/null

# Wait for user input to quit
while kill -0 "$PYTHON_PID" 2>/dev/null; do
    if read -t 1 -n 1 key 2>/dev/null; then
        if [ "$key" = "q" ] || [ -z "$key" ]; then
            echo ""
            echo "Stop requested by user..."
            break
        fi
    fi
done

# Check if process is still running
if kill -0 "$PYTHON_PID" 2>/dev/null; then
    echo "Stopping demo..."
    EXIT_CODE=0
else
    wait "$PYTHON_PID"
    EXIT_CODE=$?
fi

# Show exit status
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "Demo finished successfully."
else
    echo "Demo exited with code: $EXIT_CODE"
fi
echo ""
echo "Press Enter to close this window..."
read