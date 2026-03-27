# SAP Quantum LED Demo for RasQberry

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-purple.svg)](https://qiskit.org/)

A quantum-powered LED demonstration for RasQberry that displays "SAP" text on a 24×8 NeoPixel LED matrix with interactive controls and optional quantum computing features.

![SAP LED Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## Features

- ✅ **Correct Text Display**: "SAP" text properly oriented on both physical LEDs and virtual display
- ✅ **Interactive Controls**: Joystick button controls for color changes
- ✅ **Multiple Colors**: Blue, Red, Green, Yellow, Rainbow, and more
- ✅ **Quantum Computing**: Optional Qiskit integration for quantum-powered color generation
- ✅ **Virtual Display**: Synchronized virtual LED GUI for monitoring
- ✅ **Auto-Cycle Mode**: Automatic color cycling when joystick unavailable

## Hardware Requirements

- **RasQberry Device** (Raspberry Pi with quantum computing support)
- **24×8 NeoPixel LED Matrix** (192 LEDs, quad panel layout)
- **Sense HAT** (optional, for joystick controls)
- **GPIO Pin 18** for LED control

## Software Requirements

- Python 3.11+
- RasQberry Two environment
- Required Python packages:
  - `rpi_ws281x` (NeoPixel control)
  - `qiskit` (quantum computing, optional)
  - `qiskit-aer` (quantum simulator, optional)
  - `sense_hat` (joystick input, optional)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/SAP-IBM-Quantum-LED.git
cd SAP-IBM-Quantum-LED
```

### 2. Deploy to RasQberry

```bash
# Copy main demo
scp src/sap_led_demo.py rasqberry@YOUR_IP:/home/rasqberry/led_sap_demo.py

# Copy launcher script
scp scripts/rq_led_sap_demo.sh rasqberry@YOUR_IP:/tmp/
ssh rasqberry@YOUR_IP "sudo cp /tmp/rq_led_sap_demo.sh /usr/bin/ && sudo chmod +x /usr/bin/rq_led_sap_demo.sh"

# Apply virtual display patches (optional)
scp patches/patch_virtual_gui.py rasqberry@YOUR_IP:/tmp/
scp patches/patch_virtual_gui_yflip.py rasqberry@YOUR_IP:/tmp/
ssh rasqberry@YOUR_IP "sudo python3 /tmp/patch_virtual_gui.py && sudo python3 /tmp/patch_virtual_gui_yflip.py"
```

### 3. Configure LED Matrix

Ensure `/usr/config/rasqberry_environment.env` has:

```bash
LED_MATRIX_WIDTH=24
LED_MATRIX_HEIGHT=8
LED_MATRIX_LAYOUT=quad
LED_MATRIX_Y_FLIP=true
LED_VIRTUAL_MIRROR=true
```

## Usage

### Method 1: Desktop Icon

Double-click the "SAP LED Demo" icon on the RasQberry desktop.

### Method 2: Command Line

```bash
sudo /usr/bin/rq_led_sap_demo.sh
```

### Method 3: Direct Python

```bash
cd /home/rasqberry
sudo PYTHONPATH=/usr/bin /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 led_sap_demo.py
```

### Method 4: Quantum Version

```bash
cd /home/rasqberry
sudo PYTHONPATH=/usr/bin /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 sap_quantum_led_demo.py
```

## Controls

### Joystick Controls

| Button | Action |
|--------|--------|
| **UP** | Blue SAP |
| **DOWN** | Red SAP |
| **LEFT** | Green SAP |
| **RIGHT** | Yellow SAP |
| **PUSH** | Rainbow SAP |

### Keyboard

- **Ctrl+C**: Exit demo

## Project Structure

```
SAP-IBM-Quantum-LED/
├── src/                          # Source code
│   ├── sap_led_demo.py          # Main LED demo (production)
│   ├── sap_quantum_led_demo.py  # Quantum-enabled version
│   └── neopixel_spi_SAPtestFunc.py  # Standalone text display
├── scripts/                      # Deployment scripts
│   └── rq_led_sap_demo.sh       # Launcher script
├── patches/                      # System patches
│   ├── patch_virtual_gui.py     # Fix virtual display mapping
│   └── patch_virtual_gui_yflip.py  # Add Y-flip support
├── docs/                         # Documentation
│   ├── FINAL_SOLUTION_SUMMARY.md
│   ├── QUANTUM_ANALYSIS.md
│   ├── SAP_QUANTUM_LED_DEMO_COMPLETE.md
│   ├── SAP_LED_INTEGRATION_COMPLETE.md
│   └── SAP_LED_DEMO_FINAL_SUMMARY.md
└── README.md                     # This file
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

### Coordinate Mapping

The demo uses a complex quad panel mapping algorithm:

```python
def map_xy_to_pixel_quad(x, y):
    x1 = x * 4 + (0 if x % 2 == 0 else 3)
    y1 = (7 - y if x % 2 == 0 else y - 7)
    x2 = 96 + (23 - x) * 4 + (0 if x % 2 == 0 else 3)
    y2 = (3 - y if x % 2 == 0 else y - 3)
    return x2 + y2 if y < 4 else x1 + y1
```

## Troubleshooting

### Issue: Text appears garbled in virtual display
**Solution**: Apply the virtual display patches:
```bash
sudo python3 /tmp/patch_virtual_gui.py
sudo python3 /tmp/patch_virtual_gui_yflip.py
```

### Issue: Text upside down on physical LEDs
**Solution**: Ensure `LED_MATRIX_Y_FLIP=true` in config

### Issue: Permission denied
**Solution**: Run with sudo:
```bash
sudo /usr/bin/rq_led_sap_demo.sh
```

### Issue: Qiskit not found
**Solution**: Install in RQB2 environment:
```bash
source /home/rasqberry/RasQberry-Two/venv/RQB2/bin/activate
pip install qiskit qiskit-aer
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **RasQberry Project** - Quantum computing on Raspberry Pi
- **IBM Quantum** - Qiskit framework and quantum computing resources
- **SAP** - Inspiration for the demo

## Related Projects

- [RasQberry](https://github.com/JanLahmann/RasQberry) - Quantum computing on Raspberry Pi
- [Qiskit](https://github.com/Qiskit/qiskit) - Open-source quantum computing framework
- [IBM Quantum](https://quantum-computing.ibm.com/) - IBM's quantum computing platform

## Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for the quantum computing community**