# SAP LED Demo - Testing Guide

## Quick Start

You now have an enhanced SAP LED demo that works like the IBM Quantum LED demo with physical hardware support!

### Files on Rasqberry (100.67.33.252)

```
/home/rasqberry/
├── led_sap_demo.py              ← Enhanced version (READY TO TEST)
├── led_sap_demo_enhanced.py     ← Backup of enhanced version
├── led_sap_demo_backup.py       ← Original version backup
└── test_sap_led_demo.sh         ← Test helper script
```

## Testing Steps

### Step 1: Connect to Rasqberry

```bash
ssh rasqberry@100.67.33.252
# Password: Qiskit1!
```

### Step 2: Run the Test Script (Recommended)

```bash
cd /home/rasqberry
./test_sap_led_demo.sh
```

This will:
- Check your Python version
- Verify all required libraries
- Check file permissions
- Offer to run the demo

### Step 3: Or Run Demo Directly

```bash
python3 /home/rasqberry/led_sap_demo.py
```

## What to Expect

### On Startup
```
=== SAP LED Demo Enhanced ===
Controls:
  Joystick UP: Toggle Rainbow
  Joystick DOWN: Toggle Blink
  Joystick LEFT/RIGHT: Toggle SAP X IBM
  Joystick CENTER: Exit
=============================
```

### Initial Display
- LEDs should light up showing "SAP" in:
  - **S** = SAP Blue (#0070F2)
  - **A** = SAP Gold (#F0AB00)
  - **P** = SAP Blue (#0070F2)

## Button Controls Testing

### Test 1: Rainbow Mode
**Action:** Press Joystick UP (or GPIO17 button)
**Expected:** 
- Console shows: "Rainbow mode: ON"
- LEDs animate with smooth rainbow color transitions
- Colors continuously rotate through the spectrum

### Test 2: Blink Mode
**Action:** Press Joystick DOWN (or GPIO27 button)
**Expected:**
- Console shows: "Blink mode: ON"
- LEDs cycle through 7 colors:
  1. SAP Blue
  2. SAP Gold
  3. Red
  4. Green
  5. Magenta
  6. Cyan
  7. White
- Pattern blinks on/off every 0.5 seconds

### Test 3: SAP X IBM Mode
**Action:** Press Joystick LEFT or RIGHT (or GPIO22 button)
**Expected:**
- Console shows: "SAP X IBM mode: ON"
- Display alternates between:
  - "SAP" (Blue-Gold-Blue)
  - "IBM" (Blue-Gold-Blue)
- Changes every 0.8 seconds

### Test 4: Exit
**Action:** Press Joystick CENTER (or GPIO23 button, or Ctrl+C)
**Expected:**
- Console shows: "Stopping LED controller..."
- LEDs turn off
- Program exits cleanly

## Troubleshooting

### Issue: LEDs don't light up

**Check 1: NeoPixel library**
```bash
pip3 list | grep neopixel
# If not found:
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

**Check 2: GPIO permissions**
```bash
groups | grep gpio
# If not in gpio group:
sudo usermod -a -G gpio rasqberry
# Then logout and login again
```

**Check 3: LED connection**
- Verify LEDs are connected to GPIO18 (PWM0)
- Check power supply to LED strip
- Verify LED strip is 8x24 or 8x32 configuration

### Issue: Buttons don't work

**Check 1: SenseHat**
```bash
python3 -c "from sense_hat import SenseHat; s = SenseHat(); print('SenseHat OK')"
```

**Check 2: GPIO buttons**
```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"
```

**Check 3: Button wiring**
- GPIO17 → Rainbow button
- GPIO27 → Blink button
- GPIO22 → IBM button
- GPIO23 → Exit button
- All buttons should be pull-up (connect to GND when pressed)

### Issue: Colors look wrong

**Adjust brightness:**
Edit `/home/rasqberry/led_sap_demo.py`, line ~105:
```python
brightness=0.3,  # Change this value (0.0 to 1.0)
```

**Check color order:**
Line ~107:
```python
pixel_order=neopixel.GRB  # Try RGB or BGR if colors are wrong
```

### Issue: Layout doesn't match

The program uses RasQberry LED utilities for layout-aware mapping. If the layout looks wrong:

1. Check if `/usr/bin/rq_led_utils.py` exists
2. Verify LED configuration matches your hardware
3. The program will use fallback mapping if utilities aren't found

## Comparison with IBM Demo

| Feature | IBM Demo | SAP Demo (Enhanced) | Status |
|---------|----------|---------------------|--------|
| Physical LEDs | ✓ | ✓ | ✅ Working |
| NeoPixel Support | ✓ | ✓ | ✅ Working |
| SenseHat Joystick | ✓ | ✓ | ✅ Working |
| GPIO Buttons | ✓ | ✓ | ✅ Working |
| Rainbow Animation | ✓ | ✓ | ✅ Working |
| Layout Mapping | ✓ | ✓ | ✅ Working |
| Quantum Computing | ✓ | ✗ | N/A |
| Multiple Displays | ✓ | ✗ | Future |

## Key Improvements Made

### 1. Hardware Integration
- ✅ Added NeoPixel LED array support
- ✅ Integrated RasQberry LED utilities
- ✅ Automatic hardware detection

### 2. Control System
- ✅ SenseHat joystick support
- ✅ GPIO button support
- ✅ Keyboard fallback (Ctrl+C)

### 3. Display Features
- ✅ Rainbow mode with hue rotation (like IBM demo)
- ✅ Smooth color transitions
- ✅ Multiple animation modes
- ✅ SAP X IBM alternating display

### 4. Code Quality
- ✅ Graceful hardware detection
- ✅ Fallback modes if hardware missing
- ✅ Clean error handling
- ✅ Comprehensive logging

## Next Steps

1. **Run the test script** to verify everything works
2. **Test each button** to confirm controls work
3. **Adjust brightness** if needed for your environment
4. **Document any issues** you encounter
5. **Enjoy your enhanced SAP LED demo!**

## Support Commands

### View logs while running:
```bash
python3 /home/rasqberry/led_sap_demo.py 2>&1 | tee sap_led_test.log
```

### Check hardware status:
```bash
# Check I2C devices (for SenseHat)
i2cdetect -y 1

# Check GPIO
gpio readall

# Check LED strip
ls -l /dev/spidev*
```

### Restore original version:
```bash
cp /home/rasqberry/led_sap_demo_backup.py /home/rasqberry/led_sap_demo.py
```

## Success Criteria

- [ ] LEDs light up on startup
- [ ] "SAP" displays in correct colors
- [ ] Rainbow mode works smoothly
- [ ] Blink mode cycles through colors
- [ ] SAP X IBM mode alternates correctly
- [ ] Buttons/joystick respond immediately
- [ ] Exit works cleanly
- [ ] No error messages in console

## Contact

If you need help or encounter issues, check:
1. Console output for error messages
2. Hardware connections
3. Library installations
4. File permissions

Happy testing! 🎉