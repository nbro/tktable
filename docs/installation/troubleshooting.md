(troubleshooting)=
# Troubleshooting

`_tkinter.TclError: can't find package Tktable` or `invalid command name "table"`
: Tcl cannot find Tktable. Install pytktable with {ref}`prebuilt Tktable <prebuilt-tktable>`, or
  {ref}`install Tktable <without-prebuilt-tktable>` and, if needed, set
  {ref}`TKTABLE_LIBRARY <tktable-library>`.
  {py:class}`~tktable.table.Table` raises {py:class}`~tktable.table.CannotUseError` in this case.

`ModuleNotFoundError: No module named 'tkinter'`
: tkinter is not installed for your Python. On Linux, install your distribution's tkinter
  package ({ref}`see the commands <check-tkinter>`).

`ImportError: ... Library not loaded: .../libtk8.6.dylib` on macOS
: Your Python was compiled (e.g. by pyenv) against Homebrew's Tcl/Tk 8.6, which Homebrew has since
  replaced with Tcl/Tk 9 in the `tcl-tk` formula. Python 3.14 and newer work with Tcl/Tk 9, so
  reinstalling them is enough. Python 3.11 to 3.13 need Tcl/Tk 8.6, from Homebrew's `tcl-tk@8`;
  with pyenv, e.g. for Python 3.11.9:

  ```sh
  brew install tcl-tk@8
  ```

  ```sh
  pyenv uninstall -f 3.11.9
  ```

  ```sh
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk@8)/lib/pkgconfig" pyenv install 3.11.9
  ```

  Then {ref}`check tkinter <check-tkinter>` again, and recreate your virtual environments. The
  python.org installers for macOS don't have this problem: they come with their own Tcl/Tk.

Tktable is found but fails to load
: It was probably built for a different Tcl/Tk version than the one your Python uses (e.g. Tcl 8.6
  vs 9.0). `python -m tktable` shows both.
