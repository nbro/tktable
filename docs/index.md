# pytktable

A spreadsheet-like table widget for {py:mod}`tkinter`, wrapping the Tcl/Tk
[Tktable](https://wiki.tcl-lang.org/page/Tktable) extension.

The wrapper was originally written by [Guilherme Polo](https://github.com/gpip).

```{image} images/example1.png
:alt: A window with a table of the 8 planets of the Solar System, made with pytktable
```

The [example](usage.md) above shows the planets of the Solar System.

## Features

- Spreadsheet-like tables with title rows and columns, editable cells, and keyboard navigation.
- Cell values kept in an {py:class}`~tktable.array_var.ArrayVar` (a Tcl array), or computed on demand by a callback.
- Styling with tags: colors, fonts, alignment and relief, for single cells, rows or columns.
- Merged cells (spans), embedded widgets, and resizable rows and columns.
- Selection of cells, rows or columns; inserting and deleting rows and columns.
- Callbacks for browsing, editing, selection and validation of cells.
- Works on Linux, macOS and Windows, with Python 3.11 or later and Tcl/Tk 8.6 or 9.0.
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
changelog
license
```
