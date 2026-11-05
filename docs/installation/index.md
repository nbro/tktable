# Installation

pytktable requires Python >= 3.11 with {py:mod}`tkinter`, Python's interface to Tcl/Tk.

(check-tkinter)=
## Check tkinter first

pytktable can't install or fix tkinter, so first check that your Python has a working one:

```sh
python -c "import tkinter; print(tkinter.TkVersion)"
```

It should print the version of Tcl/Tk your Python uses, e.g. `8.6` or `9.0`. If it fails instead,
fix tkinter first (see [Troubleshooting](#troubleshooting)), then install pytktable.

(prebuilt-tktable)=
## With prebuilt Tktable (recommended)

```sh
pip install "pytktable[binary]"
```

Keep the quotes: some shells, e.g. zsh (the default on macOS), would otherwise treat the brackets
as a file pattern. This also installs [pytktable-binaries](https://github.com/nbro/pytktable-binaries), which contains
[Tktable](https://wiki.tcl-lang.org/page/Tktable), the Tcl/Tk extension that provides the table
widget, compiled for Tcl/Tk 8.6 and 9.0 for:

- Linux: x86_64 and ARM (aarch64), with glibc (most distributions) or musl (e.g. Alpine);
- macOS 11 and later: Intel and Apple silicon;
- Windows: x64, x86 and ARM.

pytktable finds it automatically, so you don't need to install Tktable or set `TKTABLE_LIBRARY`.
You only need tkinter, which the python.org installers for Windows and macOS include. On Linux,
install your distribution's tkinter package, e.g.:

```sh
sudo apt install python3-tk
```

on Debian and Ubuntu, or:

```sh
sudo dnf install python3-tkinter
```

on Fedora. Tktable also needs the X11 library (`libX11`), which every desktop Linux has.

(without-prebuilt-tktable)=
## Without prebuilt Tktable

Install only the Python wrapper, and Tktable yourself, if:

- your platform is not in the list above (e.g. 32-bit ARM Linux, FreeBSD);
- you prefer the Tktable of your OS's package manager;
- the prebuilt Tktable doesn't work for you (please
  [report it](https://github.com/nbro/pytktable-binaries/issues)).

```sh
pip install pytktable
```

Then install these, which `pip install pytktable` does not install:

1. [Tcl](https://www.tcl-lang.org/) and [Tk](https://wiki.tcl-lang.org/page/Tk), and
   {py:mod}`tkinter`;
2. [Tktable](https://wiki.tcl-lang.org/page/Tktable). It usually does not come with Tk.

How to install them depends on your OS:

- [Linux and macOS](linux-macos.md)
- [Windows](windows.md)

## Check the installation

```sh
python -m tktable
```

This prints the versions of Python, Tcl and Tk, where Tcl looks for extensions (`auto_path`), and
whether Tktable can be found and loaded. It exits with status 0 on success. See [](../api/cli.md)
for details.

(tktable-library)=
## Tktable in a non-standard location

If Tktable is installed in a directory Tcl does not search, set the environment variable
`TKTABLE_LIBRARY` to the directory containing Tktable's `pkgIndex.tcl`. That directory is named
after Tktable's version, e.g. `Tktable2.10` for Tktable 2.10. See your OS page for how to set it.

(troubleshooting)=
## Troubleshooting

`_tkinter.TclError: can't find package Tktable` or `invalid command name "table"`
: Tcl cannot find Tktable. Install pytktable with [prebuilt Tktable](#prebuilt-tktable), or
  [install Tktable](#without-prebuilt-tktable) and, if needed, set
  [`TKTABLE_LIBRARY`](#tktable-library).
  {py:class}`~tktable.table.Table` raises {py:class}`~tktable.table.CannotUseError` in this case.

`ModuleNotFoundError: No module named 'tkinter'`
: tkinter is not installed for your Python. On Linux, install your distribution's tkinter
  package ([see above](#prebuilt-tktable)).

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

  Then [check tkinter](#check-tkinter) again, and recreate your virtual environments. The
  python.org installers for macOS don't have this problem: they come with their own Tcl/Tk.

Tktable is found but fails to load
: It was probably built for a different Tcl/Tk version than the one your Python uses (e.g. Tcl 8.6
  vs 9.0). `python -m tktable` shows both.

```{toctree}
:hidden:

linux-macos
windows
```
