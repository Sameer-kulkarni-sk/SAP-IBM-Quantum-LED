# SAP LED Demo for RasQberry

A Python-based LED display demo that shows "SAP" on NeoPixel LED matrices, designed for the RasQberry quantum computing platform.

## 🎯 Overview

This project displays the SAP logo across multiple 8x8 LED panels with interactive controls via SenseHat joystick. It matches the functionality and structure of the IBM Quantum LED demo.

## 📋 Features

- ✅ Displays "SAP" across 4x 8x8 LED panels (32x8 total)
- ✅ SAP brand colors: Blue (#0070F2) and Gold (#F0AB00)
- ✅ Interactive controls via SenseHat joystick
- ✅ Rainbow animation mode
- ✅ Proper LED cleanup on exit
- ✅ Desktop launcher icon
- ✅ Compatible with RasQberry Two hardware

## 🔧 Hardware Requirements

- Raspberry Pi (tested on Pi 5)
- 4x 8x8 NeoPixel LED panels (WS2812B, 192 LEDs total)
- GPIO 18 for LED control
- SenseHat (optional, for joystick controls)
- RasQberry Two platform

## 📦 Installation

### On RasQberry Device

1. **Copy files to RasQberry:**
```bash
scp sap_led_demo_multi_panel.py rasqberry@YOUR_IP:/home/rasqberry/led_sap_demo.py
scp rq_sap_led_demo.sh rasqberry@YOUR_IP:/home/rasqberry/
scp sap-led-demo.desktop rasqberry@YOUR_IP:/home/rasqberry/Desktop/led_sap_demo.desktop
```

2. **Make scripts executable:**
```bash
ssh rasqberry@YOUR_IP
chmod +x /home/rasqberry/rq_sap_led_demo.sh
chmod +x /home/rasqberry/Desktop/led_sap_demo.desktop
```

3. **Verify RQB2 virtual environment:**
```bash
ls /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3
```

## 🚀 Usage

### Desktop Icon
Double-click the "SAP LED Demo" icon on the desktop.

### Command Line
```bash
sudo /home/rasqberry/rq_sap_led_demo.sh
```

### Direct Python
```bash
sudo /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 /home/rasqberry/led_sap_demo.py
```

## 🎮 Controls

| Control | Action |
|---------|--------|
| **Joystick UP** | Toggle rainbow mode |
| **Joystick DOWN** | Return to normal colors |
| **Joystick CENTER** | Exit demo |
| **Ctrl+C** | Exit demo |

## 🎨 Display Layout

The demo uses 4x 8x8 LED panels arranged horizontally:

```
┌────────┬────────┬────────┬────────┐
│   S    │   A    │   P    │ (blank)│
│ (Blue) │ (Gold) │ (Blue) │        │
└────────┴────────┴────────┴────────┘
 Panel 1  Panel 2  Panel 3  Panel 4
```

## 📁 Repository Structure

```
SAP-IBM-Quantum-LED/
├── README.md                      # This file
├── sap_led_demo_multi_panel.py   # Main demo (multi-panel version)
├── sap_led_demo_final_v2.py      # Single 8x8 version
├── rq_sap_led_demo.sh            # Launcher script
├── sap-led-demo.desktop           # Desktop icon
├── SAP_LED_DEMO_SOLUTION.md      # Detailed technical documentation
├── ibm_led_demo.py                # Reference IBM demo
└── docs/
    ├── QUICK_START.md
    ├── TESTING_GUIDE.md
    └── FINAL_INSTRUCTIONS.md
```

## 🔍 Technical Details

### LED Configuration
- **Total LEDs:** 192 (4 panels × 8×8)
- **GPIO Pin:** 18
- **Pixel Order:** GRB
- **Brightness:** 0.4 (40%)
- **Matrix Size:** 24×8 (configured) or 32×8 (physical)

### Virtual Environment
- **Path:** `/home/rasqberry/RasQberry-Two/venv/RQB2`
- **Python:** Python 3.11
- **Key Packages:**
  - Adafruit-Blinka 8.68.1
  - adafruit-circuitpython-neopixel 6.3.18
  - Adafruit-Blinka-Raspberry-Pi5-Neopixel 1.0.0rc2

### LED Mapping
Uses RasQberry LED utilities (`rq_led_utils`) for:
- Layout-aware pixel mapping
- Coordinate transformation (x,y → LED index)
- Support for tiled/serpentine arrangements
- Y-axis flipping

## 🐛 Troubleshooting

### LEDs Not Displaying
**Problem:** No LED output  
**Solution:** 
1. Ensure using RQB2 venv Python
2. Run with sudo for GPIO access
3. Check LED hardware connections

### "GPIO busy" Error
**Problem:** GPIO already in use  
**Solution:**
```bash
sudo pkill -9 python3
sudo /usr/bin/rq_clear_leds.sh
```

### Wrong Pattern Displayed
**Problem:** Pattern doesn't look like "SAP"  
**Solution:**
1. Verify you have 4x 8x8 panels
2. Check LED matrix configuration
3. Use `sap_led_demo_multi_panel.py` version

### Desktop Icon Doesn't Work
**Problem:** Icon doesn't launch demo  
**Solution:**
```bash
chmod +x /home/rasqberry/rq_sap_led_demo.sh
chmod +x /home/rasqberry/Desktop/led_sap_demo.desktop
```

## 📚 Documentation

- **[SAP_LED_DEMO_SOLUTION.md](SAP_LED_DEMO_SOLUTION.md)** - Complete technical documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick setup guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures

## 🔄 Version History

### v3.0 - Multi-Panel Version (Current)
- Supports 4x 8x8 LED panels
- Each letter on separate panel
- Improved LED mapping

### v2.0 - Fixed Pattern Version
- Corrected 1D pixel list format
- Fixed neopixel library imports
- Added RQB2 venv support

### v1.0 - Initial Version
- Basic SAP display
- 2D matrix (incorrect format)

## 🤝 Comparison with IBM Demo

| Feature | IBM Demo | SAP Demo | Status |
|---------|----------|----------|--------|
| LED Hardware | ✅ NeoPixel | ✅ NeoPixel | ✅ Match |
| Display Format | ✅ 8x8 pattern | ✅ 8x8 per panel | ✅ Match |
| Data Structure | ✅ 1D list | ✅ 1D list | ✅ Match |
| Virtual Environment | ✅ RQB2 | ✅ RQB2 | ✅ Match |
| LED Utilities | ✅ rq_led_utils | ✅ rq_led_utils | ✅ Match |
| Button Controls | ✅ SenseHat | ✅ SenseHat | ✅ Match |
| Desktop Launcher | ✅ Yes | ✅ Yes | ✅ Match |

## 📝 License

This project is created for educational and demonstration purposes on the RasQberry platform.

## 👥 Credits

- **RasQberry Platform:** RasQberry-Two system
- **IBM Quantum Demo:** Reference implementation (QuantumRaspberryTie)
- **LED Utilities:** rq_led_utils for layout-aware mapping
- **Libraries:** Adafruit NeoPixel, CircuitPython, Blinka

## 📧 Support

For issues or questions:
1. Check [SAP_LED_DEMO_SOLUTION.md](SAP_LED_DEMO_SOLUTION.md) for detailed troubleshooting
2. Verify hardware connections
3. Ensure RQB2 virtual environment is active
4. Run with sudo for GPIO access

## 🎯 Quick Commands

```bash
# Clear LEDs
sudo /usr/bin/rq_clear_leds.sh

# Run demo
sudo /home/rasqberry/rq_sap_led_demo.sh

# Kill running demo
sudo pkill -9 -f led_sap_demo.py

# Check if demo is running
ps aux | grep led_sap_demo
```

---

**Status:** ✅ Fully functional and tested on RasQberry Two hardware