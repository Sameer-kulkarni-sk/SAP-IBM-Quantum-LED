#!/usr/bin/env python3
"""
SAP Quantum LED Demo

This module displays the "SAP" logo on a 24x8 LED matrix with quantum-powered
color selection using Qiskit. It demonstrates quantum computing concepts by
using quantum circuits to generate truly random colors.

Features:
    - Quantum random color selection from predefined palette
    - Quantum RGB color generation using superposition
    - Interactive joystick control
    - Automatic quantum color cycling in demo mode
    - Fallback to pseudo-random when Qiskit unavailable

Quantum Mechanics:
    - Uses 3-qubit circuits for 8-color palette selection
    - Uses 8-qubit circuits for full RGB generation
    - Hadamard gates create quantum superposition
    - Measurement collapses to truly random values

Requirements:
    - RasQberry LED utilities (rq_led_utils)
    - NeoPixel LED strip
    - Qiskit and Qiskit Aer (optional, falls back to pseudo-random)
    - Optional: Sense HAT for joystick control

Usage:
    sudo python3 sap_quantum_led_demo.py

Author: SAP-IBM Quantum LED Demo Project
License: Apache 2.0
"""

from typing import Tuple, List
import sys
import os
import time

from rq_led_utils import get_led_config, create_neopixel_strip, map_xy_to_pixel

# Add RQB2-bin to path for imports
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

# Color definitions (R, G, B) tuples
COLOR_BLUE: Tuple[int, int, int] = (0, 0, 255)
COLOR_RED: Tuple[int, int, int] = (255, 0, 0)
COLOR_GREEN: Tuple[int, int, int] = (0, 255, 0)
COLOR_YELLOW: Tuple[int, int, int] = (255, 255, 0)
COLOR_CYAN: Tuple[int, int, int] = (0, 255, 255)
COLOR_MAGENTA: Tuple[int, int, int] = (255, 0, 255)
COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
COLOR_ORANGE: Tuple[int, int, int] = (255, 165, 0)
COLOR_OFF: Tuple[int, int, int] = (0, 0, 0)

# Predefined color palette for quantum selection (8 colors for 3-qubit circuit)
COLORS: List[Tuple[int, int, int]] = [
    COLOR_BLUE, COLOR_RED, COLOR_GREEN, COLOR_YELLOW,
    COLOR_CYAN, COLOR_MAGENTA, COLOR_ORANGE, COLOR_WHITE
]

# Rainbow gradient colors for each row (y-coordinate)
RAINBOW_COLORS: dict[int, Tuple[int, int, int]] = {
    7: (251, 128, 191),  # pink
    6: (250, 1, 0),      # red
    5: (249, 131, 31),   # orange
    4: (248, 223, 8),    # yellow
    3: (2, 162, 4),      # green
    2: (0, 196, 173),    # turquoise
    1: (0, 65, 183),     # blue
    0: (131, 32, 158),   # purple
}


def plotcalc(
    y: int,
    x: int,
    color: Tuple[int, int, int],
    pixels,
    rainbow: bool = False
) -> None:
    """
    Set LED color at specified matrix coordinates.

    This function maps 2D matrix coordinates to the physical LED strip index
    and sets the color. Supports rainbow gradient mode where colors are
    determined by the y-coordinate.

    Args:
        y: Row index (0-7, where 0 is bottom and 7 is top)
        x: Column index (0-23, left to right)
        color: RGB color tuple (R, G, B) with values 0-255
        pixels: NeoPixel strip object to control LEDs
        rainbow: If True, use rainbow gradient colors based on y-coordinate,
                ignoring the color parameter

    Returns:
        None

    Note:
        - Uses map_xy_to_pixel() which handles layout configuration
        - Y-flip is handled automatically based on LED_MATRIX_Y_FLIP config
        - Out-of-bounds coordinates are silently ignored
    """
    pixel_index = map_xy_to_pixel(x, y)

    if pixel_index is None:
        return

    if rainbow:
        color = RAINBOW_COLORS.get(y, color)

    pixels[pixel_index] = color


def clear_display(pixels, config: dict) -> None:
    """
    Clear all LEDs by setting them to off.

    Args:
        pixels: NeoPixel strip object
        config: LED configuration dictionary containing 'led_count'

    Returns:
        None
    """
    for i in range(config['led_count']):
        pixels[i] = COLOR_OFF
    pixels.show()


def dosap(
    pixels,
    color: Tuple[int, int, int] = COLOR_BLUE,
    rainbow: bool = False
) -> None:
    """
    Draw the SAP logo on the LED matrix.

    This function renders the three letters "S", "A", and "P" on the LED
    matrix using the specified color or rainbow gradient. The logo is
    Y-flipped to match the IBM Quantum LED orientation.

    Args:
        pixels: NeoPixel strip object to control LEDs
        color: RGB color tuple for the logo (default: blue)
        rainbow: If True, use rainbow gradient instead of solid color

    Returns:
        None

    Note:
        The logo occupies approximately:
        - Letter S: columns 0-5
        - Letter A: columns 8-13
        - Letter P: columns 16-21
        - All letters span rows 0-7 (full height)
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


def quantum_color_selector() -> Tuple[int, int, int]:
    """
    Use quantum circuit to randomly select a color from the palette.

    This function creates a 3-qubit quantum circuit in superposition and
    measures it to get a truly random 3-bit number (0-7), which is used
    to select one of 8 predefined colors.

    Quantum Process:
        1. Create 3-qubit circuit (2^3 = 8 possible outcomes)
        2. Apply Hadamard gates to create equal superposition
        3. Measure all qubits
        4. Convert binary result to color index

    Returns:
        Tuple[int, int, int]: RGB color tuple selected by quantum measurement

    Fallback:
        If Qiskit is unavailable or an error occurs, falls back to
        pseudo-random selection using Python's random module.

    Example:
        >>> color = quantum_color_selector()
        >>> print(color)  # e.g., (255, 0, 0) for red
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


def quantum_rgb_generator() -> Tuple[int, int, int]:
    """
    Use quantum circuit to generate RGB color values directly.

    This function creates an 8-qubit quantum circuit to generate random
    RGB values. The 8 qubits are distributed as: 3 bits for red, 3 bits
    for green, and 2 bits for blue, then scaled to 8-bit color values.

    Quantum Process:
        1. Create 8-qubit circuit
        2. Apply Hadamard gates to all qubits (superposition)
        3. Measure all qubits
        4. Extract and scale RGB values from measurement

    Bit Distribution:
        - Qubits 0-2: Red channel (3 bits → 0-7 → scaled to 0-224)
        - Qubits 3-5: Green channel (3 bits → 0-7 → scaled to 0-224)
        - Qubits 6-7: Blue channel (2 bits → 0-3 → scaled to 0-192)

    Returns:
        Tuple[int, int, int]: Quantum-generated RGB color tuple

    Fallback:
        If Qiskit is unavailable or an error occurs, falls back to
        pseudo-random RGB generation.

    Example:
        >>> color = quantum_rgb_generator()
        >>> print(color)  # e.g., (128, 192, 64)
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


def main() -> int:
    """
    Main demo function with quantum color selection.

    This function initializes the LED matrix, detects available input methods
    (joystick or auto-cycle), and runs the interactive quantum demo loop.

    Returns:
        int: Exit code (0 for success, 1 for error)

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C to exit
    """
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
    current_color = COLOR_BLUE
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
                            dosap(pixels, COLOR_BLUE, current_rainbow)

                        elif event.direction == "right":
                            # Default blue
                            print("RIGHT - Blue SAP")
                            current_color = COLOR_BLUE
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
                dosap(pixels, COLOR_BLUE, True)
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
