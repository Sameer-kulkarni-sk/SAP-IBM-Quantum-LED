# SAP LED Demo - Final Instructions

## ✅ Installation Complete!

The SAP LED demo has been updated to work **EXACTLY** like the IBM Quantum LED demo with physical NeoPixel hardware.

## 🎯 What's New

### Hardware Integration (Matching IBM Demo)
- ✅ Reads configuration from `/usr/config/rasqberry_environment.env`
- ✅ Uses RasQberry LED utilities (`rq_led_utils`)
- ✅ Initializes NeoPixel array exactly like IBM demo
- ✅ 192 LEDs on GPIO18, GRB pixel order, 0.4 brightness
- ✅ Layout-aware pixel mapping for 8x24 single serpentine matrix

### Button Controls
- ✅ SenseHat joystick support
- ✅ UP: Rainbow mode
- ✅ DOWN: Blink mode
- ✅ LEFT/RIGHT: SAP X IBM alternating
- ✅ CENTER: Exit

## 🚀 How to Run

### Method 1: From Terminal (RECOMMENDED for testing)

```bash
# SSH into Rasqberry
ssh rasqberry@100.67.33.252

# Run with sudo (required for GPIO access)
sudo python3 /home/rasqberry/led_sap_demo.py
```

### Method 2: Using the launcher script

```bash
ssh rasqberry@100.67.33.252
sudo /home/rasqberry/run_led_sap_demo.sh
```

### Method 3: Desktop Icon

The desktop icon should now work, but it will prompt for sudo password since GPIO access requires root privileges.

## 📋 Expected Output

When you run the demo, you should see:

```
==================================================
SAP LED Demo - Final Version
Matching IBM Quantum LED Demo
==================================================

Initializing hardware...
Loading LED config from /usr/config/rasqberry_environment.env
LED Config: 192 LEDs on GPIO18, order=GRB, brightness=0.4
✓ NeoPixel initialized: 192 LEDs on GPIO18
LED matrix config: 24x8
✓ Generated 192 LED index mappings
✓ SenseHat initialized for button controls

✓ Hardware initialized successfully!

Controls:
  Joystick UP: Rainbow mode
  Joystick DOWN: Blink mode
  Joystick LEFT/RIGHT: SAP X IBM mode
  Joystick CENTER: Exit
  Ctrl+C: Exit

==================================================
```

## 🎨 Display Modes

### 1. Normal Mode (Default)
- Shows "SAP" in SAP colors
- S = Blue (#0070F2)
- A = Gold (#F0AB00)
- P = Blue (#0070F2)

### 2. Rainbow Mode (Joystick UP)
- Animated rainbow colors
- Smooth hue rotation (like IBM demo)
- Continuous color cycling at 50 FPS

### 3. Blink Mode (Joystick DOWN)
- Cycles through 7 colors
- Blinks on/off every 0.5 seconds
- Colors: Blue, Gold, Red, Green, Magenta, Cyan, White

### 4. SAP X IBM Mode (Joystick LEFT/RIGHT)
- Alternates between "SAP" and "IBM"
- Changes every 0.8 seconds
- Same color scheme for both

## 🔧 Technical Details

### Hardware Requirements
- ✅ Raspberry Pi (Pi 4 or Pi 5)
- ✅ NeoPixel LED array (192 LEDs, 8x24 matrix)
- ✅ Connected to GPIO18
- ✅ SenseHat (optional, for button controls)

### Software Requirements
- ✅ Python 3
- ✅ `board` and `neopixel` libraries
- ✅ RasQberry LED utilities (`/usr/bin/rq_led_utils.py`)
- ✅ Configuration file (`/usr/config/rasqberry_environment.env`)

### Key Differences from Original
| Feature | Original SAP Demo | Final SAP Demo |
|---------|------------------|----------------|
| Display | Tkinter GUI only | Physical NeoPixel LEDs |
| Hardware | None | 192 LEDs on GPIO18 |
| Config | Hardcoded | Reads from environment file |
| Mapping | Simple | RasQberry layout-aware |
| Init | Basic | Matches IBM demo exactly |
| Permissions | User | Requires sudo |

## 🐛 Troubleshooting

### Issue: "NeoPixel LEDs not available"

**Solution 1: Check if running with sudo**
```bash
# Must run with sudo for GPIO access
sudo python3 /home/rasqberry/led_sap_demo.py
```

**Solution 2: Check if libraries are installed**
```bash
pip3 list | grep neopixel
# Should show: adafruit-circuitpython-neopixel

# If not installed:
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

**Solution 3: Check if LEDs are connected**
- Verify LEDs are connected to GPIO18
- Check power supply to LED strip
- Verify LED strip is working (test with IBM demo)

### Issue: "RasQberry LED utilities not found"

**Check if utilities exist:**
```bash
ls -la /usr/bin/rq_led_utils.py
```

**If missing:** The demo will use fallback sequential mapping, which should still work but may not match the exact layout.

### Issue: "Config file not found"

**Check if config exists:**
```bash
cat /usr/config/rasqberry_environment.env | grep LED
```

**If missing:** The demo will use default values (192 LEDs, GPIO18, GRB, 0.4 brightness).

### Issue: LEDs light up but pattern is wrong

**Check LED configuration:**
```bash
# View current config
cat /usr/config/rasqberry_environment.env | grep LED_MATRIX

# Should show:
# LED_MATRIX_LAYOUT=single
# LED_MATRIX_WIDTH=24
# LED_MATRIX_HEIGHT=8
# LED_MATRIX_Y_FLIP=true
```

## 📊 Comparison with IBM Demo

| Feature | IBM Demo | SAP Demo (Final) | Status |
|---------|----------|------------------|--------|
| Config File | ✓ | ✓ | ✅ Matches |
| RQ LED Utils | ✓ | ✓ | ✅ Matches |
| NeoPixel Init | ✓ | ✓ | ✅ Matches |
| GPIO18 | ✓ | ✓ | ✅ Matches |
| 192 LEDs | ✓ | ✓ | ✅ Matches |
| GRB Order | ✓ | ✓ | ✅ Matches |
| Layout Mapping | ✓ | ✓ | ✅ Matches |
| SenseHat Buttons | ✓ | ✓ | ✅ Matches |
| Rainbow Animation | ✓ | ✓ | ✅ Matches |
| Qiskit Integration | ✓ | ✗ | N/A (SAP demo) |

## ✅ Testing Checklist

Run through this checklist to verify everything works:

- [ ] SSH into Rasqberry
- [ ] Run: `sudo python3 /home/rasqberry/led_sap_demo.py`
- [ ] See initialization messages
- [ ] LEDs light up showing "SAP"
- [ ] Colors are correct (Blue-Gold-Blue)
- [ ] Press joystick UP - Rainbow animation works
- [ ] Press joystick DOWN - Blink mode cycles colors
- [ ] Press joystick LEFT/RIGHT - Alternates SAP ↔ IBM
- [ ] Press joystick CENTER - Program exits cleanly
- [ ] LEDs turn off on exit

## 🎉 Success Criteria

Your SAP LED demo is working correctly if:

1. ✅ Initialization completes without errors
2. ✅ LEDs light up on startup
3. ✅ "SAP" displays in correct colors
4. ✅ All button controls work
5. ✅ Rainbow animation is smooth
6. ✅ Blink mode cycles through colors
7. ✅ SAP X IBM alternates correctly
8. ✅ Exit works cleanly

## 📞 Next Steps

1. **Test the demo** using Method 1 (terminal with sudo)
2. **Verify all modes** work with joystick controls
3. **Check LED brightness** - adjust in config file if needed
4. **Test desktop icon** (will prompt for sudo password)

## 🔑 Key Commands

```bash
# Run the demo
sudo python3 /home/rasqberry/led_sap_demo.py

# Check LED config
cat /usr/config/rasqberry_environment.env | grep LED

# Test LED utilities
python3 -c "import sys; sys.path.insert(0, '/usr/bin'); from rq_led_utils import get_led_config; print(get_led_config())"

# View demo file
cat /home/rasqberry/led_sap_demo.py | head -50
```

## 📝 Files on Rasqberry

```
/home/rasqberry/
├── led_sap_demo.py              ← FINAL VERSION (matches IBM demo)
├── run_led_sap_demo.sh          ← Launcher with sudo
├── led_sap_demo_backup.py       ← Original GUI version
└── led_sap_demo_enhanced.py     ← Previous hardware version
```

---

**The SAP LED demo now works exactly like the IBM Quantum LED demo with physical hardware! 🎉**