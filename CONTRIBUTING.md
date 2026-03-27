# Contributing to SAP Quantum LED Demo

Thank you for your interest in contributing to the SAP Quantum LED Demo project! This document provides guidelines for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Hardware/software environment details
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the enhancement
- Use case and benefits
- Potential implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/SAP-IBM-Quantum-LED.git
   cd SAP-IBM-Quantum-LED
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   - Test on actual RasQberry hardware if possible
   - Verify both physical LEDs and virtual display
   - Test with and without joystick

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots/videos if applicable

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise

### File Organization

```
src/          # Source code
scripts/      # Deployment scripts
patches/      # System patches
docs/         # Documentation
examples/     # Example code
```

### Testing

Before submitting:
- Test on RasQberry hardware
- Verify LED display correctness
- Check virtual display synchronization
- Test joystick controls
- Verify quantum features (if applicable)

### Documentation

- Update README.md for new features
- Add inline comments for complex code
- Create/update docs for significant changes
- Include usage examples

## Project Structure

### Core Files

- `src/sap_led_demo.py` - Main LED demo (production)
- `src/sap_quantum_led_demo.py` - Quantum-enabled version
- `src/neopixel_spi_SAPtestFunc.py` - Standalone text display

### Scripts

- `scripts/rq_led_sap_demo.sh` - Launcher script

### Patches

- `patches/patch_virtual_gui.py` - Fix virtual display mapping
- `patches/patch_virtual_gui_yflip.py` - Add Y-flip support

## Areas for Contribution

### High Priority

- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Add configuration file support
- [ ] Create installation script

### Medium Priority

- [ ] Add more color patterns
- [ ] Implement animation effects
- [ ] Add web interface
- [ ] Support for different LED layouts

### Low Priority

- [ ] Add sound effects
- [ ] Create mobile app
- [ ] Add network control
- [ ] Support for multiple displays

## Quantum Features

If contributing quantum features:
- Use Qiskit 1.0+ API
- Test with Aer simulator
- Document quantum circuits
- Explain quantum concepts in comments

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions
- Ask for clarification

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the SAP Quantum LED Demo! 🎉