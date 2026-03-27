#!/usr/bin/env python3
"""
Patch the virtual LED GUI to match physical LED mapping
"""

# Read the original file
with open('/usr/bin/rq_led_virtual_gui.py', 'r') as f:
    content = f.read()

# Find the map_xy_to_pixel_quad function and replace it
import re

# New function that matches rq_led_utils.py exactly
new_function = '''    def map_xy_to_pixel_quad(self, x, y):
        """
        Map (x, y) coordinates to pixel index for quad panel layout.
        
        FIXED: Now matches the physical LED mapping from rq_led_utils.py exactly.
        Layout: Four 4x12 panels wired TL→TR→BR→BL
        """
        # Bounds checking
        if x < 0 or x >= 24 or y < 0 or y >= 8:
            return None
        
        # Original calculation logic from neopixel_spi_IBMtestFunc.py
        # (matches rq_led_utils.py exactly)
        
        # Top row calculation
        x1 = x * 4 + (0 if x % 2 == 0 else 3)
        y1 = (7 - y if x % 2 == 0 else y - 7)
        
        # Bottom row calculation
        x2 = 96 + (23 - x) * 4 + (0 if x % 2 == 0 else 3)
        y2 = (3 - y if x % 2 == 0 else y - 3)
        
        # Select based on row position
        return x2 + y2 if y < 4 else x1 + y1
'''

# Pattern to match the old function (from def to next def or class)
pattern = r'(    def map_xy_to_pixel_quad\(self, x, y\):.*?)(\n    def )'
replacement = new_function + r'\2'

# Replace the function
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the patched file
with open('/usr/bin/rq_led_virtual_gui.py', 'w') as f:
    f.write(new_content)

print("Virtual LED GUI patched successfully!")
print("The virtual display will now match the physical LED mapping.")
print("Please restart any running LED demos to see the fix.")
