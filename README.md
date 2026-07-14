# SAP Quantum LED — RasQberry external demo

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-purple.svg)](https://qiskit.org/)

Displays the SAP logo on any RasQberry LED matrix with quantum-random color patterns, using the official `rq_led_utils` API so the demo works on every panel layout (24×8, quad, 8×32, …).

## What it shows

Three modes rotate every 4 seconds:

| Mode | Quantum input |
|---|---|
| Per-LED color | one 3-qubit measurement per lit pixel |
| Per-row stripe | one 3-qubit measurement per row |
| Single solid color | one 3-qubit measurement for the whole logo |

A 3-qubit Hadamard circuit (`qc.h(range(3)); qc.measure_all()`) is run on `AerSimulator` each cycle; each 3-bit outcome maps to one of 8 palette entries. When `qiskit-aer` is not available the demo falls back to Python's `random` module seamlessly.

## Files

| File | Purpose |
|---|---|
| `sap_quantum_led.py` | Main demo script (entrypoint) |
| `rqb-demo.json` | RasQberry manifest |
| `desktop/icons/sap-logo.png` | SAP logo asset |
| `LICENSE` | Apache 2.0 |

## Running manually

```bash
sudo python3 sap_quantum_led.py
```

`rq_led_utils` is importable from `/usr/bin` on any RasQberry image. Qiskit and qiskit-aer are preinstalled in the RasQberry Python venv — no extra `pip install` needed.

## Installing via RasQberry

Once this repo is added to the RasQberry catalog:

```bash
rq_demo_add_external.sh sap-quantum-led
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
