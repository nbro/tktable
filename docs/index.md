# pytktable

A spreadsheet-like table widget for {py:mod}`tkinter`, wrapping the Tcl/Tk
[Tktable](https://wiki.tcl-lang.org/page/Tktable) extension.

```{admonition} Install Tktable
:class: danger

pytktable is only the Python wrapper. The table widget itself is
[Tktable](https://wiki.tcl-lang.org/page/Tktable), an extension for Tcl/Tk written in C, which
`pip install pytktable` does not install. Install it with pytktable, prebuilt for Linux, macOS and
Windows, with `pip install "pytktable[binary]"`, or install it yourself following the
[installation instructions](installation/index.md) for your OS. Then run `python -m tktable` to
check that it works.
```

The wrapper was originally written by [Guilherme Polo](https://github.com/gpip). The code is on
GitHub, in [nbro/tktable](https://github.com/nbro/tktable), where you can also
[report issues](https://github.com/nbro/tktable/issues).

```{image} images/planets.png
:alt: A window with a table of the 8 planets of the Solar System, made with pytktable
```

The [example](usage.md) above shows the planets of the Solar System (screenshot taken on
Windows 11).

## Features

- Spreadsheet-like tables with title rows and columns, editable cells, and keyboard navigation.
- Cell values kept in an {py:class}`~tktable.array_var.ArrayVar` (a Tcl array), or computed on demand by a callback.
- Styling with tags: colors, fonts, alignment and relief, for single cells, rows or columns.
- Merged cells (spans), embedded widgets, and resizable rows and columns.
- Cells that flash when their value changes, with a color of your choice.
- Selection of cells, rows or columns; inserting and deleting rows and columns.
- Callbacks when the active cell changes, to compute cell values, to validate edits, and to
  format the selection when it is copied.
- Works on Linux, macOS and Windows, with Python 3.11 or later and Tcl/Tk 8.6 or 9.0, once
  Tcl/Tk (usually bundled with Python) and the Tktable extension are [installed](installation/index.md).
- [`python -m tktable`](api/cli.md) checks that Tktable can be found and loaded.

## Quick start

```python
from tktable import Table
```

The package is published on PyPI as `pytktable` and imported as `tktable`.

- New here? Start with [Installation](installation/index.md), then [Usage](usage.md).
- Looking for a class or function? See the [API reference](api/index.md).
- Want to contribute? See [Development](development.md).

```{toctree}
:maxdepth: 2
:hidden:

installation/index
usage
api/index
development
releasing
history
changelog
license
```
