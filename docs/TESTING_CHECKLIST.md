# Testing Checklist for SAP LED Demo

Use this checklist to verify the demo works correctly after deployment to RasQberry.

---

## Pre-Deployment Tests (Local)

Run these tests before deploying to RasQberry:

- [ ] **Python Syntax Check**
  ```bash
  python3 -m py_compile src/sap_led_demo.py
  python3 -m py_compile src/sap_quantum_led_demo.py
  ```

- [ ] **Script Permissions**
  ```bash
  test -x scripts/deploy_to_rasqberry.sh && echo "OK" || echo "FAIL"
  test -x scripts/rq_led_sap_demo.sh && echo "OK" || echo "FAIL"
  test -x scripts/install_desktop_icon.sh && echo "OK" || echo "FAIL"
  ```

- [ ] **Required Files Present**
  ```bash
  test -f src/sap_led_demo.py && echo "✓ Main demo"
  test -f scripts/rq_led_sap_demo.sh && echo "✓ Launcher"
  test -f desktop/sap-led-demo.desktop && echo "✓ Desktop icon"
  test -f docs/DEPLOYMENT_GUIDE.md && echo "✓ Documentation"
  ```

---

## Deployment Tests

- [ ] **Connection Test**
  ```bash
  ssh rasqberry@YOUR_IP "echo 'Connection OK'"
  ```

- [ ] **Run Deployment Script**
  ```bash
  ./scripts/deploy_to_rasqberry.sh YOUR_IP
  ```
  
  Expected output:
  - [SUCCESS] Connection established
  - [SUCCESS] Main demo deployed
  - [SUCCESS] Launcher script deployed
  - [SUCCESS] Desktop icon installed
  - [SUCCESS] Deployment Complete!

---

## Post-Deployment Verification

### 1. File Existence Tests

SSH into RasQberry and verify files:

```bash
ssh rasqberry@YOUR_IP
```

- [ ] **Main Demo**
  ```bash
  ls -la /home/rasqberry/led_sap_demo.py
  ```
  Expected: File exists, executable permissions

- [ ] **Launcher Script**
  ```bash
  ls -la /usr/bin/rq_led_sap_demo.sh
  ```
  Expected: File exists, executable permissions

- [ ] **Desktop Icon**
  ```bash
  ls -la /home/rasqberry/Desktop/sap-led-demo.desktop
  ```
  Expected: File exists, executable permissions

- [ ] **Quantum Version**
  ```bash
  ls -la /home/rasqberry/sap_quantum_led_demo.py
  ```
  Expected: File exists, executable permissions

### 2. Python Syntax Verification

- [ ] **Check Main Demo Syntax**
  ```bash
  /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 -m py_compile /home/rasqberry/led_sap_demo.py
  echo $?  # Should be 0
  ```

### 3. Desktop Icon Test

- [ ] **Visual Check**
  - Look at RasQberry desktop
  - Verify "SAP LED Demo" icon is visible
  - Icon should have RasQberry logo

- [ ] **Desktop File Validation**
  ```bash
  cat /home/rasqberry/Desktop/sap-led-demo.desktop
  ```
  Expected: Contains `Exec=sudo /usr/bin/rq_led_sap_demo.sh`

### 4. Functional Tests

#### Test 1: Launch from Desktop Icon

- [ ] Double-click "SAP LED Demo" icon on desktop
- [ ] Terminal window opens
- [ ] Demo starts without errors
- [ ] "SAP" text appears on LED matrix
- [ ] Text is correctly oriented (not upside down or mirrored)

#### Test 2: Launch from Command Line

- [ ] Run: `sudo /usr/bin/rq_led_sap_demo.sh`
- [ ] Demo starts without errors
- [ ] "SAP" text displays correctly

#### Test 3: Joystick Controls (if available)

- [ ] Press UP button → Text changes to blue
- [ ] Press DOWN button → Text changes to red
- [ ] Press LEFT button → Text changes to green
- [ ] Press RIGHT button → Text changes to yellow
- [ ] Press PUSH button → Text shows rainbow colors

#### Test 4: Auto-Cycle Mode (if no joystick)

- [ ] Demo automatically cycles through colors
- [ ] Colors change every few seconds
- [ ] No errors in terminal

#### Test 5: Virtual Display Sync

- [ ] Check virtual LED display window
- [ ] Text matches physical LEDs
- [ ] Orientation is correct
- [ ] Colors match

#### Test 6: Clean Exit

- [ ] Press Ctrl+C
- [ ] Demo exits cleanly
- [ ] No error messages
- [ ] LEDs turn off

### 5. Quantum Version Test (Optional)

- [ ] Run: `sudo PYTHONPATH=/usr/bin /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 /home/rasqberry/sap_quantum_led_demo.py`
- [ ] Quantum circuits execute without errors
- [ ] Colors are generated via quantum measurement
- [ ] Demo runs smoothly

---

## Isolation Tests

Verify other demos are not affected:

- [ ] **IBM Demo Still Works**
  ```bash
  sudo /usr/bin/rq_led_ibm_demo.sh
  ```
  Expected: IBM demo runs normally

- [ ] **Other Desktop Icons Present**
  ```bash
  ls /home/rasqberry/Desktop/
  ```
  Expected: All original icons still present

- [ ] **Configuration Unchanged**
  ```bash
  cat /usr/config/rasqberry_environment.env | grep LED
  ```
  Expected: LED configuration unchanged

---

## Performance Tests

- [ ] **Startup Time**
  - Demo starts within 5 seconds
  
- [ ] **Response Time**
  - Joystick button press → color change < 1 second
  
- [ ] **CPU Usage**
  ```bash
  top -b -n 1 | grep python3
  ```
  Expected: Reasonable CPU usage (< 50%)

- [ ] **Memory Usage**
  ```bash
  ps aux | grep led_sap_demo
  ```
  Expected: < 100MB memory

---

## Rollback Test

- [ ] **Restore Backup**
  ```bash
  cp /home/rasqberry/led_sap_demo.py.backup /home/rasqberry/led_sap_demo.py
  ```
  Expected: Previous version restored successfully

- [ ] **Remove Desktop Icon**
  ```bash
  rm /home/rasqberry/Desktop/sap-led-demo.desktop
  ```
  Expected: Icon removed from desktop

---

## Final Checklist

- [ ] All files deployed correctly
- [ ] Desktop icon visible and functional
- [ ] Demo launches from icon
- [ ] Demo launches from command line
- [ ] Text displays correctly on LEDs
- [ ] Joystick controls work (if available)
- [ ] Virtual display synchronized
- [ ] Other demos unaffected
- [ ] Clean exit works
- [ ] No error messages

---

## Issue Reporting

If any test fails, document:

1. **Which test failed**
2. **Error message (if any)**
3. **Expected vs actual behavior**
4. **Screenshots (if applicable)**
5. **System information**:
   ```bash
   uname -a
   python3 --version
   cat /usr/config/rasqberry_environment.env
   ```

Report issues at: https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED/issues

---

**Testing Complete!** ✅

If all tests pass, the deployment is successful and the demo is ready for use.