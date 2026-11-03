# Installation

Install the package with `pip`:

```sh
pip install pytktable
```

It requires Python >= 3.11.

This package is pure Python, but it also needs these, which `pip` does not install:

1. [Tcl](https://www.tcl-lang.org/) and [Tk](https://wiki.tcl-lang.org/page/Tk);
2. {py:mod}`tkinter`, Python's interface to Tk;
3. [Tktable](https://wiki.tcl-lang.org/page/Tktable), the Tk extension that provides the table
   widget. It usually does not come with Tk.

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

## Troubleshooting

`_tkinter.TclError: can't find package Tktable` or `invalid command name "table"`
: Tcl cannot find Tktable. Install it, or set [`TKTABLE_LIBRARY`](#tktable-library).
  {py:class}`~tktable.table.Table` raises {py:class}`~tktable.table.CannotUseError` in this case.

`ModuleNotFoundError: No module named 'tkinter'`
: tkinter is not installed for your Python. See your OS page.

Tktable is found but fails to load
: It was probably built for a different Tcl/Tk version than the one your Python uses (e.g. Tcl 8.6
  vs 9.0). `python -m tktable` shows both.

```{toctree}
:hidden:

linux-macos
windows
```
