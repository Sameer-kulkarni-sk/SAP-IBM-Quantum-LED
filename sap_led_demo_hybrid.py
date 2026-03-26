#!/usr/bin/env python3
"""
LED SAP Demo - Hybrid Version
Works with both physical NeoPixel LEDs AND Tkinter GUI
Automatically detects hardware and uses best available option
"""

import sys
import time
from colorsys import hsv_to_rgb
import tkinter as tk
from tkinter import Canvas

# Try to import hardware libraries
try:
    sys.path.insert(0, '/usr/bin')
    from rq_led_utils import get_led_config, map_xy_to_pixel
    HAS_RQ_UTILS = True
except ImportError:
    HAS_RQ_UTILS = False

try:
    import board
    import neopixel
    HAS_NEOPIXEL = True
except ImportError:
    HAS_NEOPIXEL = False

try:
    from sense_hat import SenseHat
    HAS_SENSEHAT = True
except ImportError:
    HAS_SENSEHAT = False

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False

# Configuration
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 24
TOTAL_LEDS = 192
LED_SIZE = 40
LED_SPACING = 5

# Colors
COLOR_SAP_BLUE = (0, 112, 242)
COLOR_SAP_GOLD = (240, 171, 0)
COLOR_OFF = (0, 0, 0)

COLOR_CYCLE = [
    COLOR_SAP_BLUE,
    COLOR_SAP_GOLD,
    (255, 0, 0),
    (0, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

# GPIO pins
BUTTON_RAINBOW = 17
BUTTON_BLINK = 27
BUTTON_IBM = 22
BUTTON_EXIT = 23


class LEDMatrixHybrid:
    def __init__(self, use_gui=True):
        self.use_gui = use_gui
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

        # Hardware components
        self.neopixel_array = None
        self.sense_hat = None
        self.led_indices = None

        # GUI components
        self.root = None
        self.canvas = None
        self.leds_gui = []
        self.info_label = None

        # Initialize
        self._init_hardware()
        if self.use_gui:
            self._init_gui()
        self._init_buttons()

        print(f"Mode: {'GUI + Hardware' if self.use_gui and self.neopixel_array else 'GUI Only' if self.use_gui else 'Hardware Only'}")

    def _init_hardware(self):
        """Initialize NeoPixel hardware"""
        if HAS_NEOPIXEL:
            try:
                self.neopixel_array = neopixel.NeoPixel(
                    board.D18,
                    TOTAL_LEDS,
                    brightness=0.3,
                    auto_write=False,
                    pixel_order=neopixel.GRB
                )
                print("✓ NeoPixel array initialized")

                if HAS_RQ_UTILS:
                    self.led_indices = self._generate_led_indices()
                else:
                    self.led_indices = {i: i for i in range(TOTAL_LEDS)}
            except Exception as e:
                print(f"✗ NeoPixel init failed: {e}")
                self.neopixel_array = None

        if HAS_SENSEHAT:
            try:
                self.sense_hat = SenseHat()
                print("✓ SenseHat initialized")
            except Exception as e:
                print(f"✗ SenseHat init failed: {e}")

    def _init_gui(self):
        """Initialize Tkinter GUI"""
        try:
            self.root = tk.Tk()
            self.root.title("LED SAP Demo - Hybrid")
            self.root.attributes('-fullscreen', True)
            self.root.configure(bg='#000000')

            # Main frame
            main_frame = tk.Frame(self.root, bg='#000000')
            main_frame.pack(expand=True, fill='both')

            # Canvas
            canvas_width = MATRIX_WIDTH * \
                (LED_SIZE + LED_SPACING) + LED_SPACING
            canvas_height = MATRIX_HEIGHT * \
                (LED_SIZE + LED_SPACING) + LED_SPACING + 100

            self.canvas = Canvas(
                main_frame,
                width=canvas_width,
                height=canvas_height - 100,
                bg='#000000',
                highlightthickness=0
            )
            self.canvas.pack(expand=True)

            # Create LED grid
            self._create_led_grid()

            # Info label
            self.info_label = tk.Label(
                main_frame,
                text="Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit",
                font=('Arial', 12),
                fg='#888888',
                bg='#000000'
            )
            self.info_label.pack(pady=10)

            # Bind keys
            self.root.bind('<Escape>', lambda e: self.stop())
            self.root.bind('r', lambda e: self.toggle_rainbow())
            self.root.bind('R', lambda e: self.toggle_rainbow())
            self.root.bind('b', lambda e: self.toggle_blink())
            self.root.bind('B', lambda e: self.toggle_blink())
            self.root.bind('i', lambda e: self.toggle_ibm())
            self.root.bind('I', lambda e: self.toggle_ibm())
            self.root.bind('q', lambda e: self.stop())
            self.root.bind('Q', lambda e: self.stop())

            print("✓ GUI initialized")
        except Exception as e:
            print(f"✗ GUI init failed: {e}")
            self.use_gui = False

    def _create_led_grid(self):
        """Create visual LED grid in GUI"""
        for row in range(MATRIX_HEIGHT):
            led_row = []
            for col in range(MATRIX_WIDTH):
                x = col * (LED_SIZE + LED_SPACING) + LED_SPACING
                y = row * (LED_SIZE + LED_SPACING) + LED_SPACING

                led = self.canvas.create_oval(
                    x, y,
                    x + LED_SIZE, y + LED_SIZE,
                    fill='#1a1a1a',
                    outline='#333333',
                    width=2
                )
                led_row.append(led)
            self.leds_gui.append(led_row)

    def _generate_led_indices(self):
        """Generate LED indices using RasQberry utilities"""
        try:
            led_config = get_led_config()
            indices = {}
            for row in range(MATRIX_HEIGHT):
                for col in range(MATRIX_WIDTH):
                    display_idx = row * MATRIX_WIDTH + col
                    pixel_idx = map_xy_to_pixel(col, row)
                    indices[display_idx] = pixel_idx if pixel_idx is not None else 0
            return indices
        except:
            return {i: i for i in range(TOTAL_LEDS)}

    def _init_buttons(self):
        """Initialize GPIO buttons"""
        if HAS_GPIO and not HAS_SENSEHAT:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(BUTTON_RAINBOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_BLINK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_IBM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(BUTTON_EXIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
                print(f"✗ GPIO init failed: {e}")

    def set_led(self, row, col, color):
        """Set LED color"""
        if 0 <= row < MATRIX_HEIGHT and 0 <= col < MATRIX_WIDTH:
            self.matrix[row][col] = color

    def clear_matrix(self):
        """Clear all LEDs"""
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                self.matrix[row][col] = COLOR_OFF

    def update_display(self):
        """Update both hardware and GUI displays"""
        # Update hardware LEDs
        if self.neopixel_array:
            try:
                for row in range(MATRIX_HEIGHT):
                    for col in range(MATRIX_WIDTH):
                        display_idx = row * MATRIX_WIDTH + col
                        if display_idx in self.led_indices:
                            led_idx = self.led_indices[display_idx]
                            if 0 <= led_idx < TOTAL_LEDS:
                                self.neopixel_array[led_idx] = self.matrix[row][col]
                self.neopixel_array.show()
            except Exception as e:
                print(f"Hardware update error: {e}")

        # Update GUI
        if self.use_gui and self.canvas:
            try:
                for row in range(MATRIX_HEIGHT):
                    for col in range(MATRIX_WIDTH):
                        color = self.matrix[row][col]
                        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                        self.canvas.itemconfig(
                            self.leds_gui[row][col], fill=hex_color)
            except Exception as e:
                print(f"GUI update error: {e}")

    def get_rainbow_color(self, position, total_positions):
        """Get rainbow color"""
        hue = (position / total_positions + self.hue_offset) % 1.0
        rgb = hsv_to_rgb(hue, 1.0, 1.0)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def draw_sap(self, rainbow=False):
        """Draw SAP letters"""
        self.clear_matrix()

        # Letter patterns
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

        # Draw letters
        for row in range(len(s_rotated)):
            for col in range(len(s_rotated[0])):
                if s_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row, len(s_rotated)) if rainbow else COLOR_SAP_BLUE
                    self.set_led(row + 1, col, color)

        for row in range(len(a_rotated)):
            for col in range(len(a_rotated[0])):
                if a_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row, len(a_rotated)) if rainbow else COLOR_SAP_GOLD
                    self.set_led(row + 9, col, color)

        for row in range(len(p_rotated)):
            for col in range(len(p_rotated[0])):
                if p_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row, len(p_rotated)) if rainbow else COLOR_SAP_BLUE
                    if row + 17 < MATRIX_HEIGHT:
                        self.set_led(row + 17, col, color)

        self.update_display()

    def draw_sap_x_ibm(self):
        """Draw SAP X IBM alternating"""
        self.clear_matrix()

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

        letter_set = ['S', 'A', 'P'] if self.scroll_offset % 2 == 0 else [
            'I', 'B', 'M']
        colors = [COLOR_SAP_BLUE, COLOR_SAP_GOLD, COLOR_SAP_BLUE]
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
        print(f"Rainbow: {'ON' if self.rainbow_mode else 'OFF'}")
        if self.info_label:
            mode = "Rainbow ON" if self.rainbow_mode else "Normal"
            self.info_label.config(
                text=f"{mode} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit")

    def toggle_blink(self):
        """Toggle blink mode"""
        self.blink_mode = not self.blink_mode
        if self.blink_mode:
            self.rainbow_mode = False
            self.ibm_mode = False
            self.blink_state = True
            self.color_cycle_index = 0
        print(f"Blink: {'ON' if self.blink_mode else 'OFF'}")
        if self.info_label:
            mode = "Blink ON" if self.blink_mode else "Normal"
            self.info_label.config(
                text=f"{mode} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit")

    def toggle_ibm(self):
        """Toggle IBM mode"""
        self.ibm_mode = not self.ibm_mode
        if self.ibm_mode:
            self.rainbow_mode = False
            self.blink_mode = False
            self.scroll_offset = 0
        print(f"SAP X IBM: {'ON' if self.ibm_mode else 'OFF'}")
        if self.info_label:
            mode = "SAP X IBM ON" if self.ibm_mode else "Normal"
            self.info_label.config(
                text=f"{mode} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit")

    def stop(self):
        """Stop the controller"""
        self.running = False
        print("Stopping...")
        if self.use_gui and self.root:
            self.root.quit()

    def check_sensehat_buttons(self):
        """Check SenseHat joystick"""
        if self.sense_hat:
            try:
                for event in self.sense_hat.stick.get_events():
                    if event.action == 'pressed':
                        if event.direction == 'up':
                            self.toggle_rainbow()
                        elif event.direction == 'down':
                            self.toggle_blink()
                        elif event.direction in ['left', 'right']:
                            self.toggle_ibm()
                        elif event.direction == 'middle':
                            self.stop()
            except:
                pass

    def animate_gui(self):
        """Animation loop for GUI mode"""
        if not self.running:
            return

        self.check_sensehat_buttons()

        if self.rainbow_mode:
            self.hue_offset = (self.hue_offset + 0.01) % 1.0
            self.draw_sap(rainbow=True)
            delay = 20
        elif self.blink_mode:
            if self.blink_state:
                color = COLOR_CYCLE[self.color_cycle_index]
                self.clear_matrix()
                self.draw_sap(rainbow=False)
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
            delay = 500
        elif self.ibm_mode:
            self.draw_sap_x_ibm()
            delay = 800
        else:
            self.draw_sap(rainbow=False)
            delay = 500

        if self.use_gui and self.root:
            self.root.after(delay, self.animate_gui)

    def animate_hardware(self):
        """Animation loop for hardware-only mode"""
        print("\n=== SAP LED Demo (Hardware Mode) ===")
        print("Controls: SenseHat joystick or GPIO buttons")
        print("Ctrl+C to exit\n")

        try:
            while self.running:
                self.check_sensehat_buttons()

                if self.rainbow_mode:
                    self.hue_offset = (self.hue_offset + 0.01) % 1.0
                    self.draw_sap(rainbow=True)
                    time.sleep(0.02)
                elif self.blink_mode:
                    if self.blink_state:
                        color = COLOR_CYCLE[self.color_cycle_index]
                        self.clear_matrix()
                        self.draw_sap(rainbow=False)
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

    def run(self):
        """Start the application"""
        if self.use_gui:
            self.draw_sap(rainbow=False)
            self.animate_gui()
            self.root.mainloop()
        else:
            self.animate_hardware()

    def cleanup(self):
        """Cleanup resources"""
        if self.neopixel_array:
            self.neopixel_array.fill(COLOR_OFF)
            self.neopixel_array.show()
        if HAS_GPIO:
            try:
                GPIO.cleanup()
            except:
                pass


def main():
    # Determine if we should use GUI
    use_gui = True  # Always try GUI first for desktop icon compatibility

    app = LEDMatrixHybrid(use_gui=use_gui)
    app.run()


if __name__ == "__main__":
    main()
