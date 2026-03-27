#!/usr/bin/env python3
"""
SAP LED Demo - Integrated Version
Displays "SAP" text on 24x8 LED matrix with joystick controls
Based on IBM demo text display approach
"""

from rq_led_utils import get_led_config, create_neopixel_strip, map_xy_to_pixel
import sys
import os
import time

# Add RQB2-bin to path for imports
sys.path.insert(0, '/usr/bin')


# Color definitions
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_white = (255, 255, 255)
color_off = (0, 0, 0)


def plotcalc(y, x, color, pixels, rainbow=False):
    """
    Calculate pixel index using environment-configured layout (single or quad).

    Args:
        y: Row index (0-7)
        x: Column index (0-23)
        color: Base color value
        pixels: NeoPixel strip object
        rainbow: If True, override color with rainbow gradient based on y
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
    Draw SAP logo on LED matrix (Y-flipped to match IBM orientation).

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


def main():
    """Main demo function with joystick control."""
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

    # Current color
    current_color = color_blue
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
                            current_color = color_blue
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "down":
                            print("DOWN - Red SAP")
                            current_color = color_red
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "left":
                            print("LEFT - Green SAP")
                            current_color = color_green
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "right":
                            print("RIGHT - Yellow SAP")
                            current_color = color_yellow
                            current_rainbow = False
                            dosap(pixels, current_color, current_rainbow)
                        elif event.direction == "middle":
                            print("PUSH - Rainbow SAP")
                            current_rainbow = True
                            dosap(pixels, color_blue, current_rainbow)

                        pixels.show()

                time.sleep(0.1)
        else:
            # Auto-cycle mode (no joystick)
            print("Auto-cycling through colors...")
            colors = [
                ("Blue", color_blue, False),
                ("Rainbow", color_blue, True),
                ("Red", color_red, False),
                ("Green", color_green, False),
                ("Yellow", color_yellow, False),
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
