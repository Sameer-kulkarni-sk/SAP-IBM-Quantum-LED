#!/usr/bin/env python3
"""
SAP LED Demo - Integrated Version

This module displays the "SAP" logo on a 24x8 LED matrix with interactive
joystick controls. It supports multiple color modes and automatic cycling
when no joystick is available.

Features:
    - Interactive joystick control for color selection
    - Multiple color modes (blue, red, green, yellow, rainbow)
    - Automatic color cycling in demo mode
    - Support for both single and quad LED matrix layouts

Requirements:
    - RasQberry LED utilities (rq_led_utils)
    - NeoPixel LED strip
    - Optional: Sense HAT for joystick control

Usage:
    sudo python3 sap_led_demo.py

Author: SAP-IBM Quantum LED Demo Project
License: Apache 2.0
"""

from typing import Tuple, Optional
import sys
import os
import time

from rq_led_utils import get_led_config, create_neopixel_strip, map_xy_to_pixel

# Add RQB2-bin to path for imports
sys.path.insert(0, '/usr/bin')


# Color definitions (R, G, B) tuples
COLOR_BLUE: Tuple[int, int, int] = (0, 0, 255)
COLOR_RED: Tuple[int, int, int] = (255, 0, 0)
COLOR_GREEN: Tuple[int, int, int] = (0, 255, 0)
COLOR_YELLOW: Tuple[int, int, int] = (255, 255, 0)
COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
COLOR_OFF: Tuple[int, int, int] = (0, 0, 0)

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
    # Get pixel index from layout-aware mapping function
    pixel_index = map_xy_to_pixel(x, y)

    if pixel_index is None:
        # Out of bounds, skip silently
        return

    # Apply rainbow gradient if requested
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


def main() -> int:
    """
    Main demo function with joystick control.

    This function initializes the LED matrix, detects available input methods
    (joystick or auto-cycle), and runs the interactive demo loop.

    Returns:
        int: Exit code (0 for success, 1 for error)

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C to exit
    """
    print("=" * 70)
    print("SAP LED Demo - Integrated Version")
    print("=" * 70)

    # Get LED configuration
    config = get_led_config()
    print(f"Matrix: {config['matrix_width']}x{config['matrix_height']}")
    print(f"Layout: {config['layout']}")
    print(f"Total LEDs: {config['led_count']}")
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
        print("✗ Joystick not available (running in demo mode)")

    print()
    print("Controls:")
    if joystick_available:
        print("  UP    - Blue SAP")
        print("  DOWN  - Red SAP")
        print("  LEFT  - Green SAP")
        print("  RIGHT - Yellow SAP")
        print("  PUSH  - Rainbow SAP")
    print("  Ctrl+C - Exit")
    print()
    print("Starting demo...")
    print()

    # Current state
    current_color = COLOR_BLUE
    current_rainbow = False

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
                            print("UP - Blue SAP")
                            current_color = COLOR_BLUE
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "down":
                            print("DOWN - Red SAP")
                            current_color = COLOR_RED
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "left":
                            print("LEFT - Green SAP")
                            current_color = COLOR_GREEN
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "right":
                            print("RIGHT - Yellow SAP")
                            current_color = COLOR_YELLOW
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "middle":
                            print("PUSH - Rainbow SAP")
                            current_rainbow = True
                            dosap(pixels, COLOR_BLUE, current_rainbow)

                        pixels.show()

                time.sleep(0.1)
        else:
            # Auto-cycle mode (no joystick)
            print("Auto-cycling through colors...")
            colors = [
                ("Blue", COLOR_BLUE, False),
                ("Rainbow", COLOR_BLUE, True),
                ("Red", COLOR_RED, False),
                ("Green", COLOR_GREEN, False),
                ("Yellow", COLOR_YELLOW, False),
            ]
            idx = 0

            while True:
                name, color, rainbow = colors[idx]
                print(f"Displaying: {name} SAP")
                clear_display(pixels, config)
                dosap(pixels, color, rainbow)
                pixels.show()
                time.sleep(3.0)
                idx = (idx + 1) % len(colors)

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
