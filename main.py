import tkinter as tk
from src.color_picker import ScreenColorPicker

def main():
    root = tk.Tk()
    app = ScreenColorPicker(root, width=350, height=450)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()