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
-  **Virtual Display**: Synchronized virtual LED GUI with automatic mapping fix
-  **Auto-Cycle Mode**: Automatic color cycling when joystick unavailable
-  **Easy Deployment**: One-command deployment with automatic patching


### Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git
cd SAP-IBM-Quantum-LED

# Deploy everything with one command (includes custom SAP logo icon)
./scripts/deploy_to_rasqberry.sh YOUR_RASQBERRY_IP

# If virtual display shows incorrect orientation, apply the fix:
scp patches/patch_virtual_gui.py rasqberry@YOUR_IP:/tmp/
ssh rasqberry@YOUR_IP "sudo python3 /tmp/patch_virtual_gui.py"
```

**Note**: The virtual display patch ensures the virtual LED GUI matches the physical LED mapping exactly. This is needed because the virtual GUI uses a different coordinate system by default.

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

