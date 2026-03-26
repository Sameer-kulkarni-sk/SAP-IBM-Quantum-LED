#!/usr/bin/env python3
"""
LED SAP Demo - Multi-Panel Version
Displays "SAP" across 4x 8x8 LED panels (32x8 total)
Each letter gets its own 8x8 panel
"""

import sys
import os
import time
import platform
from colorsys import hsv_to_rgb

# Add RasQberry utilities to path
sys.path.insert(0, '/usr/bin')

# Initialize flags
IsRPi = False
NoHat = False
UseNeo = True
HAS_NEOPIXEL = False
HAS_SENSEHAT = False
HAS_RQ_UTILS = False

# Check if running on Raspberry Pi
IsRPi = ("aarch64" in platform.processor() or 'aarch64' in platform.machine())
if not IsRPi:
    print("Not running on Raspberry Pi - LED hardware disabled")
    UseNeo = False
    NoHat = True

# Try to import RasQberry LED utilities
try:
    from rq_led_utils import get_led_config, map_xy_to_pixel
    HAS_RQ_UTILS = True
    print("✓ RasQberry LED utilities loaded")
except ImportError:
    print("✗ RasQberry LED utilities not found")
    HAS_RQ_UTILS = False

# Try to import NeoPixel
if UseNeo and IsRPi:
    print("Importing neopixel library...")
    try:
        import board
        import neopixel
        HAS_NEOPIXEL = True
        print("✓ NeoPixel library loaded")
    except Exception as e:
        print(f"✗ Error importing neopixel: {e}")
        UseNeo = False
        HAS_NEOPIXEL = False

# Try to import SenseHat
try:
    from sense_hat import SenseHat
    HAS_SENSEHAT = True
    print("✓ SenseHat library loaded")
except ImportError:
    print("✗ SenseHat not available")
    HAS_SENSEHAT = False

# Color definitions (RGB tuples)
B = [0, 112, 242]    # SAP Blue
G = [240, 171, 0]    # SAP Gold
O = [0, 0, 0]        # Off/Black

# Global variables
neopixel_array = None
sense_hat = None
LED_array_indices = None

# Letter S - 8x8 pattern (64 pixels)
Letter_S = [
    O, B, B, B, B, B, O, O,
    B, B, O, O, O, O, B, O,
    B, O, O, O, O, O, O, O,
    O, B, B, B, B, O, O, O,
    O, O, O, O, O, B, B, O,
    O, O, O, O, O, O, B, B,
    B, O, O, O, O, B, B, O,
    O, B, B, B, B, B, O, O,
]

# Letter A - 8x8 pattern (64 pixels)
Letter_A = [
    O, O, G, G, G, G, O, O,
    O, G, G, O, O, G, G, O,
    G, G, O, O, O, O, G, G,
    G, O, O, O, O, O, O, G,
    G, G, G, G, G, G, G, G,
    G, O, O, O, O, O, O, G,
    G, O, O, O, O, O, O, G,
    G, O, O, O, O, O, O, G,
]

# Letter P - 8x8 pattern (64 pixels)
Letter_P = [
    B, B, B, B, B, B, O, O,
    B, O, O, O, O, O, B, O,
    B, O, O, O, O, O, B, O,
    B, O, O, O, O, O, B, O,
    B, B, B, B, B, B, O, O,
    B, O, O, O, O, O, O, O,
    B, O, O, O, O, O, O, O,
    B, O, O, O, O, O, O, O,
]

# Blank panel - 8x8 pattern (64 pixels)
Letter_Blank = [O] * 64


def load_led_config():
    """Load LED configuration from RasQberry environment file"""
    env_file = "/usr/config/rasqberry_environment.env"
    config = {}

    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key] = value

    num_pixels = int(config.get("LED_COUNT", "192"))
    gpio_pin = int(config.get("LED_GPIO_PIN", "18"))
    pixel_order_str = config.get("LED_PIXEL_ORDER", "GRB")
    brightness = float(config.get("LED_DEFAULT_BRIGHTNESS", "0.4"))

    return num_pixels, gpio_pin, pixel_order_str, brightness


def init_neopixel():
    """Initialize NeoPixel array (matching IBM demo)"""
    global neopixel_array, LED_array_indices, UseNeo

    if not UseNeo or not HAS_NEOPIXEL:
        return False

    try:
        num_pixels, gpio_pin, pixel_order_str, brightness = load_led_config()

        PIXEL_ORDER = getattr(neopixel, pixel_order_str, neopixel.GRB)
        gpio_board_pin = getattr(board, f"D{gpio_pin}")

        neopixel_array = neopixel.NeoPixel(
            gpio_board_pin,
            num_pixels,
            pixel_order=PIXEL_ORDER,
            brightness=brightness,
            auto_write=False,
        )

        neopixel_array.fill((0, 0, 0))
        neopixel_array.show()

        print(f"✓ NeoPixel initialized: {num_pixels} LEDs on GPIO{gpio_pin}")

        if HAS_RQ_UTILS:
            LED_array_indices = generate_led_indices_multi_panel()
        else:
            LED_array_indices = {i: i for i in range(num_pixels)}

        return True

    except Exception as e:
        print(f"✗ Error initializing NeoPixel: {e}")
        UseNeo = False
        return False


def generate_led_indices_multi_panel():
    """Generate LED indices for 4x 8x8 panels displaying S-A-P-Blank"""
    try:
        led_config = get_led_config()
        width = led_config['matrix_width']
        height = led_config['matrix_height']

        print(f"LED matrix config: {width}x{height}")
        print("Mapping 4x 8x8 panels for S-A-P display")

        indices = {}

        # We have 4 panels of 8x8 each
        # Panel 0: Letter S (columns 0-7)
        # Panel 1: Letter A (columns 8-15)
        # Panel 2: Letter P (columns 16-23)
        # Panel 3: Blank (columns 24-31 if exists)

        panel_letters = [Letter_S, Letter_A, Letter_P, Letter_Blank]

        for panel_num in range(4):
            panel_start_x = panel_num * 8

            for panel_idx in range(64):
                row = panel_idx // 8
                col = panel_idx % 8

                # Calculate position in full matrix
                led_x = panel_start_x + col
                led_y = row

                # Only map if within matrix bounds
                if led_x < width and led_y < height:
                    pixel_idx = map_xy_to_pixel(led_x, led_y)
                    if pixel_idx is not None:
                        # Store mapping: display_idx -> (panel_num, panel_idx, led_idx)
                        display_idx = panel_num * 64 + panel_idx
                        indices[display_idx] = pixel_idx

        print(
            f"✓ Generated {len(indices)} LED index mappings for multi-panel display")
        return indices

    except Exception as e:
        print(f"✗ Error generating LED indices: {e}")
        return {i: i for i in range(192)}


def init_sensehat():
    """Initialize SenseHat"""
    global sense_hat

    if not HAS_SENSEHAT or not IsRPi:
        return False

    try:
        sense_hat = SenseHat()
        print("✓ SenseHat initialized")
        return True
    except Exception as e:
        print(f"✗ Error initializing SenseHat: {e}")
        return False


def display_to_LEDs(pixel_list, LED_array_indices, clear_first=False):
    """Display pixel list to physical LEDs"""
    global neopixel_array

    if not UseNeo or neopixel_array is None:
        return

    try:
        if clear_first:
            neopixel_array.fill((0, 0, 0))

        for index, pixel in enumerate(pixel_list):
            if index in LED_array_indices:
                # Get RGB data from pixel list
                red, green, blue = pixel[0], pixel[1], pixel[2]

                # Get the corresponding index position on the LED array
                LED_index = LED_array_indices[index]
                if not isinstance(LED_index, int):
                    LED_index = int(LED_index)

                # Set the appropriate pixel to the RGB value
                neopixel_array[LED_index] = (red, green, blue)

        # Display image after all pixels have been set
        neopixel_array.show()

    except Exception as e:
        print(f"Error updating LEDs: {e}")


def scale(v):
    """Scale a 0-1 float to 0-255 int"""
    return int(v * 255)


def get_rainbow_color(position, total_positions, hue_offset=0.0):
    """Get rainbow color"""
    hue = (position / total_positions + hue_offset) % 1.0
    rgb = hsv_to_rgb(hue, 1.0, 1.0)
    return [scale(rgb[0]), scale(rgb[1]), scale(rgb[2])]


def draw_sap(rainbow=False, hue_offset=0.0):
    """Draw SAP across 4 panels"""
    # Combine all 4 panels into one pixel list
    pixels = []

    for panel_num, letter in enumerate([Letter_S, Letter_A, Letter_P, Letter_Blank]):
        for pixel in letter:
            if rainbow and pixel != O:
                # Apply rainbow effect
                pixels.append(get_rainbow_color(panel_num, 4, hue_offset))
            else:
                pixels.append(pixel[:])

    # Display to LEDs
    display_to_LEDs(pixels, LED_array_indices, clear_first=True)


def check_sensehat_buttons():
    """Check SenseHat joystick"""
    if sense_hat is None:
        return None

    try:
        for event in sense_hat.stick.get_events():
            if event.action == 'pressed':
                return event.direction
    except:
        pass

    return None


def main():
    """Main program"""
    print("\n" + "="*50)
    print("SAP LED Demo - Multi-Panel Version")
    print("Displays S-A-P across 4x 8x8 LED panels")
    print("="*50 + "\n")

    # Initialize hardware
    print("Initializing hardware...")
    neo_ok = init_neopixel()
    hat_ok = init_sensehat()

    if not neo_ok:
        print("\n✗ NeoPixel LEDs not available")
        print("Please check hardware and run with sudo")
        return

    print("\n✓ Hardware initialized!")
    print("\nControls:")
    if hat_ok:
        print("  Joystick UP: Rainbow mode")
        print("  Joystick DOWN: Normal mode")
        print("  Joystick CENTER: Exit")
    print("  Ctrl+C: Exit")
    print("\n" + "="*50 + "\n")

    # Animation state
    rainbow_mode = False
    hue_offset = 0.0
    running = True

    # Initial display
    draw_sap(rainbow=False)
    print("SAP displayed across panels!")

    try:
        while running:
            # Check for button presses
            button = check_sensehat_buttons()
            if button:
                if button == 'up':
                    rainbow_mode = not rainbow_mode
                    print(f"Rainbow mode: {'ON' if rainbow_mode else 'OFF'}")
                elif button == 'down':
                    rainbow_mode = False
                    draw_sap(rainbow=False)
                    print("Normal mode")
                elif button == 'middle':
                    running = False
                    print("Exiting...")

            # Update display
            if rainbow_mode:
                hue_offset = (hue_offset + 0.01) % 1.0
                draw_sap(rainbow=True, hue_offset=hue_offset)
                time.sleep(0.02)
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        # Cleanup
        print("Cleaning up...")
        if neopixel_array:
            neopixel_array.fill((0, 0, 0))
            neopixel_array.show()
        print("Done!")


if __name__ == "__main__":
    main()
