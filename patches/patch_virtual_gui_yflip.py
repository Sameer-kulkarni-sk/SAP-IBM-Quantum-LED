#!/usr/bin/env python3
"""
Patch virtual LED GUI to apply Y-flip transformation
This makes the virtual display match the physical LEDs when Y-flip is used
"""

# Read the original file
with open('/usr/bin/rq_led_virtual_gui.py', 'r') as f:
    content = f.read()

# Find the map_xy_to_pixel function and update it to apply Y-flip
import re

# New map_xy_to_pixel that applies Y-flip before calling quad mapping
new_function = '''    def map_xy_to_pixel(self, x, y):
        """
        Map (x, y) coordinates to pixel index based on configured layout.
        
        UPDATED: Now applies Y-flip transformation to match physical LED behavior.
        The physical LEDs have Y-flip enabled in config, so we apply it here too.
        """
        # Apply Y-flip transformation (y → 7-y) to match physical LEDs
        # This is needed because LED_MATRIX_Y_FLIP=true in config
        y_flipped = 7 - y
        
        if MATRIX_LAYOUT == 'quad':
            return self.map_xy_to_pixel_quad(x, y_flipped)
        return self.map_xy_to_pixel_single(x, y_flipped)
'''

# Pattern to match the old map_xy_to_pixel function
pattern = r'(    def map_xy_to_pixel\(self, x, y\):.*?)(\n    def map_xy_to_pixel_single)'
replacement = new_function + r'\2'

# Replace the function
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the patched file
with open('/usr/bin/rq_led_virtual_gui.py', 'w') as f:
    f.write(new_content)

print("Virtual LED GUI patched with Y-flip support!")
print("The virtual display will now apply Y-flip like the physical LEDs.")
print("Please restart the virtual LED GUI to see the fix.")
