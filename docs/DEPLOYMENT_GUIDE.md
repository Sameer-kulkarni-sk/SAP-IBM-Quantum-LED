# Safe Deployment Guide for RasQberry

This guide ensures the SAP LED demo can be deployed safely without affecting other RasQberry demos or system files.

---

### Quick Deployment (Recommended)

Use the automated deployment script:

```bash
# Clone repository
git clone https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git
cd SAP-IBM-Quantum-LED

# Deploy everything (including desktop icon)
./scripts/deploy_to_rasqberry.sh YOUR_IP
```

This script will:
-  Test connection
-  Create backups
-  Deploy main demo
-  Install launcher script
-  Create desktop icon
-  Deploy quantum version
-  Verify installation


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

## Support

If you encounter issues:
1. Check the rollback procedure above
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Provide error messages and logs

---
