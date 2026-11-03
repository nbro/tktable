"""Diagnose whether Tktable can be used: ``python -m tktable``.

Exits with status 0 if Tktable can be found (and loaded, when a display is available),
and 1 otherwise.
"""

import os
import platform
import sys


def main() -> int:
    """Print diagnostic information and return the exit status."""
    print(f"Python:    {sys.version.split()[0]} ({platform.platform()})")

    try:
        import tkinter  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        print(f"tkinter:   NOT AVAILABLE ({exc})")
        print("Install tkinter for your Python (e.g. `sudo apt install python3-tk`).")
        return 1

    # pylint: disable-next=import-outside-toplevel
    from tktable.utils import TKTABLE_LIBRARY_ENV_VAR, find_tktable, load_tktable

    try:
        interp = tkinter.Tcl()  # Tcl only: no window, so no display needed.
    except tkinter.TclError as exc:
        print(f"Tcl:       NOT AVAILABLE ({exc})")
        return 1

    print(f"Tcl:       {interp.call('info', 'patchlevel')}")
    print(f"{TKTABLE_LIBRARY_ENV_VAR}: {os.environ.get(TKTABLE_LIBRARY_ENV_VAR, '(not set)')}")
    versions = find_tktable(interp)
    # One folder per line, as plain text (Tcl 9 returns them as "path objects").
    print("auto_path:")
    for folder in interp.tk.splitlist(interp.call("set", "auto_path")):
        print(f"  {folder}")
    if not versions:
        print("Tktable:   NOT FOUND")
        print("See https://nbro.github.io/tktable/installation/")
        return 1
    print(f"Tktable:   found version(s) {', '.join(versions)}")

    try:
        root = tkinter.Tk()
    except tkinter.TclError as exc:
        print(f"Tk:        cannot start ({exc}); skipped loading Tktable")
        return 0

    try:
        root.withdraw()
        print(f"Tk:        {root.call('info', 'patchlevel')}")
        print(f"Tktable:   loaded version {load_tktable(root)}")
    except tkinter.TclError as exc:
        print(f"Tktable:   FOUND BUT FAILED TO LOAD ({exc})")
        print("It may have been built for a different Tcl/Tk version than your Python uses.")
        return 1
    finally:
        root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
