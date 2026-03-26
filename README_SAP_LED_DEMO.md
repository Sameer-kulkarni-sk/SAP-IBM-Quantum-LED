# SAP LED Demo - Enhanced Version

## Overview
The SAP LED demo has been enhanced to work like the IBM Quantum LED demo with physical NeoPixel LED array support and button controls.

## Changes Made

### 1. **Physical Hardware Support**
- ✅ Added NeoPixel LED array support (8x24 tiled or 8x32 single array)
- ✅ Integrated RasQberry LED utilities for layout-aware pixel mapping
- ✅ Automatic hardware detection with graceful fallback

### 2. **Button Controls** (Multiple Options)
- ✅ **SenseHat Joystick Controls:**
  - UP: Toggle Rainbow mode
  - DOWN: Toggle Blink mode
  - LEFT/RIGHT: Toggle SAP X IBM alternating mode
  - CENTER (press): Exit program

- ✅ **GPIO Button Controls** (if SenseHat not available):
  - GPIO17: Toggle Rainbow mode
  - GPIO27: Toggle Blink mode
  - GPIO22: Toggle SAP X IBM mode
  - GPIO23: Exit program

### 3. **Display Modes**
- ✅ **Normal Mode**: Static SAP display (Blue-Gold-Blue)
- ✅ **Rainbow Mode**: Animated rainbow colors with hue rotation (like IBM demo)
- ✅ **Blink Mode**: Color cycling through 7 colors
- ✅ **SAP X IBM Mode**: Alternates between "SAP" and "IBM" text

### 4. **Key Features from IBM Demo**
- ✅ Rainbow animation with smooth hue rotation
- ✅ Hardware detection and graceful degradation
- ✅ Layout-aware LED pixel mapping
- ✅ Thread-safe display updates
- ✅ Button/joystick event handling

## File Locations on Rasqberry

```
/home/rasqberry/
├── led_sap_demo.py                    # Enhanced version (NEW)
├── led_sap_demo_enhanced.py           # Enhanced version (backup)
├── led_sap_demo_backup.py             # Original version (backup)
└── led_sap_demo_backup_20260125_*.py  # Previous backup
```

## Testing Instructions

### 1. Test on Rasqberry with Physical LEDs

```bash
# SSH into Rasqberry
ssh rasqberry@100.67.33.252

# Run the enhanced demo
python3 /home/rasqberry/led_sap_demo.py

# Or run directly
./led_sap_demo.py
```

### 2. Expected Behavior

**On Startup:**
- The program will detect available hardware (NeoPixel, SenseHat, GPIO)
- Display "SAP" in SAP colors (Blue-Gold-Blue)
- Show control instructions in console

**Button Controls:**
- Press joystick UP or Button 1: Rainbow animation starts
- Press joystick DOWN or Button 2: Color cycling blink mode
- Press joystick LEFT/RIGHT or Button 3: Alternates SAP ↔ IBM
- Press joystick CENTER or Button 4: Exit program

### 3. Hardware Requirements

**Minimum:**
- Raspberry Pi with Python 3
- NeoPixel LED array (8x24 or 8x32)
- Connected to GPIO18 (PWM0)

**Optional:**
- SenseHat for joystick controls
- GPIO buttons (GPIO17, 27, 22, 23)
- RasQberry LED utilities for optimal pixel mapping

### 4. Troubleshooting

**If LEDs don't light up:**
```bash
# Check if NeoPixel library is installed
pip3 list | grep neopixel

# Install if missing
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

# Check GPIO permissions
sudo usermod -a -G gpio rasqberry
```

**If buttons don't work:**
```bash
# Check if SenseHat is detected
python3 -c "from sense_hat import SenseHat; print('SenseHat OK')"

# Or check GPIO
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"
```

**If RasQberry utilities not found:**
- The program will use fallback pixel mapping
- LEDs will still work but may not match the tiled layout exactly

## Comparison: Original vs Enhanced

| Feature | Original SAP Demo | Enhanced SAP Demo |
|---------|------------------|-------------------|
| Display | Tkinter GUI only | Physical NeoPixel LEDs |
| Controls | Keyboard only | Joystick + GPIO buttons |
| Animation | Basic | Rainbow with hue rotation |
| Hardware | None | NeoPixel + SenseHat |
| Layout | Fixed | RasQberry-aware mapping |
| Modes | 3 modes | 4 modes (added SAP↔IBM) |

## Code Architecture

### Main Components:

1. **LEDMatrixController Class**
   - Manages LED matrix state
   - Handles hardware initialization
   - Processes button events
   - Updates physical display

2. **Hardware Detection**
   - Auto-detects NeoPixel arrays
   - Auto-detects SenseHat
   - Auto-detects GPIO buttons
   - Graceful fallback if hardware missing

3. **Display Functions**
   - `draw_sap()`: Draw SAP letters
   - `draw_sap_x_ibm()`: Alternate SAP/IBM
   - `get_rainbow_color()`: Generate rainbow colors
   - `update_display()`: Push to physical LEDs

4. **Animation Loop**
   - Checks button states
   - Updates display based on mode
   - Handles timing and transitions

## Testing Checklist

- [ ] LEDs light up on startup
- [ ] SAP letters display correctly
- [ ] Rainbow mode works (joystick UP or Button 1)
- [ ] Blink mode works (joystick DOWN or Button 2)
- [ ] SAP X IBM mode works (joystick LEFT/RIGHT or Button 3)
- [ ] Exit works (joystick CENTER or Button 4)
- [ ] Colors match SAP branding (Blue #0070F2, Gold #F0AB00)
- [ ] Smooth transitions between modes
- [ ] No crashes or errors

## Next Steps

1. **Test the enhanced demo** on the Rasqberry with physical LEDs
2. **Verify button controls** work as expected
3. **Adjust LED brightness** if needed (modify `brightness=0.3` in code)
4. **Fine-tune animations** based on visual feedback
5. **Document any issues** for further refinement

## Support

If you encounter issues:
1. Check console output for error messages
2. Verify hardware connections
3. Ensure all required libraries are installed
4. Check file permissions (`chmod +x led_sap_demo.py`)

## Files in This Repository

- `sap_led_demo_enhanced.py` - Enhanced version with hardware support
- `sap_led_demo.py` - Original Tkinter GUI version
- `ibm_led_demo.py` - IBM Quantum LED demo (reference)
- `README_SAP_LED_DEMO.md` - This documentation
- `ssh_connect.exp` - SSH connection helper script