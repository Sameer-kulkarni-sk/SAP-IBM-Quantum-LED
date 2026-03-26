#!/usr/bin/env python3
"""
LED SAP Demo - Visual LED Matrix Simulator
Displays "SAP" on a simulated 24x8 LED matrix
Optimized for 1280x720 landscape display
"""

import tkinter as tk
import time
from tkinter import Canvas

# LED Matrix Configuration
MATRIX_WIDTH = 8  # columns
MATRIX_HEIGHT = 24  # rows
LED_SIZE = 40  # pixels per LED
LED_SPACING = 5  # spacing between LEDs
ANIMATION_DELAY = 1000  # milliseconds

# SAP Colors
COLOR_SAP_BLUE = '#0070F2'
COLOR_SAP_GOLD = '#F0AB00'
COLOR_OFF = '#1a1a1a'
COLOR_BACKGROUND = '#000000'

# Color cycle for blinking mode
COLOR_CYCLE = [
    COLOR_SAP_BLUE,
    COLOR_SAP_GOLD,
    '#FF0000',  # Red
    '#00FF00',  # Green
    '#FF00FF',  # Magenta
    '#00FFFF',  # Cyan
    '#FFFFFF',  # White
]


class LEDMatrix:
    def __init__(self, root):
        self.root = root
        self.root.title("LED SAP Demo")

        # Force landscape mode and fullscreen
        # Force landscape mode and fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLOR_BACKGROUND)

        # Calculate canvas size
        canvas_width = MATRIX_WIDTH * (LED_SIZE + LED_SPACING) + LED_SPACING
        canvas_height = MATRIX_HEIGHT * \
            (LED_SIZE + LED_SPACING) + LED_SPACING + 100

        # Create main frame
        self.main_frame = tk.Frame(root, bg=COLOR_BACKGROUND)
        self.main_frame.pack(expand=True, fill='both')

        # Create canvas for LED matrix
        self.canvas = Canvas(
            self.main_frame,
            width=canvas_width,
            height=canvas_height - 100,
            bg=COLOR_BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        # Initialize LED grid
        self.leds = []
        self.create_led_grid()

        # Initialize matrix state
        self.matrix = [[0 for _ in range(MATRIX_WIDTH)]
                       for _ in range(MATRIX_HEIGHT)]

        # Animation state
        self.rainbow_mode = False
        self.blink_mode = False
        self.blink_state = True
        self.color_cycle_index = 0
        self.ibm_mode = False
        self.scroll_offset = 0

        # Bind keys
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('r', lambda e: self.toggle_rainbow())
        self.root.bind('R', lambda e: self.toggle_rainbow())
        self.root.bind('b', lambda e: self.toggle_blink())
        self.root.bind('B', lambda e: self.toggle_blink())
        self.root.bind('i', lambda e: self.toggle_ibm())
        self.root.bind('I', lambda e: self.toggle_ibm())
        self.root.bind('q', lambda e: self.root.quit())
        self.root.bind('Q', lambda e: self.root.quit())

        # Info label
        self.info_label = tk.Label(
            self.main_frame,
            text="Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit",
            font=('Arial', 12),
            fg='#888888',
            bg=COLOR_BACKGROUND
        )
        self.info_label.pack(pady=10)

        # Start animation
        self.animate()

    def create_led_grid(self):
        """Create the visual LED grid"""
        for row in range(MATRIX_HEIGHT):
            led_row = []
            for col in range(MATRIX_WIDTH):
                x = col * (LED_SIZE + LED_SPACING) + LED_SPACING
                y = row * (LED_SIZE + LED_SPACING) + LED_SPACING

                # Create LED circle
                led = self.canvas.create_oval(
                    x, y,
                    x + LED_SIZE, y + LED_SIZE,
                    fill=COLOR_OFF,
                    outline='#333333',
                    width=2
                )
                led_row.append(led)
            self.leds.append(led_row)

    def set_led(self, row, col, color):
        """Set LED color at specific position"""
        if 0 <= row < MATRIX_HEIGHT and 0 <= col < MATRIX_WIDTH:
            self.canvas.itemconfig(self.leds[row][col], fill=color)
            self.matrix[row][col] = 1 if color != COLOR_OFF else 0

    def clear_matrix(self):
        """Turn off all LEDs"""
        for row in range(MATRIX_HEIGHT):
            for col in range(MATRIX_WIDTH):
                self.set_led(row, col, COLOR_OFF)

    def get_rainbow_color(self, row):
        """Get rainbow color for specific row"""
        colors = [
            '#83209e',  # purple
            '#0041b7',  # blue
            '#00c4ad',  # turquoise
            '#02a204',  # green
            '#f8df08',  # yellow
            '#f9831f',  # orange
            '#fa0100',  # red
            '#fb80bf'   # pink
        ]
        return colors[row] if row < len(colors) else COLOR_SAP_BLUE

    def draw_sap(self, rainbow=False):
        """Draw SAP letters on the LED matrix - patterns rotated 90° clockwise"""
        self.clear_matrix()

        # Original patterns (8 rows × 6 cols)
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

        # Rotate 90° clockwise: rotated = [list(row) for row in zip(*pattern[::-1])]
        s_rotated = [list(row) for row in zip(*s_orig[::-1])]
        a_rotated = [list(row) for row in zip(*a_orig[::-1])]
        p_rotated = [list(row) for row in zip(*p_orig[::-1])]

        # Draw S (now 6 rows × 8 cols after rotation)
        for row in range(len(s_rotated)):
            for col in range(len(s_rotated[0])):
                if s_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row) if rainbow else COLOR_SAP_BLUE
                    self.set_led(row + 1, col, color)

        # Draw A (now 6 rows × 8 cols after rotation)
        for row in range(len(a_rotated)):
            for col in range(len(a_rotated[0])):
                if a_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row) if rainbow else COLOR_SAP_GOLD
                    self.set_led(row + 9, col, color)

        # Draw P (now 6 rows × 8 cols after rotation)
        for row in range(len(p_rotated)):
            for col in range(len(p_rotated[0])):
                if p_rotated[row][col]:
                    color = self.get_rainbow_color(
                        row) if rainbow else COLOR_SAP_BLUE
                    if row + 17 < MATRIX_HEIGHT:
                        self.set_led(row + 17, col, color)

    def draw_sap_with_color(self, color):
        """Draw SAP letters with a specific color"""
        self.clear_matrix()

        # Original patterns (8 rows × 6 cols)
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
                    self.set_led(row + 1, col, color)

        # Draw A
        for row in range(len(a_rotated)):
            for col in range(len(a_rotated[0])):
                if a_rotated[row][col]:
                    self.set_led(row + 9, col, color)

        # Draw P
        for row in range(len(p_rotated)):
            for col in range(len(p_rotated[0])):
                if p_rotated[row][col]:
                    if row + 17 < MATRIX_HEIGHT:
                        self.set_led(row + 17, col, color)

    def toggle_rainbow(self):
        """Toggle rainbow mode"""
        self.rainbow_mode = not self.rainbow_mode
        if self.rainbow_mode:
            self.blink_mode = False
            self.ibm_mode = False
        mode_text = "Rainbow Mode ON" if self.rainbow_mode else "Rainbow Mode OFF"
        self.info_label.config(
            text=f"{mode_text} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit"
        )

    def toggle_blink(self):
        """Toggle blink mode"""
        self.blink_mode = not self.blink_mode
        if self.blink_mode:
            self.rainbow_mode = False
            self.ibm_mode = False
            self.blink_state = True
            self.color_cycle_index = 0
        mode_text = "Blink Mode ON" if self.blink_mode else "Blink Mode OFF"
        self.info_label.config(
            text=f"{mode_text} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit"
        )

    def toggle_ibm(self):
        """Toggle IBM scrolling mode"""
        self.ibm_mode = not self.ibm_mode
        if self.ibm_mode:
            self.rainbow_mode = False
            self.blink_mode = False
            self.scroll_offset = 0
        mode_text = "SAP X IBM Mode ON" if self.ibm_mode else "SAP X IBM Mode OFF"
        self.info_label.config(
            text=f"{mode_text} | Press 'R' Rainbow | 'B' Blink | 'I' SAP X IBM | 'ESC' Exit"
        )

    def draw_sap_x_ibm(self):
        """Draw 'SAP X IBM' alternating - same format as regular SAP"""
        self.clear_matrix()

        # Original patterns (8 rows × 6 cols) - same as draw_sap
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

        # I pattern
        i_orig = [
            [1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1],
        ]

        # B pattern
        b_orig = [
            [1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0],
        ]

        # M pattern
        m_orig = [
            [1, 1, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1],
        ]

        # Rotate all 90° clockwise
        s_rotated = [list(row) for row in zip(*s_orig[::-1])]
        a_rotated = [list(row) for row in zip(*a_orig[::-1])]
        p_rotated = [list(row) for row in zip(*p_orig[::-1])]
        i_rotated = [list(row) for row in zip(*i_orig[::-1])]
        b_rotated = [list(row) for row in zip(*b_orig[::-1])]
        m_rotated = [list(row) for row in zip(*m_orig[::-1])]

        # Alternate between "SAP" and "IBM" based on scroll_offset
        if self.scroll_offset % 2 == 0:
            # Draw S
            for row in range(len(s_rotated)):
                for col in range(len(s_rotated[0])):
                    if s_rotated[row][col]:
                        self.set_led(row + 1, col, COLOR_SAP_BLUE)

            # Draw A
            for row in range(len(a_rotated)):
                for col in range(len(a_rotated[0])):
                    if a_rotated[row][col]:
                        self.set_led(row + 9, col, COLOR_SAP_GOLD)

            # Draw P
            for row in range(len(p_rotated)):
                for col in range(len(p_rotated[0])):
                    if p_rotated[row][col]:
                        if row + 17 < MATRIX_HEIGHT:
                            self.set_led(row + 17, col, COLOR_SAP_BLUE)
        else:
            # Draw I
            for row in range(len(i_rotated)):
                for col in range(len(i_rotated[0])):
                    if i_rotated[row][col]:
                        self.set_led(row + 1, col, COLOR_SAP_BLUE)

            # Draw B
            for row in range(len(b_rotated)):
                for col in range(len(b_rotated[0])):
                    if b_rotated[row][col]:
                        self.set_led(row + 9, col, COLOR_SAP_GOLD)

            # Draw M
            for row in range(len(m_rotated)):
                for col in range(len(m_rotated[0])):
                    if m_rotated[row][col]:
                        if row + 17 < MATRIX_HEIGHT:
                            self.set_led(row + 17, col, COLOR_SAP_BLUE)

        # Update scroll offset for alternating
        self.scroll_offset = (self.scroll_offset + 1) % 2

    def animate(self):
        """Animation loop for rainbow, blink, and IBM scrolling effects"""
        if self.rainbow_mode:
            self.draw_sap(rainbow=True)
        elif self.blink_mode:
            if self.blink_state:
                # Cycle through colors
                self.color_cycle_index = (
                    self.color_cycle_index + 1) % len(COLOR_CYCLE)
                self.draw_sap_with_color(COLOR_CYCLE[self.color_cycle_index])
            else:
                # Turn off (show background)
                self.clear_matrix()
            self.blink_state = not self.blink_state
        elif self.ibm_mode:
            self.draw_sap_x_ibm()
        else:
            self.draw_sap(rainbow=False)

        # Adjust timing based on mode
        delay = 800 if self.ibm_mode else 500
        self.root.after(delay, self.animate)


def main():
    root = tk.Tk()
    app = LEDMatrix(root)
    root.mainloop()


if __name__ == "__main__":
    main()
