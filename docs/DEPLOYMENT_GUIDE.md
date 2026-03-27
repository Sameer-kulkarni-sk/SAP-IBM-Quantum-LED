# Safe Deployment Guide for RasQberry

This guide ensures the SAP LED demo can be deployed safely without affecting other RasQberry demos or system files.

---

## Pre-Deployment Checklist

### 1. **Backup Existing Files**

Before deploying, backup any existing files that will be modified:

```bash
# Backup existing SAP demo (if any)
ssh rasqberry@YOUR_IP "cp /home/rasqberry/led_sap_demo.py /home/rasqberry/led_sap_demo.py.backup 2>/dev/null || true"

# Backup virtual LED GUI (if applying patches)
ssh rasqberry@YOUR_IP "sudo cp /usr/bin/rq_led_virtual_gui.py /usr/bin/rq_led_virtual_gui.py.backup 2>/dev/null || true"
```

### 2. **Check System Requirements**

```bash
# Verify RasQberry environment
ssh rasqberry@YOUR_IP "ls -la /home/rasqberry/RasQberry-Two/venv/RQB2"

# Check LED configuration
ssh rasqberry@YOUR_IP "cat /usr/config/rasqberry_environment.env | grep LED"

# Verify Python version
ssh rasqberry@YOUR_IP "/home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 --version"
```

---

## Safe Deployment Steps

### Step 1: Clone Repository (Local Machine)

```bash
git clone https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git
cd SAP-IBM-Quantum-LED
```

### Step 2: Deploy Main Demo

This **only affects** `/home/rasqberry/led_sap_demo.py` - no other demos are touched.

```bash
# Copy main demo to user home directory (safe location)
scp src/sap_led_demo.py rasqberry@YOUR_IP:/home/rasqberry/led_sap_demo.py

# Set permissions
ssh rasqberry@YOUR_IP "chmod +x /home/rasqberry/led_sap_demo.py"
```

**Impact**:  Only replaces `/home/rasqberry/led_sap_demo.py`  
**Other demos**:  Not affected

### Step 3: Deploy Launcher Script (Optional)

This adds a new launcher script without modifying existing ones.

```bash
# Copy launcher to temp
scp scripts/rq_led_sap_demo.sh rasqberry@YOUR_IP:/tmp/

# Install to system (requires sudo)
ssh rasqberry@YOUR_IP "sudo cp /tmp/rq_led_sap_demo.sh /usr/bin/ && sudo chmod +x /usr/bin/rq_led_sap_demo.sh"
```

**Impact**:  Adds new file `/usr/bin/rq_led_sap_demo.sh`  
**Other scripts**:  Not affected

### Step 4: Apply Virtual Display Patches (Optional)

 **IMPORTANT**: These patches modify system files. Only apply if you need virtual display synchronization.

```bash
# Copy patches
scp patches/patch_virtual_gui.py rasqberry@YOUR_IP:/tmp/
scp patches/patch_virtual_gui_yflip.py rasqberry@YOUR_IP:/tmp/

# Apply patches (modifies /usr/bin/rq_led_virtual_gui.py)
ssh rasqberry@YOUR_IP "sudo python3 /tmp/patch_virtual_gui.py"
ssh rasqberry@YOUR_IP "sudo python3 /tmp/patch_virtual_gui_yflip.py"
```

**Impact**:  Modifies `/usr/bin/rq_led_virtual_gui.py`  
**Backup**:  Automatically created at `/usr/bin/rq_led_virtual_gui.py.backup`  
**Other demos**: Should work normally (patches improve virtual display for all demos)

### Step 5: Deploy Quantum Version (Optional)

```bash
# Copy quantum demo to user home
scp src/sap_quantum_led_demo.py rasqberry@YOUR_IP:/home/rasqberry/

# Set permissions
ssh rasqberry@YOUR_IP "chmod +x /home/rasqberry/sap_quantum_led_demo.py"
```

**Impact**: Adds new file `/home/rasqberry/sap_quantum_led_demo.py`  
**Other demos**:  Not affected

---

## Files Modified by Deployment

### User Home Directory (`/home/rasqberry/`)
-  `led_sap_demo.py` - **Replaced** (backed up first)
-  `sap_quantum_led_demo.py` - **Added** (optional)

### System Binaries (`/usr/bin/`)
-  `rq_led_sap_demo.sh` - **Added** (optional)
-  `rq_led_virtual_gui.py` - **Modified** (only if patches applied, backed up first)

### Configuration Files
- **No configuration files modified**
- `/usr/config/rasqberry_environment.env` - **Not touched**

### Other Demos
-  **IBM Quantum demos** - Not affected
-  **Other LED demos** - Not affected
-  **Quantum games** - Not affected
-  **System utilities** - Not affected

---

## Verification After Deployment

### 1. Test SAP Demo

```bash
# Test the demo
ssh rasqberry@YOUR_IP "cd /home/rasqberry && sudo PYTHONPATH=/usr/bin /home/rasqberry/RasQberry-Two/venv/RQB2/bin/python3 led_sap_demo.py"
```

**Expected**: SAP text displays correctly on LEDs

### 2. Test Other Demos

```bash
# Test IBM demo (should still work)
ssh rasqberry@YOUR_IP "sudo /usr/bin/rq_led_ibm_demo.sh"

# Test other demos from desktop icons
```

**Expected**: All other demos work normally

### 3. Check Virtual Display

```bash
# Check if virtual GUI is running
ssh rasqberry@YOUR_IP "pgrep -f rq_led_virtual_gui"
```

**Expected**: Virtual display shows correct text for all demos

---

## Rollback Procedure

If anything goes wrong, you can easily rollback:

### Rollback SAP Demo

```bash
ssh rasqberry@YOUR_IP "cp /home/rasqberry/led_sap_demo.py.backup /home/rasqberry/led_sap_demo.py"
```

### Rollback Virtual GUI Patches

```bash
ssh rasqberry@YOUR_IP "sudo cp /usr/bin/rq_led_virtual_gui.py.backup /usr/bin/rq_led_virtual_gui.py"
```

### Remove Launcher Script

```bash
ssh rasqberry@YOUR_IP "sudo rm /usr/bin/rq_led_sap_demo.sh"
```

---

## Safety Guarantees

###  What is Safe

1. **User Home Directory**: All main files go to `/home/rasqberry/` (user space)
2. **Isolated Demo**: SAP demo runs independently
3. **No Config Changes**: LED configuration not modified
4. **Automatic Backups**: System files backed up before modification
5. **Easy Rollback**: Simple restore from backups

###  What Requires Caution

1. **Virtual GUI Patches**: Modify system file (but improve all demos)
2. **Sudo Commands**: Required for system file access
3. **LED Control**: Requires GPIO access (same as other demos)

###  What is NOT Affected

1. **IBM Quantum Demos**: Completely independent
2. **Other LED Demos**: Use different files
3. **System Configuration**: No config files modified
4. **RasQberry Core**: No core system changes
5. **Other Users**: Only affects rasqberry user

---

## Testing Matrix

| Test | Expected Result | Status |
|------|----------------|--------|
| SAP Demo Launch | Displays "SAP" correctly | |
| IBM Demo Launch | Works normally | |
| Virtual Display | Shows correct text |  |
| Joystick Controls | Responds to buttons |  |
| Other Demos | Work normally |  |
| System Stability | No crashes |  |

---

## Troubleshooting

### Issue: SAP demo doesn't start

**Check**:
```bash
ssh rasqberry@YOUR_IP "ls -la /home/rasqberry/led_sap_demo.py"
```

**Fix**: Re-deploy the demo file

### Issue: Other demos affected

**Check**:
```bash
ssh rasqberry@YOUR_IP "ls -la /usr/bin/rq_led_*.sh"
```

**Fix**: Rollback virtual GUI patches if needed

### Issue: Permission errors

**Fix**: Ensure running with sudo:
```bash
sudo /usr/bin/rq_led_sap_demo.sh
```

---

## Best Practices

1. **Always backup** before deploying
2. **Test in stages** (demo first, then patches)
3. **Verify each step** before proceeding
4. **Keep backups** until confirmed working
5. **Document changes** for your team

---

## Support

If you encounter issues:
1. Check the rollback procedure above
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Provide error messages and logs

---

**Deployment is designed to be safe and non-invasive!** 