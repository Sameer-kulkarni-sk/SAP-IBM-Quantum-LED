#!/usr/bin/env python3
"""
SAP LED Test Function

This module provides a simple test function for displaying the SAP logo
on a 24x8 LED matrix with automatic rainbow toggle. It's designed for
testing and validation purposes.

Features:
    - Automatic color cycling (solid blue → rainbow)
    - Non-blocking keyboard input for stopping
    - Simple test loop for validation

Requirements:
    - RasQberry LED utilities (rq_led_utils)
    - NeoPixel LED strip

Usage:
    sudo python3 neopixel_spi_SAPtestFunc.py

Author: SAP-IBM Quantum LED Demo Project
License: Apache 2.0
"""

from typing import Tuple
import time
import sys
import select

from rq_led_utils import (
    get_led_config,
    create_neopixel_strip,
    chunked_show,
    map_xy_to_pixel
)

# Configuration
DELAY: int = 5  # Seconds between color changes

# Color definitions (R, G, B) tuples
COLOR_BLUE: Tuple[int, int, int] = (0, 0, 255)
COLOR_RED: Tuple[int, int, int] = (255, 0, 0)
COLOR_GREEN: Tuple[int, int, int] = (0, 255, 0)
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

# Load configuration from environment file
config = get_led_config()

# Create LED strip (auto-detects Pi4 PWM or Pi5 PIO)
pixels = create_neopixel_strip(
    config['led_count'],
    config['pixel_order'],
    brightness=config['led_default_brightness']
)


def plotcalc(
    y: int,
    x: int,
    color: Tuple[int, int, int],
    pixels,
    rainbow: bool
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


def dosap(toggle: bool) -> None:
    """
    Draw the SAP logo on the LED matrix.

    This function renders the three letters "S", "A", and "P" on the LED
    matrix using either solid blue color or rainbow gradient. The logo is
    Y-flipped to match the IBM Quantum LED orientation.

    Args:
        toggle: If True, use rainbow gradient; if False, use solid blue

    Returns:
        None

    Note:
        The logo occupies approximately:
        - Letter S: columns 0-5
        - Letter A: columns 8-13
        - Letter P: columns 16-21
        - All letters span rows 0-7 (full height)
    """
    # Letter "S" (blue) - Y-flipped only (y=7-y, x stays same)
    plotcalc(7, 0, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 1, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 2, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 3, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 5, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 0, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 1, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 0, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 1, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 0, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 1, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 2, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 3, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 2, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 3, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 5, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 5, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 5, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 0, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 1, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 2, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 3, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 4, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 5, COLOR_BLUE, pixels, toggle)

    # Letter "A" (blue) - Y-flipped only
    plotcalc(7, 10, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 11, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 9, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 12, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 13, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 9, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 10, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 11, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 12, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 13, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 13, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 13, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 13, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 8, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 13, COLOR_BLUE, pixels, toggle)

    # Letter "P" (blue) - Y-flipped only
    plotcalc(7, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 18, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 19, COLOR_BLUE, pixels, toggle)
    plotcalc(7, 20, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 20, COLOR_BLUE, pixels, toggle)
    plotcalc(6, 21, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 20, COLOR_BLUE, pixels, toggle)
    plotcalc(5, 21, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 18, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 19, COLOR_BLUE, pixels, toggle)
    plotcalc(4, 20, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(3, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(2, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(1, 17, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 16, COLOR_BLUE, pixels, toggle)
    plotcalc(0, 17, COLOR_BLUE, pixels, toggle)


def main() -> None:
    """
    Main test loop for SAP LED display.

    This function runs a simple test loop that alternates between solid blue
    and rainbow gradient displays. It supports non-blocking keyboard input
    for stopping the demo.

    Returns:
        None

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C to exit
    """
    print("SAP LED Test Function")
    print("=" * 50)
    print(f"Matrix: {config['matrix_width']}x{config['matrix_height']}")
    print(f"Layout: {config['layout']}")
    print(f"Total LEDs: {config['led_count']}")
    print()
    print("Press Enter to stop...")
    print()

    try:
        while True:
            # Solid blue color
            dosap(False)
            chunked_show(pixels)
            time.sleep(DELAY)

            # Rainbow gradient
            dosap(True)
            chunked_show(pixels)
            time.sleep(DELAY)

            # Check for Enter key press (non-blocking)
            if select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.readline()
                print("\nStopping demo...")
                break

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")

    finally:
        # Clear all LEDs
        print("Clearing LEDs...")
        for i in range(config['led_count']):
            pixels[i] = COLOR_OFF
        pixels.show()
        print("Done!")


if __name__ == '__main__':
    main()
