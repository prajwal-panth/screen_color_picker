import tkinter as tk
from tkinter import ttk, messagebox
from pynput import mouse
import pyautogui
import colorsys
import webbrowser
from .utils import rgb_to_hex, save_color_to_file

class ScreenColorPicker:
    def __init__(self, master: tk.Tk, width: int, height: int):
        self.master = master
        self.master.title("Screen Color Picker")
        
        self.window_width = width
        self.window_height = height
        self.master.geometry(f"{self.window_width}x{self.window_height}")
        self.master.resizable(False, False)
        self.master.attributes('-topmost', True)  # Always on top

        self.current_color = "#FFFFFF"  # Initialize with white
        self.theme = "light"
        self.picking_color = False
        self.listener = None
        self.github_url = "https://github.com/prajwal-panth"

        self.setup_ui()
        self.update_color_display()

    def setup_ui(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_top_frame(main_frame)
        self.setup_color_display(main_frame)
        self.setup_labels(main_frame)
        self.setup_buttons(main_frame)

    def setup_top_frame(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        help_button = ttk.Button(top_frame, text="?", width=3, command=self.show_help)
        help_button.pack(side=tk.LEFT)

        theme_button = ttk.Button(top_frame, text="🌓", command=self.toggle_theme, width=3)
        theme_button.pack(side=tk.LEFT)

        about_button = ttk.Button(top_frame, text="About", command=self.open_about, width=8)
        about_button.pack(side=tk.RIGHT)

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.master.tk_setPalette(background='#2b2b2b', foreground='#D2D2D2')
        else:
            self.theme = "light"
            self.master.tk_setPalette(background='#D2D2D2', foreground='black')
        
        style = ttk.Style()
        
        if self.theme == "dark":
            style.configure("TButton", foreground="#D2D2D2", background="#3b3b3b")
            style.configure("TLabel", foreground="#D2D2D2", background="#2b2b2b")
            style.configure("TFrame", background="#2b2b2b")
        else:
            style.configure("TButton", foreground="black", background="#f0f0f0")
            style.configure("TLabel", foreground="black", background="#D2D2D2")
            style.configure("TFrame", background="#D2D2D2")

    def setup_color_display(self, parent):
        self.color_display = tk.Canvas(parent, width=150, height=150, relief="ridge", borderwidth=2)
        self.color_display.pack(pady=10)

    def setup_labels(self, parent):
        self.color_label = ttk.Label(parent, text="Click 'Pick Color' to start", font=('Helvetica', 12))
        self.color_label.pack(pady=5)

        self.hex_label = ttk.Label(parent, text="", font=('Helvetica', 12, 'bold'))
        self.hex_label.pack(pady=2)

        self.rgb_label = ttk.Label(parent, text="", font=('Helvetica', 12))
        self.rgb_label.pack(pady=2)

        self.hsv_label = ttk.Label(parent, text="", font=('Helvetica', 12))
        self.hsv_label.pack(pady=2)

    def setup_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)

        self.pick_button = ttk.Button(button_frame, text="Pick Color", command=self.start_color_pick, width=15)
        self.pick_button.grid(row=0, column=0, padx=5)

        self.copy_button = ttk.Button(button_frame, text="Copy HEX", command=self.copy_to_clipboard, width=15)
        self.copy_button.grid(row=0, column=1, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save Color", command=self.save_color, width=15)
        self.save_button.grid(row=1, column=0, columnspan=2, pady=5)

    def start_color_pick(self):
        if not self.picking_color:
            self.picking_color = True
            self.color_label.config(text="Click on the screen to pick a color")
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()

    def on_click(self, x: int, y: int, button, pressed: bool):
        if pressed and self.picking_color:
            try:
                pixel_color = pyautogui.screenshot().getpixel((x, y))
                rgb_color = pixel_color[:3]
                self.current_color = rgb_to_hex(rgb_color)
                self.update_color_display()
                self.color_label.config(text="Color picked successfully!")
            except Exception as e:
                self.color_label.config(text=f"Error: {str(e)}")
            finally:
                self.picking_color = False
                if self.listener:
                    self.listener.stop()
                    self.listener = None

    def update_color_display(self):
        self.color_display.config(bg=self.current_color)
        r, g, b = tuple(int(self.current_color[i:i+2], 16) for i in (1, 3, 5))
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        self.hex_label.config(text=f"HEX: {self.current_color.upper()}")
        self.rgb_label.config(text=f"RGB: ({r}, {g}, {b})")
        self.hsv_label.config(text=f"HSV: ({int(h*360)}°, {int(s*100)}%, {int(v*100)}%)")

    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.current_color.upper())
        self.color_label.config(text="HEX color copied to clipboard!")

    def save_color(self):
        save_color_to_file(self.current_color)
        self.color_label.config(text="Color saved to saved_colors.txt")

    def open_about(self):
        webbrowser.open(self.github_url)

    def show_help(self):
        help_text = """
        Screen Color Picker Help:
        
        1. Click 'Pick Color' to start the color picking process.
        2. Click anywhere on the screen to select a color.
        3. The selected color will be displayed with its HEX, RGB, and HSV values.
        4. Use 'Copy HEX' to copy the color's HEX value to clipboard.
        5. Use 'Save Color' to save the current color to a text file.
        6. Click the 'About' button to visit the developer's profile.
        7. Use the 🌓 button to toggle between light and dark themes.
        """
        messagebox.showinfo("Help", help_text)

    def on_close(self):
        if self.listener:
            self.listener.stop()
        self.master.quit()