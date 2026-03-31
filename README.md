# SAP Quantum LED Demo for RasQberry

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-purple.svg)](https://qiskit.org/)

A quantum-powered LED demonstration for RasQberry that displays "SAP" text on a 24×8 NeoPixel LED matrix with interactive controls and optional quantum computing features.


## Features

-  **Correct Text Display**: "SAP" text properly oriented on both physical LEDs and virtual display
-  **Interactive Controls**: Joystick button controls for color changes
-  **Multiple Colors**: Blue, Red, Green, Yellow, Rainbow, and more
-  **Quantum Computing**: Optional Qiskit integration for quantum-powered color generation
-  **Virtual Display**: Synchronized virtual LED GUI for monitoring
-  **Auto-Cycle Mode**: Automatic color cycling when joystick unavailable

## Hardware Requirements

- **RasQberry Device** (Raspberry Pi with quantum computing support)
- **24×8 NeoPixel LED Matrix** (192 LEDs, quad panel layout)
- **Sense HAT** (optional, for joystick controls)
- **GPIO Pin 18** for LED control

## Software Requirements

- Python 3.7 or higher
- RasQberry Two environment
- Required Python packages:
  - `rpi_ws281x` (NeoPixel control)
  - `qiskit` (quantum computing, optional)
  - `qiskit-aer` (quantum simulator, optional)
  - `sense_hat` (joystick input, optional)

## Installation

> **⚠️ IMPORTANT**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for safe deployment that won't affect other RasQberry demos or system files.

### Quick Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git
cd SAP-IBM-Quantum-LED

# Verify icon setup (optional)
./scripts/verify_icon.sh

# Deploy everything with one command (includes custom SAP logo icon)
./scripts/deploy_to_rasqberry.sh YOUR_RASQBERRY_IP
```

This automated script will:
-  Deploy the demo to RasQberry
-  Install custom SAP logo icon (if provided)
-  Create desktop shortcut with SAP branding
-  Install launcher script
-  Deploy quantum version
-  Verify installation

### Manual Installation

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for step-by-step manual deployment instructions.

### 3. Configure LED Matrix

Ensure `/usr/config/rasqberry_environment.env` has:

```bash
LED_MATRIX_WIDTH=24
LED_MATRIX_HEIGHT=8
LED_MATRIX_LAYOUT=quad
LED_MATRIX_Y_FLIP=true
LED_VIRTUAL_MIRROR=true
```


## Project Structure

```
SAP-IBM-Quantum-LED/
├── src/                              # Source code
│   ├── sap_led_demo.py              # Main LED demo (production)
│   ├── sap_quantum_led_demo.py      # Quantum-enabled version
│   └── neopixel_spi_SAPtestFunc.py  # Standalone text display
├── scripts/                          # Deployment & utility scripts
│   ├── deploy_to_rasqberry.sh       # Automated deployment script
│   ├── rq_led_sap_demo.sh           # Launcher script
│   └── install_desktop_icon.sh      # Desktop icon installer
├── desktop/                          # Desktop integration
│   └── sap-led-demo.desktop         # Desktop entry file
├── patches/                          # System patches
│   ├── patch_virtual_gui.py         # Fix virtual display mapping
│   └── patch_virtual_gui_yflip.py   # Add Y-flip support
├── docs/                             # Documentation
│   ├── DEPLOYMENT_GUIDE.md          # Safe deployment guide
│   ├── DOCUMENTATION_CHANGELOG.md   # Documentation changes log
│   └── SAFETY_GUARANTEES.md         # Safety & isolation info
├── .github/                          # GitHub configuration
│   ├── workflows/validate.yml       # CI/CD validation
│   └── COMMIT_TEMPLATE.md           # Commit message template
└── README.md                         # This file
```

## Quantum Features

The quantum version (`sap_quantum_led_demo.py`) includes:

### 3-Qubit Color Selector
- Creates superposition of 8 possible colors
- Uses Hadamard gates for equal probability
- Provides true quantum randomness

### 8-Qubit RGB Generator
- Generates custom RGB colors via quantum measurement
- 3 qubits for Red, 3 for Green, 2 for Blue
- 256 possible color combinations

### Example Quantum Circuit

```python
from qiskit import QuantumCircuit
from qiskit_aer import Aer

# Create 3-qubit circuit
qc = QuantumCircuit(3, 3)

# Apply Hadamard gates (superposition)
qc.h(0)
qc.h(1)
qc.h(2)

# Measure
qc.measure([0, 1, 2], [0, 1, 2])

# Execute on simulator
backend = Aer.get_backend('qasm_simulator')
job = backend.run(transpile(qc, backend), shots=1)
result = job.result()
```

## Technical Details

### LED Matrix Configuration

- **Size**: 24×8 (192 LEDs total)
- **Layout**: Quad (4 panels of 12×4 in 2×2 grid)
- **Wiring**: TL→TR→BR→BL
- **Coordinate System**: (0,0) = top-left, (23,7) = bottom-right
- **Y-Flip**: Applied for correct orientation


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

