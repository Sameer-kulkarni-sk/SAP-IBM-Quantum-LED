#!/usr/bin/env python3
"""
SAP Quantum LED Demo
Displays "SAP" text on LED matrix with quantum-powered color selection
Uses Qiskit to generate truly random colors via quantum measurements
"""

from rq_led_utils import get_led_config, create_neopixel_strip, map_xy_to_pixel
import sys
import os
import time

# Add RQB2-bin to path for imports BEFORE importing rq_led_utils
sys.path.insert(0, '/usr/bin')


# Quantum computing imports
try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer
    from qiskit_ibm_runtime.fake_provider import FakeManilaV2
    QUANTUM_AVAILABLE = True
    print("✓ Qiskit quantum computing libraries loaded")
except ImportError as e:
    QUANTUM_AVAILABLE = False
    print(f"✗ Quantum libraries not available: {e}")
    print("  Will use pseudo-random colors instead")

# Color definitions
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_cyan = (0, 255, 255)
color_magenta = (255, 0, 255)
color_white = (255, 255, 255)
color_orange = (255, 165, 0)
color_off = (0, 0, 0)

# Predefined color palette
COLORS = [color_blue, color_red, color_green, color_yellow,
          color_cyan, color_magenta, color_orange, color_white]


def plotcalc(y, x, color, pixels, rainbow=False):
    """
    Calculate pixel index using environment-configured layout.

    Args:
        y: Row index (0-7)
        x: Column index (0-23)
        color: Base color value
        pixels: NeoPixel strip object
        rainbow: If True, override color with rainbow gradient based on y
    """
    i = map_xy_to_pixel(x, y)

    if i is None:
        return

    if rainbow:
        if (y == 7):
            color = (251, 128, 191)  # pink
        if (y == 6):
            color = (250, 1, 0)      # red
        if (y == 5):
            color = (249, 131, 31)   # orange
        if (y == 4):
            color = (248, 223, 8)    # yellow
        if (y == 3):
            color = (2, 162, 4)      # green
        if (y == 2):
            color = (0, 196, 173)    # turquoise
        if (y == 1):
            color = (0, 65, 183)     # blue
        if (y == 0):
            color = (131, 32, 158)   # purple

    pixels[i] = color


def clear_display(pixels, config):
    """Clear all LEDs"""
    for i in range(config['led_count']):
        pixels[i] = color_off
    pixels.show()


def dosap(pixels, color=color_blue, rainbow=False):
    """
    Draw SAP logo on LED matrix (Y-flipped).

    Args:
        pixels: NeoPixel strip object
        color: Color to use for the text
        rainbow: If True, use rainbow gradient
    """
    # Letter "S" (Y-flipped: y=7-y, x stays same)
    plotcalc(7, 0, color, pixels, rainbow)
    plotcalc(7, 1, color, pixels, rainbow)
    plotcalc(7, 2, color, pixels, rainbow)
    plotcalc(7, 3, color, pixels, rainbow)
    plotcalc(7, 4, color, pixels, rainbow)
    plotcalc(7, 5, color, pixels, rainbow)
    plotcalc(6, 0, color, pixels, rainbow)
    plotcalc(6, 1, color, pixels, rainbow)
    plotcalc(5, 0, color, pixels, rainbow)
    plotcalc(5, 1, color, pixels, rainbow)
    plotcalc(4, 0, color, pixels, rainbow)
    plotcalc(4, 1, color, pixels, rainbow)
    plotcalc(4, 2, color, pixels, rainbow)
    plotcalc(4, 3, color, pixels, rainbow)
    plotcalc(4, 4, color, pixels, rainbow)
    plotcalc(3, 2, color, pixels, rainbow)
    plotcalc(3, 3, color, pixels, rainbow)
    plotcalc(3, 4, color, pixels, rainbow)
    plotcalc(3, 5, color, pixels, rainbow)
    plotcalc(2, 4, color, pixels, rainbow)
    plotcalc(2, 5, color, pixels, rainbow)
    plotcalc(1, 4, color, pixels, rainbow)
    plotcalc(1, 5, color, pixels, rainbow)
    plotcalc(0, 0, color, pixels, rainbow)
    plotcalc(0, 1, color, pixels, rainbow)
    plotcalc(0, 2, color, pixels, rainbow)
    plotcalc(0, 3, color, pixels, rainbow)
    plotcalc(0, 4, color, pixels, rainbow)
    plotcalc(0, 5, color, pixels, rainbow)

    # Letter "A" (Y-flipped)
    plotcalc(7, 10, color, pixels, rainbow)
    plotcalc(7, 11, color, pixels, rainbow)
    plotcalc(6, 9, color, pixels, rainbow)
    plotcalc(6, 12, color, pixels, rainbow)
    plotcalc(5, 8, color, pixels, rainbow)
    plotcalc(5, 13, color, pixels, rainbow)
    plotcalc(4, 8, color, pixels, rainbow)
    plotcalc(4, 9, color, pixels, rainbow)
    plotcalc(4, 10, color, pixels, rainbow)
    plotcalc(4, 11, color, pixels, rainbow)
    plotcalc(4, 12, color, pixels, rainbow)
    plotcalc(4, 13, color, pixels, rainbow)
    plotcalc(3, 8, color, pixels, rainbow)
    plotcalc(3, 13, color, pixels, rainbow)
    plotcalc(2, 8, color, pixels, rainbow)
    plotcalc(2, 13, color, pixels, rainbow)
    plotcalc(1, 8, color, pixels, rainbow)
    plotcalc(1, 13, color, pixels, rainbow)
    plotcalc(0, 8, color, pixels, rainbow)
    plotcalc(0, 13, color, pixels, rainbow)

    # Letter "P" (Y-flipped)
    plotcalc(7, 16, color, pixels, rainbow)
    plotcalc(7, 17, color, pixels, rainbow)
    plotcalc(7, 18, color, pixels, rainbow)
    plotcalc(7, 19, color, pixels, rainbow)
    plotcalc(7, 20, color, pixels, rainbow)
    plotcalc(6, 16, color, pixels, rainbow)
    plotcalc(6, 17, color, pixels, rainbow)
    plotcalc(6, 20, color, pixels, rainbow)
    plotcalc(6, 21, color, pixels, rainbow)
    plotcalc(5, 16, color, pixels, rainbow)
    plotcalc(5, 17, color, pixels, rainbow)
    plotcalc(5, 20, color, pixels, rainbow)
    plotcalc(5, 21, color, pixels, rainbow)
    plotcalc(4, 16, color, pixels, rainbow)
    plotcalc(4, 17, color, pixels, rainbow)
    plotcalc(4, 18, color, pixels, rainbow)
    plotcalc(4, 19, color, pixels, rainbow)
    plotcalc(4, 20, color, pixels, rainbow)
    plotcalc(3, 16, color, pixels, rainbow)
    plotcalc(3, 17, color, pixels, rainbow)
    plotcalc(2, 16, color, pixels, rainbow)
    plotcalc(2, 17, color, pixels, rainbow)
    plotcalc(1, 16, color, pixels, rainbow)
    plotcalc(1, 17, color, pixels, rainbow)
    plotcalc(0, 16, color, pixels, rainbow)
    plotcalc(0, 17, color, pixels, rainbow)


def quantum_color_selector():
    """
    Use quantum circuit to randomly select a color.
    Returns a color tuple (R, G, B).
    """
    if not QUANTUM_AVAILABLE:
        # Fallback to pseudo-random
        import random
        return random.choice(COLORS)

    try:
        # Create 3-qubit circuit for color selection (8 possible outcomes)
        qc = QuantumCircuit(3, 3)

        # Apply Hadamard gates to create superposition
        qc.h(0)  # Qubit 0
        qc.h(1)  # Qubit 1
        qc.h(2)  # Qubit 2

        # Measure all qubits
        qc.measure([0, 1, 2], [0, 1, 2])

        # Execute on local simulator
        backend = Aer.get_backend('qasm_simulator')
        job = backend.run(transpile(qc, backend), shots=1)
        result = job.result()
        counts = result.get_counts()

        # Get measurement result (e.g., "101")
        measurement = list(counts.keys())[0]

        # Convert binary measurement to color index (0-7)
        color_index = int(measurement, 2)

        return COLORS[color_index]

    except Exception as e:
        print(f"Quantum measurement error: {e}")
        import random
        return random.choice(COLORS)


def quantum_rgb_generator():
    """
    Use quantum circuit to generate RGB values directly.
    Returns a color tuple (R, G, B) with quantum-generated values.
    """
    if not QUANTUM_AVAILABLE:
        import random
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    try:
        # Create 8-qubit circuit (for 8-bit RGB: 3 bits R, 3 bits G, 2 bits B)
        qc = QuantumCircuit(8, 8)

        # Apply Hadamard gates
        for i in range(8):
            qc.h(i)

        # Measure
        qc.measure(range(8), range(8))

        # Execute
        backend = Aer.get_backend('qasm_simulator')
        job = backend.run(transpile(qc, backend), shots=1)
        result = job.result()
        counts = result.get_counts()

        # Get measurement
        measurement = list(counts.keys())[0]

        # Extract RGB values (scale 3-bit to 8-bit)
        r = int(measurement[0:3], 2) * 32  # 3 bits -> 0-7 -> 0-224
        g = int(measurement[3:6], 2) * 32  # 3 bits -> 0-7 -> 0-224
        b = int(measurement[6:8], 2) * 64  # 2 bits -> 0-3 -> 0-192

        return (r, g, b)

    except Exception as e:
        print(f"Quantum RGB generation error: {e}")
        import random
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def main():
    """Main demo function with quantum color selection."""
    print("=" * 70)
    print("SAP Quantum LED Demo")
    print("=" * 70)

    # Get LED configuration
    config = get_led_config()
    print(f"Matrix: {config['matrix_width']}x{config['matrix_height']}")
    print(f"Layout: {config['layout']}")
    print(f"Total LEDs: {config['led_count']}")

    if QUANTUM_AVAILABLE:
        print("Quantum Mode: ENABLED (using Qiskit)")
    else:
        print("Quantum Mode: DISABLED (using pseudo-random)")
    print()

    # Create NeoPixel strip
    try:
        pixels = create_neopixel_strip(
            config['led_count'],
            config['pixel_order'],
            brightness=config['led_default_brightness'],
            gpio_pin=config['led_gpio_pin']
        )
        print("✓ NeoPixel strip created successfully")
    except Exception as e:
        print(f"✗ Error creating NeoPixel strip: {e}")
        print("  Make sure to run with sudo!")
        return 1

    # Try to import joystick
    try:
        from sense_hat import SenseHat
        sense = SenseHat()
        joystick_available = True
        print("✓ Joystick available")
    except:
        joystick_available = False
        print("✗ Joystick not available (running in auto mode)")

    print()
    print("Controls:")
    if joystick_available:
        print("  UP    - New quantum color (palette)")
        print("  DOWN  - New quantum RGB color")
        print("  LEFT  - Rainbow SAP")
        print("  RIGHT - Blue SAP (default)")
        print("  PUSH  - Cycle through preset colors")
    print("  Ctrl+C - Exit")
    print()

    if QUANTUM_AVAILABLE:
        print("Quantum Info:")
        print("  - Using 3-qubit circuit for color selection")
        print("  - Hadamard gates create superposition")
        print("  - Measurement collapses to random color")
        print("  - True quantum randomness!")
    print()
    print("Starting demo...")
    print()

    # Current state
    current_color = color_blue
    current_rainbow = False
    color_cycle_index = 0

    try:
        if joystick_available:
            # Joystick control mode
            print("Waiting for joystick input...")

            # Show initial display
            clear_display(pixels, config)
            dosap(pixels, current_color, current_rainbow)
            pixels.show()

            while True:
                for event in sense.stick.get_events():
                    if event.action == "pressed":
                        clear_display(pixels, config)

                        if event.direction == "up":
                            # Quantum color from palette
                            current_color = quantum_color_selector()
                            current_rainbow = False
                            print(f"UP - Quantum color: {current_color}")
                            dosap(pixels, current_color, current_rainbow)

                        elif event.direction == "down":
                            # Quantum RGB generation
                            current_color = quantum_rgb_generator()
                            current_rainbow = False
                            print(f"DOWN - Quantum RGB: {current_color}")
                            dosap(pixels, current_color, current_rainbow)

                        elif event.direction == "left":
                            # Rainbow
                            print("LEFT - Rainbow SAP")
                            current_rainbow = True
                            dosap(pixels, color_blue, current_rainbow)

                        elif event.direction == "right":
                            # Default blue
                            print("RIGHT - Blue SAP")
                            current_color = color_blue
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)

                        elif event.direction == "middle":
                            # Cycle through preset colors
                            current_color = COLORS[color_cycle_index]
                            color_cycle_index = (
                                color_cycle_index + 1) % len(COLORS)
                            current_rainbow = False
                            print(f"PUSH - Preset color: {current_color}")
                            dosap(pixels, current_color, current_rainbow)

                        pixels.show()

                time.sleep(0.1)
        else:
            # Auto-cycle mode with quantum colors
            print("Auto-cycling with quantum colors...")

            while True:
                # Quantum color from palette
                print("Quantum color selection...")
                color = quantum_color_selector()
                clear_display(pixels, config)
                dosap(pixels, color, False)
                pixels.show()
                time.sleep(3.0)

                # Quantum RGB
                print("Quantum RGB generation...")
                color = quantum_rgb_generator()
                clear_display(pixels, config)
                dosap(pixels, color, False)
                pixels.show()
                time.sleep(3.0)

                # Rainbow
                print("Rainbow mode...")
                clear_display(pixels, config)
                dosap(pixels, color_blue, True)
                pixels.show()
                time.sleep(3.0)

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    finally:
        # Clear all LEDs
        print("Clearing LEDs...")
        clear_display(pixels, config)
        print("Done!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
