#!/usr/bin/env python3
# SAP LED Demo - Based on IBM LED Demo
# Displays "SAP" text on 24x8 LED matrix with rainbow toggle

import time
import sys
import select
from rq_led_utils import get_led_config, create_neopixel_strip, chunked_show, map_xy_to_pixel

# Load configuration from environment file
config = get_led_config()

# Color definitions - using (R, G, B) tuple format
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
DELAY = 5

# Create LED strip (auto-detects Pi4 PWM or Pi5 PIO)
pixels = create_neopixel_strip(
    config['led_count'],
    config['pixel_order'],
    brightness=config['led_default_brightness']
)


def plotcalc(y, x, color, pixels, rainbow):
    """
    Calculate pixel index using environment-configured layout (single or quad).

    Args:
        y: Row index (0-7)
        x: Column index (0-23)
        color: Base color value
        pixels: NeoPixel strip object
        rainbow: If True, override color with rainbow gradient based on y

    Note: Uses map_xy_to_pixel() which reads LED_MATRIX_LAYOUT from environment.
          Y-flip is handled in rq_led_utils based on LED_MATRIX_Y_FLIP config.
    """
    # Get pixel index from layout-aware mapping function
    i = map_xy_to_pixel(x, y)

    if i is None:
        # Out of bounds, skip
        return

    if rainbow:
        if (y == 7):
            color = (251, 128, 191)  # pink
        if (y == 6):
            color = (250, 1, 0)     # red
        if (y == 5):
            color = (249, 131, 31)  # orange
        if (y == 4):
            color = (248, 223, 8)   # yellow
        if (y == 3):
            color = (2, 162, 4)     # green
        if (y == 2):
            color = (0, 196, 173)   # turquoise
        if (y == 1):
            color = (0, 65, 183)    # blue
        if (y == 0):
            color = (131, 32, 158)  # purple

    pixels[i] = color


def dosap(toggle):
    """
    Draw SAP logo on LED matrix (Y-flipped only to match IBM orientation).

    Args:
        toggle: If True, use rainbow colors; if False, use solid colors (blue for all letters)
    """
    # Letter "S" (blue) - Y-flipped only (y=7-y, x stays same)
    plotcalc(7, 0, color_blue, pixels, toggle)
    plotcalc(7, 1, color_blue, pixels, toggle)
    plotcalc(7, 2, color_blue, pixels, toggle)
    plotcalc(7, 3, color_blue, pixels, toggle)
    plotcalc(7, 4, color_blue, pixels, toggle)
    plotcalc(7, 5, color_blue, pixels, toggle)
    plotcalc(6, 0, color_blue, pixels, toggle)
    plotcalc(6, 1, color_blue, pixels, toggle)
    plotcalc(5, 0, color_blue, pixels, toggle)
    plotcalc(5, 1, color_blue, pixels, toggle)
    plotcalc(4, 0, color_blue, pixels, toggle)
    plotcalc(4, 1, color_blue, pixels, toggle)
    plotcalc(4, 2, color_blue, pixels, toggle)
    plotcalc(4, 3, color_blue, pixels, toggle)
    plotcalc(4, 4, color_blue, pixels, toggle)
    plotcalc(3, 2, color_blue, pixels, toggle)
    plotcalc(3, 3, color_blue, pixels, toggle)
    plotcalc(3, 4, color_blue, pixels, toggle)
    plotcalc(3, 5, color_blue, pixels, toggle)
    plotcalc(2, 4, color_blue, pixels, toggle)
    plotcalc(2, 5, color_blue, pixels, toggle)
    plotcalc(1, 4, color_blue, pixels, toggle)
    plotcalc(1, 5, color_blue, pixels, toggle)
    plotcalc(0, 0, color_blue, pixels, toggle)
    plotcalc(0, 1, color_blue, pixels, toggle)
    plotcalc(0, 2, color_blue, pixels, toggle)
    plotcalc(0, 3, color_blue, pixels, toggle)
    plotcalc(0, 4, color_blue, pixels, toggle)
    plotcalc(0, 5, color_blue, pixels, toggle)

    # Letter "A" (blue) - Y-flipped only
    plotcalc(7, 10, color_blue, pixels, toggle)
    plotcalc(7, 11, color_blue, pixels, toggle)
    plotcalc(6, 9, color_blue, pixels, toggle)
    plotcalc(6, 12, color_blue, pixels, toggle)
    plotcalc(5, 8, color_blue, pixels, toggle)
    plotcalc(5, 13, color_blue, pixels, toggle)
    plotcalc(4, 8, color_blue, pixels, toggle)
    plotcalc(4, 9, color_blue, pixels, toggle)
    plotcalc(4, 10, color_blue, pixels, toggle)
    plotcalc(4, 11, color_blue, pixels, toggle)
    plotcalc(4, 12, color_blue, pixels, toggle)
    plotcalc(4, 13, color_blue, pixels, toggle)
    plotcalc(3, 8, color_blue, pixels, toggle)
    plotcalc(3, 13, color_blue, pixels, toggle)
    plotcalc(2, 8, color_blue, pixels, toggle)
    plotcalc(2, 13, color_blue, pixels, toggle)
    plotcalc(1, 8, color_blue, pixels, toggle)
    plotcalc(1, 13, color_blue, pixels, toggle)
    plotcalc(0, 8, color_blue, pixels, toggle)
    plotcalc(0, 13, color_blue, pixels, toggle)

    # Letter "P" (blue) - Y-flipped only
    plotcalc(7, 16, color_blue, pixels, toggle)
    plotcalc(7, 17, color_blue, pixels, toggle)
    plotcalc(7, 18, color_blue, pixels, toggle)
    plotcalc(7, 19, color_blue, pixels, toggle)
    plotcalc(7, 20, color_blue, pixels, toggle)
    plotcalc(6, 16, color_blue, pixels, toggle)
    plotcalc(6, 17, color_blue, pixels, toggle)
    plotcalc(6, 20, color_blue, pixels, toggle)
    plotcalc(6, 21, color_blue, pixels, toggle)
    plotcalc(5, 16, color_blue, pixels, toggle)
    plotcalc(5, 17, color_blue, pixels, toggle)
    plotcalc(5, 20, color_blue, pixels, toggle)
    plotcalc(5, 21, color_blue, pixels, toggle)
    plotcalc(4, 16, color_blue, pixels, toggle)
    plotcalc(4, 17, color_blue, pixels, toggle)
    plotcalc(4, 18, color_blue, pixels, toggle)
    plotcalc(4, 19, color_blue, pixels, toggle)
    plotcalc(4, 20, color_blue, pixels, toggle)
    plotcalc(3, 16, color_blue, pixels, toggle)
    plotcalc(3, 17, color_blue, pixels, toggle)
    plotcalc(2, 16, color_blue, pixels, toggle)
    plotcalc(2, 17, color_blue, pixels, toggle)
    plotcalc(1, 16, color_blue, pixels, toggle)
    plotcalc(1, 17, color_blue, pixels, toggle)
    plotcalc(0, 16, color_blue, pixels, toggle)
    plotcalc(0, 17, color_blue, pixels, toggle)


# Main loop - simple toggle between solid colors and rainbow
print("SAP LED Demo (Final - Correct Orientation)")
print("=" * 50)
print(f"Matrix: {config['matrix_width']}x{config['matrix_height']}")
print(f"Layout: {config['layout']}")
print()
print("Press Enter to stop...")
print()

try:
    while True:
        dosap(0)  # Solid blue color
        chunked_show(pixels)
        time.sleep(DELAY)
        dosap(1)  # Rainbow gradient based on rows
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
        pixels[i] = (0, 0, 0)
    pixels.show()
    print("Done!")
