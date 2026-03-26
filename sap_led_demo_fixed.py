#!/usr/bin/env python3
"""
LED SAP Demo - Fixed Pattern Version
Displays "SAP" correctly on 8x8 LED matrix
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

# Configuration - using 8x8 display like IBM demo
DISPLAY_WIDTH = 8
DISPLAY_HEIGHT = 8
TOTAL_PIXELS = 64  # 8x8 = 64 pixels for display
TOTAL_LEDS = 192   # Physical LEDs on strip

# Color definitions (RGB tuples)
B = [0, 112, 242]    # SAP Blue
G = [240, 171, 0]    # SAP Gold
O = [0, 0, 0]        # Off/Black

# Global variables
neopixel_array = None
sense_hat = None
LED_array_indices = None

# SAP Pattern on 8x8 grid - each letter is roughly 2 columns wide
# Layout: S (cols 0-1), A (cols 3-4), P (cols 6-7)
SAP_Pattern = [
    # Row 0
    B, B, O, G, G, O, B, B,
    # Row 1
    B, O, O, G, O, G, B, O,
    # Row 2
    B, B, O, G, G, O, B, B,
    # Row 3
    O, B, O, G, O, G, B, O,
    # Row 4
    B, B, O, G, O, G, B, B,
    # Row 5
    O, O, O, O, O, O, B, O,
    # Row 6
    O, O, O, O, O, O, B, O,
    # Row 7
    O, O, O, O, O, O, O, O,
]


def load_led_config():
    """Load LED configuration from RasQberry environment file"""
    env_file = "/usr/config/rasqberry_environment.env"
    config = {}

    if os.path.exists(env_file):
        print(f"Loading LED config from {env_file}")
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

    print(
        f"LED Config: {num_pixels} LEDs on GPIO{gpio_pin}, order={pixel_order_str}, brightness={brightness}")

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
            LED_array_indices = generate_led_indices()
        else:
            LED_array_indices = {i: i for i in range(num_pixels)}

        return True

    except Exception as e:
        print(f"✗ Error initializing NeoPixel: {e}")
        UseNeo = False
        return False


def generate_led_indices():
    """Generate LED indices using RasQberry utilities"""
    try:
        led_config = get_led_config()
        width = led_config['matrix_width']
        height = led_config['matrix_height']

        print(f"LED matrix config: {width}x{height}")

        # Calculate starting position to center 8x8 display on matrix
        start_x = (width - 8) // 2
        start_y = (height - 8) // 2

        indices = {}
        for display_idx in range(64):
            row = display_idx // 8
            col = display_idx % 8

            # Map display position to LED matrix position
            led_x = start_x + col
            led_y = start_y + row

            pixel_idx = map_xy_to_pixel(led_x, led_y)
            if pixel_idx is not None:
                indices[display_idx] = pixel_idx
            else:
                indices[display_idx] = 0

        print(f"✓ Generated {len(indices)} LED index mappings")
        return indices

    except Exception as e:
        print(f"✗ Error generating LED indices: {e}")
        return {i: i for i in range(TOTAL_LEDS)}


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
    """Display pixel list to physical LEDs (EXACTLY like IBM demo)"""
    global neopixel_array

    if not UseNeo or neopixel_array is None:
        return

    try:
        if clear_first:
            neopixel_array.fill((0, 0, 0))

        for index, pixel in enumerate(pixel_list):
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
    """Draw SAP on 8x8 display"""
    # Create pixel list
    if rainbow:
        pixels = [get_rainbow_color(i // 8, 8, hue_offset) if SAP_Pattern[i] != O else O[:]
                  for i in range(TOTAL_PIXELS)]
    else:
        pixels = [SAP_Pattern[i][:] for i in range(TOTAL_PIXELS)]

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
    print("SAP LED Demo - Fixed Pattern Version")
    print("Displays SAP on 8x8 LED matrix")
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
    print("SAP displayed on LEDs!")

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
