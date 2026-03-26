#!/usr/bin/env python3
"""
LED SAP Demo - Enhanced Version with Physical LED Support
Displays "SAP" on physical NeoPixel LED matrix (8x24 or 8x32)
Includes button controls and rainbow animations like IBM demo
"""

import sys
import time
from colorsys import hsv_to_rgb
from threading import Thread

# Try to import RasQberry LED utilities
try:
    sys.path.insert(0, '/usr/bin')
    from rq_led_utils import get_led_config, map_xy_to_pixel
    HAS_RQ_UTILS = True
except ImportError:
    print("Warning: RasQberry LED utilities not found. Using fallback mode.")
    HAS_RQ_UTILS = False

# Try to import NeoPixel for physical LED control
try:
    import board
    import neopixel
    HAS_NEOPIXEL = True
except ImportError:
    print("Warning: NeoPixel library not found. Running in simulation mode.")
    HAS_NEOPIXEL = False

# Try to import SenseHat for button controls
try:
    from sense_hat import SenseHat
    HAS_SENSEHAT = True
except ImportError:
    print("Warning: SenseHat library not found. Button controls disabled.")
    HAS_SENSEHAT = False

# Try to import GPIO for button controls (alternative to SenseHat)
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    print("Warning: RPi.GPIO not found. GPIO button controls disabled.")
    HAS_GPIO = False

# LED Matrix Configuration
MATRIX_WIDTH = 8  # columns
MATRIX_HEIGHT = 24  # rows
TOTAL_LEDS = 192  # 8x24 = 192 LEDs

# SAP Colors
COLOR_SAP_BLUE = (0, 112, 242)  # RGB tuple
COLOR_SAP_GOLD = (240, 171, 0)
COLOR_OFF = (0, 0, 0)

# Color cycle for blinking mode
COLOR_CYCLE = [
    COLOR_SAP_BLUE,
    COLOR_SAP_GOLD,
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 255),  # White
]

# GPIO Button pins (if using physical buttons)
BUTTON_RAINBOW = 17  # GPIO17
BUTTON_BLINK = 27    # GPIO27
BUTTON_IBM = 22      # GPIO22
BUTTON_EXIT = 23     # GPIO23


class LEDMatrixController:
    def __init__(self):
        self.matrix = [[COLOR_OFF for _ in range(
            MATRIX_WIDTH)] for _ in range(MATRIX_HEIGHT)]
        self.rainbow_mode = False
        self.blink_mode = False
        self.blink_state = True
        self.color_cycle_index = 0
        self.ibm_mode = False
        self.scroll_offset = 0
        self.running = True
        self.hue_offset = 0.0

        # Initialize hardware
        self.neopixel_array = None
        self.sense_hat = None
        self.led_indices = None

        self._init_hardware()
        self._init_buttons()

    def _init_hardware(self):
        """Initialize NeoPixel LED array"""
        if HAS_NEOPIXEL:
            try:
                # Try to initialize NeoPixel array
                # Adjust pin and LED count based on your setup
                self.neopixel_array = neopixel.NeoPixel(
                    board.D18,  # GPIO18 (PWM0)
                    TOTAL_LEDS,
                    brightness=0.3,
                    auto_write=False,
                    pixel_order=neopixel.GRB
                )
                print("✓ NeoPixel array initialized successfully")

                # Generate LED indices mapping
                if HAS_RQ_UTILS:
                    self.led_indices = self._generate_led_indices()
                else:
                    self.led_indices = self._generate_fallback_indices()

            except Exception as e:
                print(f"✗ Failed to initialize NeoPixel: {e}")
                self.neopixel_array = None

        if HAS_SENSEHAT:
            try:
                self.sense_hat = SenseHat()
                print("✓ SenseHat initialized for button controls")
            except Exception as e:
                print(f"✗ Failed to initialize SenseHat: {e}")
                self.sense_hat = None

    def _init_buttons(self):
        """Initialize GPIO buttons if available"""
        if HAS_GPIO and not HAS_SENSEHAT:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(BUTTON_RAINBOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_BLINK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_IBM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_EXIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

                # Add event detection
                GPIO.add_event_detect(BUTTON_RAINBOW, GPIO.FALLING,
                                      callback=lambda x: self.toggle_rainbow(), bouncetime=300)
                GPIO.add_event_detect(BUTTON_BLINK, GPIO.FALLING,
                                      callback=lambda x: self.toggle_blink(), bouncetime=300)
                GPIO.add_event_detect(BUTTON_IBM, GPIO.FALLING,
                                      callback=lambda x: self.toggle_ibm(), bouncetime=300)
                GPIO.add_event_detect(BUTTON_EXIT, GPIO.FALLING,
                                      callback=lambda x: self.stop(), bouncetime=300)

                print("✓ GPIO buttons initialized")
            except Exception as e:
                print(f"✗ Failed to initialize GPIO buttons: {e}")

    def _generate_led_indices(self):
        """Generate LED indices using RasQberry utilities"""
        led_config = get_led_config()
        width = led_config['matrix_width']
        height = led_config['matrix_height']

        indices = {}
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                display_idx = row * MATRIX_WIDTH + col
                pixel_idx = map_xy_to_pixel(col, row)
                if pixel_idx is not None:
                    indices[display_idx] = pixel_idx
                else:
                    indices[display_idx] = 0

        return indices

    def _generate_fallback_indices(self):
        """Generate fallback LED indices for tiled layout"""
        # This is a simplified tiled layout for 8x24 matrix
        indices = {}
        for i in range(TOTAL_LEDS):
            indices[i] = i
        return indices

    def set_led(self, row, col, color):
        """Set LED color at specific position"""
        if 0 <= row < MATRIX_HEIGHT and 0 <= col < MATRIX_WIDTH:
            self.matrix[row][col] = color

    def clear_matrix(self):
        """Turn off all LEDs"""
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                self.matrix[row][col] = COLOR_OFF

    def update_display(self):
        """Update physical LED display"""
        if self.neopixel_array is None:
            return

        try:
            # Map matrix to LED array
            for row in range(MATRIX_HEIGHT):
                for col in range(MATRIX_WIDTH):
                    display_idx = row * MATRIX_WIDTH + col
                    if display_idx in self.led_indices:
                        led_idx = self.led_indices[display_idx]
                        if 0 <= led_idx < TOTAL_LEDS:
                            self.neopixel_array[led_idx] = self.matrix[row][col]

            self.neopixel_array.show()
        except Exception as e:
            print(f"Error updating display: {e}")

    def get_rainbow_color(self, position, total_positions):
        """Get rainbow color for specific position with hue rotation"""
        hue = (position / total_positions + self.hue_offset) % 1.0
        rgb = hsv_to_rgb(hue, 1.0, 1.0)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def draw_sap(self, rainbow=False):
        """Draw SAP letters on the LED matrix"""
        self.clear_matrix()

        # Letter patterns (8 rows × 6 cols)
        s_orig = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ]

        a_orig = [
            [0, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
        ]

        p_orig = [
            [1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
        ]

        # Rotate 90° clockwise
        s_rotated = [list(row) for row in zip(*s_orig[::-1])]
        a_rotated = [list(row) for row in zip(*a_orig[::-1])]
        p_rotated = [list(row) for row in zip(*p_orig[::-1])]

        # Draw S
        for row in range(len(s_rotated)):
            for col in range(len(s_rotated[0])):
                if s_rotated[row][col]:
                    if rainbow:
                        color = self.get_rainbow_color(row, len(s_rotated))
                    else:
                        color = COLOR_SAP_BLUE
                    self.set_led(row + 1, col, color)

        # Draw A
        for row in range(len(a_rotated)):
            for col in range(len(a_rotated[0])):
                if a_rotated[row][col]:
                    if rainbow:
                        color = self.get_rainbow_color(row, len(a_rotated))
                    else:
                        color = COLOR_SAP_GOLD
                    self.set_led(row + 9, col, color)

        # Draw P
        for row in range(len(p_rotated)):
            for col in range(len(p_rotated[0])):
                if p_rotated[row][col]:
                    if rainbow:
                        color = self.get_rainbow_color(row, len(p_rotated))
                    else:
                        color = COLOR_SAP_BLUE
                    if row + 17 < MATRIX_HEIGHT:
                        self.set_led(row + 17, col, color)

        self.update_display()

    def draw_sap_x_ibm(self):
        """Draw 'SAP X IBM' alternating"""
        self.clear_matrix()

        # Define all letter patterns
        letters = {
            'S': [[1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1]],
            'A': [[0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]],
            'P': [[1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]],
            'I': [[1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0],
                  [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0],
                  [0, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1]],
            'B': [[1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 0]],
            'M': [[1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],
                  [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1],
                  [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]],
        }

        # Select letters based on scroll offset
        if self.scroll_offset % 2 == 0:
            letter_set = ['S', 'A', 'P']
            colors = [COLOR_SAP_BLUE, COLOR_SAP_GOLD, COLOR_SAP_BLUE]
        else:
            letter_set = ['I', 'B', 'M']
            colors = [COLOR_SAP_BLUE, COLOR_SAP_GOLD, COLOR_SAP_BLUE]

        # Draw letters
        positions = [1, 9, 17]
        for idx, letter in enumerate(letter_set):
            pattern = letters[letter]
            rotated = [list(row) for row in zip(*pattern[::-1])]

            for row in range(len(rotated)):
                for col in range(len(rotated[0])):
                    if rotated[row][col]:
                        if row + positions[idx] < MATRIX_HEIGHT:
                            self.set_led(
                                row + positions[idx], col, colors[idx])

        self.scroll_offset = (self.scroll_offset + 1) % 2
        self.update_display()

    def toggle_rainbow(self):
        """Toggle rainbow mode"""
        self.rainbow_mode = not self.rainbow_mode
        if self.rainbow_mode:
            self.blink_mode = False
            self.ibm_mode = False
        print(f"Rainbow mode: {'ON' if self.rainbow_mode else 'OFF'}")

    def toggle_blink(self):
        """Toggle blink mode"""
        self.blink_mode = not self.blink_mode
        if self.blink_mode:
            self.rainbow_mode = False
            self.ibm_mode = False
            self.blink_state = True
            self.color_cycle_index = 0
        print(f"Blink mode: {'ON' if self.blink_mode else 'OFF'}")

    def toggle_ibm(self):
        """Toggle IBM scrolling mode"""
        self.ibm_mode = not self.ibm_mode
        if self.ibm_mode:
            self.rainbow_mode = False
            self.blink_mode = False
            self.scroll_offset = 0
        print(f"SAP X IBM mode: {'ON' if self.ibm_mode else 'OFF'}")

    def stop(self):
        """Stop the controller"""
        self.running = False
        print("Stopping LED controller...")

    def check_sensehat_buttons(self):
        """Check SenseHat joystick for button presses"""
        if self.sense_hat is None:
            return

        try:
            for event in self.sense_hat.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'up':
                        self.toggle_rainbow()
                    elif event.direction == 'down':
                        self.toggle_blink()
                    elif event.direction == 'left' or event.direction == 'right':
                        self.toggle_ibm()
                    elif event.direction == 'middle':
                        self.stop()
        except Exception as e:
            print(f"Error checking SenseHat buttons: {e}")

    def animate(self):
        """Main animation loop"""
        print("\n=== SAP LED Demo Enhanced ===")
        print("Controls:")
        if HAS_SENSEHAT:
            print("  Joystick UP: Toggle Rainbow")
            print("  Joystick DOWN: Toggle Blink")
            print("  Joystick LEFT/RIGHT: Toggle SAP X IBM")
            print("  Joystick CENTER: Exit")
        elif HAS_GPIO:
            print("  Button 1 (GPIO17): Toggle Rainbow")
            print("  Button 2 (GPIO27): Toggle Blink")
            print("  Button 3 (GPIO22): Toggle SAP X IBM")
            print("  Button 4 (GPIO23): Exit")
        else:
            print("  Press Ctrl+C to exit")
        print("=============================\n")

        try:
            while self.running:
                # Check for button presses
                self.check_sensehat_buttons()

                # Update display based on mode
                if self.rainbow_mode:
                    self.hue_offset = (self.hue_offset + 0.01) % 1.0
                    self.draw_sap(rainbow=True)
                    time.sleep(0.02)
                elif self.blink_mode:
                    if self.blink_state:
                        color = COLOR_CYCLE[self.color_cycle_index]
                        self.clear_matrix()
                        self.draw_sap(rainbow=False)
                        # Override colors with cycle color
                        for row in range(MATRIX_HEIGHT):
                            for col in range(MATRIX_WIDTH):
                                if self.matrix[row][col] != COLOR_OFF:
                                    self.matrix[row][col] = color
                        self.update_display()
                        self.color_cycle_index = (
                            self.color_cycle_index + 1) % len(COLOR_CYCLE)
                    else:
                        self.clear_matrix()
                        self.update_display()
                    self.blink_state = not self.blink_state
                    time.sleep(0.5)
                elif self.ibm_mode:
                    self.draw_sap_x_ibm()
                    time.sleep(0.8)
                else:
                    self.draw_sap(rainbow=False)
                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        print("Cleaning up...")
        if self.neopixel_array:
            self.neopixel_array.fill(COLOR_OFF)
            self.neopixel_array.show()
        if HAS_GPIO:
            GPIO.cleanup()
        print("Done!")


def main():
    controller = LEDMatrixController()
    controller.animate()


if __name__ == "__main__":
    main()
