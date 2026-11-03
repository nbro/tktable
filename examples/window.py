"""Window setup shared by the examples: theme, sharp text, description, size and position."""

import sys
import tkinter
from tkinter import ttk

DESCRIPTION_WIDTH = 640  # pixels


def enable_sharp_text_on_windows() -> None:
    """Tell Windows this app handles high-DPI screens, so text is crisp instead of blurry.

    Must run before the window is created. Does nothing on other systems.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes  # pylint: disable=import-outside-toplevel

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


def use_modern_theme(root: tkinter.Tk) -> None:
    """Use the native ttk theme on Windows (vista) and macOS (aqua), else the modern "clam"."""
    style = ttk.Style(root)
    for theme in ("vista", "aqua", "clam"):
        if theme in style.theme_names():
            style.theme_use(theme)
            return


def create_window(title: str, description: str) -> tuple[tkinter.Tk, ttk.Frame]:
    """Create the example's window, with its description at the top.

    :return: the window, and the frame to put the example's widgets in.
    """
    enable_sharp_text_on_windows()
    root = tkinter.Tk()
    root.title(f"{title} - pytktable example")
    use_modern_theme(root)

    # A themed frame gives the window the theme's background and padding.
    frame = ttk.Frame(root, padding=16)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text=description, wraplength=DESCRIPTION_WIDTH, justify="left").pack(
        side="top", fill="x", pady=(0, 12)
    )
    return root, frame


def fit_and_center(root: tkinter.Tk) -> None:
    """Center the window on the screen, and don't let it get smaller than its contents."""
    root.update_idletasks()  # Lay out the window, so its size is known.
    width, height = root.winfo_reqwidth(), root.winfo_reqheight()

    root.minsize(width, height)

    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"+{x}+{y}")


def run(root: tkinter.Tk) -> None:
    """Center the window and show it. With -test, close it after a second (used by the tests)."""
    fit_and_center(root)
    if "-test" in sys.argv:
        root.after(1000, root.destroy)
    root.mainloop()
