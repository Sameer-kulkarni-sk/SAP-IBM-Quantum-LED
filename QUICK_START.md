# SAP LED Demo - Quick Start Guide

## ✅ Installation Complete!

The SAP LED demo has been successfully updated on your Rasqberry device at **100.67.33.252**.

## 🚀 How to Run

### Method 1: Double-Click Desktop Icon (RECOMMENDED)
1. On your Rasqberry desktop, find the **"LED SAP Demo"** icon
2. Double-click it to launch
3. The app will now open with a GUI window showing the LED matrix

### Method 2: From Terminal
```bash
ssh rasqberry@100.67.33.252
python3 /home/rasqberry/led_sap_demo.py
```

### Method 3: Run Test Script
```bash
ssh rasqberry@100.67.33.252
./test_sap_led_demo.sh
```

## 🎮 Controls

### Keyboard Controls (GUI Mode)
- **R** = Toggle Rainbow mode
- **B** = Toggle Blink mode
- **I** = Toggle SAP X IBM alternating mode
- **ESC** or **Q** = Exit

### Hardware Controls (If Available)
- **SenseHat Joystick UP** (or GPIO17) = Rainbow mode
- **SenseHat Joystick DOWN** (or GPIO27) = Blink mode
- **SenseHat Joystick LEFT/RIGHT** (or GPIO22) = SAP X IBM mode
- **SenseHat Joystick CENTER** (or GPIO23) = Exit

## 🎨 Display Modes

### 1. Normal Mode (Default)
- Shows "SAP" in SAP colors
- S = Blue (#0070F2)
- A = Gold (#F0AB00)
- P = Blue (#0070F2)

### 2. Rainbow Mode (Press R)
- Animated rainbow colors
- Smooth hue rotation like IBM demo
- Continuous color cycling

### 3. Blink Mode (Press B)
- Cycles through 7 colors
- Blinks on/off every 0.5 seconds
- Colors: Blue, Gold, Red, Green, Magenta, Cyan, White

### 4. SAP X IBM Mode (Press I)
- Alternates between "SAP" and "IBM"
- Changes every 0.8 seconds
- Same color scheme for both

## 🔧 What's New

### Hybrid Mode Features
✅ **GUI Display** - Always shows visual LED matrix in window
✅ **Physical LED Support** - Automatically detects and uses NeoPixel arrays
✅ **Dual Mode** - Works with GUI + Hardware simultaneously
✅ **Button Controls** - Supports keyboard, SenseHat joystick, and GPIO buttons
✅ **Auto-Detection** - Gracefully handles missing hardware
✅ **IBM-Style Animation** - Rainbow mode matches IBM demo behavior

### Improvements Over Original
- ✅ Physical LED hardware support added
- ✅ Button/joystick controls working
- ✅ Rainbow animation with smooth transitions
- ✅ Hardware auto-detection
- ✅ Fallback to GUI if hardware unavailable
- ✅ Desktop icon now works correctly

## 📋 Troubleshooting

### Issue: Desktop icon doesn't open
**Solution:** The icon should now work! If not:
```bash
ssh rasqberry@100.67.33.252
chmod +x /home/rasqberry/run_led_sap_demo.sh
chmod +x /home/rasqberry/led_sap_demo.py
```

### Issue: GUI window doesn't appear
**Check:** Make sure you're running on the Rasqberry desktop (not SSH)
```bash
# On Rasqberry desktop terminal:
DISPLAY=:0 python3 /home/rasqberry/led_sap_demo.py
```

### Issue: Physical LEDs don't light up
**This is OK!** The hybrid version will show the GUI even if LEDs aren't connected. To enable LEDs:
1. Connect NeoPixel array to GPIO18
2. Install libraries: `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
3. Run with sudo: `sudo python3 /home/rasqberry/led_sap_demo.py`

### Issue: Buttons don't work
**This is OK!** Use keyboard controls (R, B, I, ESC) in the GUI window.

## 📁 Files on Rasqberry

```
/home/rasqberry/
├── led_sap_demo.py              ← Main app (HYBRID VERSION)
├── led_sap_demo_enhanced.py     ← Hardware-only version
├── led_sap_demo_backup.py       ← Original GUI-only version
├── run_led_sap_demo.sh          ← Launcher script (for desktop icon)
└── test_sap_led_demo.sh         ← Test/diagnostic script
```

## 🎯 Testing Checklist

- [ ] Desktop icon opens the app
- [ ] GUI window appears with LED matrix
- [ ] "SAP" displays in correct colors (Blue-Gold-Blue)
- [ ] Press R - Rainbow animation works
- [ ] Press B - Blink mode cycles colors
- [ ] Press I - Alternates between SAP and IBM
- [ ] Press ESC - App closes cleanly
- [ ] Physical LEDs work (if connected)
- [ ] Buttons work (if available)

## 💡 Tips

1. **For best results:** Run directly on Rasqberry desktop (not via SSH)
2. **For physical LEDs:** Run with `sudo` for GPIO access
3. **For testing:** Use keyboard controls - they always work
4. **For debugging:** Check console output for hardware detection messages

## 📞 Need Help?

If something doesn't work:
1. Check the console output for error messages
2. Run the test script: `./test_sap_led_demo.sh`
3. Try the original version: `python3 /home/rasqberry/led_sap_demo_backup.py`

## 🎉 Success!

Your SAP LED demo is now enhanced with:
- ✅ IBM-style rainbow animations
- ✅ Physical LED hardware support
- ✅ Button controls (keyboard + hardware)
- ✅ Hybrid GUI + Hardware mode
- ✅ Desktop icon working

**Enjoy your enhanced SAP LED demo!**