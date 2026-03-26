#!/usr/bin/env python3
"""
LED SAP Demo - Final Version
Matches IBM Quantum LED demo initialization and hardware handling
Uses RasQberry configuration and LED utilities
"""

import sys
import os
import time
import platform
from colorsys import hsv_to_rgb
from threading import Thread

# Add RasQberry utilities to path
sys.path.insert(0, '/usr/bin')

# Initialize flags
IsRPi = False
NoHat = False
UseNeo = True
NeoTiled = False  # Using single 8x24 array, not tiled
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

# Try to import SenseHat for button controls
try:
    from sense_hat import SenseHat
    HAS_SENSEHAT = True
    print("✓ SenseHat library loaded")
except ImportError:
    print("✗ SenseHat not available")
    HAS_SENSEHAT = False

# Configuration
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 24
TOTAL_LEDS = 192

# SAP Colors (RGB tuples)
COLOR_SAP_BLUE = (0, 112, 242)
COLOR_SAP_GOLD = (240, 171, 0)
COLOR_OFF = (0, 0, 0)

COLOR_CYCLE = [
    COLOR_SAP_BLUE,
    COLOR_SAP_GOLD,
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 255),  # White
]

# Global variables
neopixel_array = None
sense_hat = None
LED_array_indices = None
pixels = [[COLOR_OFF for _ in range(MATRIX_WIDTH)]
          for _ in range(MATRIX_HEIGHT)]


def load_led_config():
    """Load LED configuration from RasQberry environment file (like IBM demo)"""
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
    else:
        print(f"Config file not found: {env_file}, using defaults")

    # Extract configuration (matching IBM demo approach)
    num_pixels = int(config.get("LED_COUNT", "192"))
    gpio_pin = int(config.get("LED_GPIO_PIN", "18"))
    pixel_order_str = config.get("LED_PIXEL_ORDER", "GRB")
    brightness = float(config.get("LED_DEFAULT_BRIGHTNESS", "0.4"))

    print(
        f"LED Config: {num_pixels} LEDs on GPIO{gpio_pin}, order={pixel_order_str}, brightness={brightness}")

    return num_pixels, gpio_pin, pixel_order_str, brightness


def init_neopixel():
    """Initialize NeoPixel array (matching IBM demo initialization)"""
    global neopixel_array, LED_array_indices, UseNeo

    if not UseNeo or not HAS_NEOPIXEL:
        return False

    try:
        # Load configuration from environment file
        num_pixels, gpio_pin, pixel_order_str, brightness = load_led_config()

        # Get pixel order attribute
        PIXEL_ORDER = getattr(neopixel, pixel_order_str, neopixel.GRB)

        # Get GPIO pin
        gpio_board_pin = getattr(board, f"D{gpio_pin}")

        # Initialize NeoPixel array (exactly like IBM demo)
        neopixel_array = neopixel.NeoPixel(
            gpio_board_pin,
            num_pixels,
            pixel_order=PIXEL_ORDER,
            brightness=brightness,
            auto_write=False,
        )

        # Initialize all pixels to black
        neopixel_array.fill((0, 0, 0))
        neopixel_array.show()

        print(f"✓ NeoPixel initialized: {num_pixels} LEDs on GPIO{gpio_pin}")

        # Generate LED indices mapping
        if HAS_RQ_UTILS:
            LED_array_indices = generate_led_indices()
        else:
            # Fallback: simple sequential mapping
            LED_array_indices = {i: i for i in range(num_pixels)}

        return True

    except Exception as e:
        print(f"✗ Error initializing NeoPixel: {e}")
        UseNeo = False
        return False


def generate_led_indices():
    """Generate LED indices using RasQberry utilities (like IBM demo)"""
    try:
        led_config = get_led_config()
        width = led_config['matrix_width']
        height = led_config['matrix_height']

        print(f"LED matrix config: {width}x{height}")

        indices = {}
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                display_idx = row * MATRIX_WIDTH + col
                pixel_idx = map_xy_to_pixel(col, row)
                if pixel_idx is not None:
                    indices[display_idx] = pixel_idx
                else:
                    indices[display_idx] = 0

        print(f"✓ Generated {len(indices)} LED index mappings")
        return indices

    except Exception as e:
        print(f"✗ Error generating LED indices: {e}")
        # Fallback to sequential mapping
        return {i: i for i in range(TOTAL_LEDS)}


def init_sensehat():
    """Initialize SenseHat for button controls"""
    global sense_hat

    if not HAS_SENSEHAT or not IsRPi:
        return False

    try:
        sense_hat = SenseHat()
        print("✓ SenseHat initialized for button controls")
        return True
    except Exception as e:
        print(f"✗ Error initializing SenseHat: {e}")
        return False


def display_to_LEDs(pixel_matrix, clear_first=False):
    """Display pixel matrix to physical LEDs (matching IBM demo function)"""
    global neopixel_array, LED_array_indices

    if not UseNeo or neopixel_array is None:
        return

    try:
        # Optional: clear entire matrix before updating
        if clear_first:
            neopixel_array.fill((0, 0, 0))

        # Map matrix to LED array
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                display_idx = row * MATRIX_WIDTH + col

                if display_idx in LED_array_indices:
                    led_idx = LED_array_indices[display_idx]

                    if 0 <= led_idx < TOTAL_LEDS:
                        color = pixel_matrix[row][col]
                        neopixel_array[led_idx] = color

        # Display image after all pixels have been set
        neopixel_array.show()

    except Exception as e:
        print(f"Error updating LEDs: {e}")


def set_pixel(row, col, color):
    """Set a single pixel color"""
    global pixels
    if 0 <= row < MATRIX_HEIGHT and 0 <= col < MATRIX_WIDTH:
        pixels[row][col] = color


def clear_matrix():
    """Clear all pixels"""
    global pixels
    for row in range(MATRIX_HEIGHT):
        for col in range(MATRIX_WIDTH):
            pixels[row][col] = COLOR_OFF


def get_rainbow_color(position, total_positions, hue_offset=0.0):
    """Get rainbow color for position with hue rotation"""
    hue = (position / total_positions + hue_offset) % 1.0
    rgb = hsv_to_rgb(hue, 1.0, 1.0)
    return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


def draw_sap(rainbow=False, hue_offset=0.0):
    """Draw SAP letters on the LED matrix"""
    clear_matrix()

    # Letter patterns (8 rows × 6 cols)
    s_orig = [[1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1]]
    a_orig = [[0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]]
    p_orig = [[1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]]

    # Rotate 90° clockwise
    s_rotated = [list(row) for row in zip(*s_orig[::-1])]
    a_rotated = [list(row) for row in zip(*a_orig[::-1])]
    p_rotated = [list(row) for row in zip(*p_orig[::-1])]

    # Draw S
    for row in range(len(s_rotated)):
        for col in range(len(s_rotated[0])):
            if s_rotated[row][col]:
                color = get_rainbow_color(
                    row, len(s_rotated), hue_offset) if rainbow else COLOR_SAP_BLUE
                set_pixel(row + 1, col, color)

    # Draw A
    for row in range(len(a_rotated)):
        for col in range(len(a_rotated[0])):
            if a_rotated[row][col]:
                color = get_rainbow_color(
                    row, len(a_rotated), hue_offset) if rainbow else COLOR_SAP_GOLD
                set_pixel(row + 9, col, color)

    # Draw P
    for row in range(len(p_rotated)):
        for col in range(len(p_rotated[0])):
            if p_rotated[row][col]:
                color = get_rainbow_color(
                    row, len(p_rotated), hue_offset) if rainbow else COLOR_SAP_BLUE
                if row + 17 < MATRIX_HEIGHT:
                    set_pixel(row + 17, col, color)

    display_to_LEDs(pixels)


def draw_sap_x_ibm(scroll_offset):
    """Draw SAP X IBM alternating"""
    clear_matrix()

    letters = {
        'S': [[1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1]],
        'A': [[0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]],
        'P': [[1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]],
        'I': [[1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0],
              [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1]],
        'B': [[1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0]],
        'M': [[1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1],
              [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]],
    }

    letter_set = ['S', 'A', 'P'] if scroll_offset % 2 == 0 else ['I', 'B', 'M']
    colors = [COLOR_SAP_BLUE, COLOR_SAP_GOLD, COLOR_SAP_BLUE]
    positions = [1, 9, 17]

    for idx, letter in enumerate(letter_set):
        pattern = letters[letter]
        rotated = [list(row) for row in zip(*pattern[::-1])]

        for row in range(len(rotated)):
            for col in range(len(rotated[0])):
                if rotated[row][col]:
                    if row + positions[idx] < MATRIX_HEIGHT:
                        set_pixel(row + positions[idx], col, colors[idx])

    display_to_LEDs(pixels)


def check_sensehat_buttons():
    """Check SenseHat joystick for button presses"""
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
    print("SAP LED Demo - Final Version")
    print("Matching IBM Quantum LED Demo")
    print("="*50 + "\n")

    # Initialize hardware
    print("Initializing hardware...")
    neo_ok = init_neopixel()
    hat_ok = init_sensehat()

    if not neo_ok:
        print("\n✗ NeoPixel LEDs not available")
        print("This demo requires physical LED hardware")
        print("Please check:")
        print("  1. Running on Raspberry Pi")
        print("  2. NeoPixel library installed")
        print("  3. LEDs connected to GPIO18")
        print("  4. Running with sudo for GPIO access")
        return

    print("\n✓ Hardware initialized successfully!")
    print("\nControls:")
    if hat_ok:
        print("  Joystick UP: Rainbow mode")
        print("  Joystick DOWN: Blink mode")
        print("  Joystick LEFT/RIGHT: SAP X IBM mode")
        print("  Joystick CENTER: Exit")
    print("  Ctrl+C: Exit")
    print("\n" + "="*50 + "\n")

    # Animation state
    rainbow_mode = False
    blink_mode = False
    ibm_mode = False
    blink_state = True
    color_cycle_index = 0
    scroll_offset = 0
    hue_offset = 0.0
    running = True

    # Initial display
    draw_sap(rainbow=False)

    try:
        while running:
            # Check for button presses
            button = check_sensehat_buttons()
            if button:
                if button == 'up':
                    rainbow_mode = not rainbow_mode
                    if rainbow_mode:
                        blink_mode = False
                        ibm_mode = False
                    print(f"Rainbow mode: {'ON' if rainbow_mode else 'OFF'}")
                elif button == 'down':
                    blink_mode = not blink_mode
                    if blink_mode:
                        rainbow_mode = False
                        ibm_mode = False
                        blink_state = True
                        color_cycle_index = 0
                    print(f"Blink mode: {'ON' if blink_mode else 'OFF'}")
                elif button in ['left', 'right']:
                    ibm_mode = not ibm_mode
                    if ibm_mode:
                        rainbow_mode = False
                        blink_mode = False
                        scroll_offset = 0
                    print(f"SAP X IBM mode: {'ON' if ibm_mode else 'OFF'}")
                elif button == 'middle':
                    running = False
                    print("Exiting...")

            # Update display based on mode
            if rainbow_mode:
                hue_offset = (hue_offset + 0.01) % 1.0
                draw_sap(rainbow=True, hue_offset=hue_offset)
                time.sleep(0.02)
            elif blink_mode:
                if blink_state:
                    color = COLOR_CYCLE[color_cycle_index]
                    clear_matrix()
                    draw_sap(rainbow=False)
                    # Override colors with cycle color
                    for row in range(MATRIX_HEIGHT):
                        for col in range(MATRIX_WIDTH):
                            if pixels[row][col] != COLOR_OFF:
                                pixels[row][col] = color
                    display_to_LEDs(pixels)
                    color_cycle_index = (
                        color_cycle_index + 1) % len(COLOR_CYCLE)
                else:
                    clear_matrix()
                    display_to_LEDs(pixels)
                blink_state = not blink_state
                time.sleep(0.5)
            elif ibm_mode:
                draw_sap_x_ibm(scroll_offset)
                scroll_offset = (scroll_offset + 1) % 2
                time.sleep(0.8)
            else:
                draw_sap(rainbow=False)
                time.sleep(0.5)

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
