"""Diagnose whether Tktable can be used: ``python -m tktable``.

Exits with status 0 if Tktable can be found (and loaded, when a display is available),
and 1 otherwise.
"""

import os
import platform
import sys

#: Where to read how to install tkinter, Tcl/Tk and Tktable.
INSTALLATION_URL = "https://nbro.github.io/tktable/installation/"


def label(name: str) -> str:
    """``name`` followed by a colon, padded so that the values line up."""
    return f"{name + ':':<28}"


#: Tktable is the Tcl/Tk extension, not this Python package (pytktable), so say it.
TKTABLE = label("Tktable (Tcl/Tk extension)")


def main() -> int:
    """Print diagnostic information and return the exit status."""
    print(f"{label('Python')}{sys.version.split()[0]} ({platform.platform()})")

    try:
        import tkinter  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        print(f"{label('tkinter')}NOT AVAILABLE ({exc})")
        print(f"Your Python has no working tkinter: see {INSTALLATION_URL}")
        return 1

    # pylint: disable-next=import-outside-toplevel
    from tktable.utils import TKTABLE_LIBRARY_ENV_VAR, find_tktable, load_tktable

    try:
        interp = tkinter.Tcl()  # Tcl only: no window, so no display needed.
    except tkinter.TclError as exc:
        print(f"{label('Tcl')}NOT AVAILABLE ({exc})")
        return 1

    print(f"{label('Tcl')}{interp.call('info', 'patchlevel')}")
    print(f"{label(TKTABLE_LIBRARY_ENV_VAR)}{os.environ.get(TKTABLE_LIBRARY_ENV_VAR, '(not set)')}")
    versions = find_tktable(interp)
    # One folder per line, as plain text (Tcl 9 returns them as "path objects").
    print("auto_path:")
    for folder in interp.tk.splitlist(interp.call("set", "auto_path")):
        print(f"  {folder}")
    if not versions:
        print(f"{TKTABLE}NOT FOUND")
        print(f"See {INSTALLATION_URL}")
        return 1
    print(f"{TKTABLE}found version(s) {', '.join(versions)}")

    try:
        root = tkinter.Tk()
    except tkinter.TclError as exc:
        print(f"{label('Tk')}cannot start ({exc}); skipped loading Tktable")
        return 0

    try:
        root.withdraw()
        print(f"{label('Tk')}{root.call('info', 'patchlevel')}")
        print(f"{TKTABLE}loaded version {load_tktable(root)}")
    except tkinter.TclError as exc:
        print(f"{TKTABLE}FOUND BUT FAILED TO LOAD ({exc})")
        print("It may have been built for a different Tcl/Tk version than your Python uses.")
        return 1
    finally:
        root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
