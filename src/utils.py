import colorsys
from typing import Tuple

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return '#%02x%02x%02x' % rgb

def save_color_to_file(color: str):
    r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    with open("saved_colors.txt", "a") as f:
        f.write(f"{color.upper()} - RGB: ({r}, {g}, {b}) - HSV: ({int(h*360)}°, {int(s*100)}%, {int(v*100)}%)\n")