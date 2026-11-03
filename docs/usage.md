# Usage

A {py:class}`~tktable.table.Table` is a {py:class}`tkinter.Widget`. Its cells are usually stored in
an {py:class}`~tktable.array_var.ArrayVar`, a Tcl array keyed by `"row,col"` indices. The keyword
arguments of {py:class}`~tktable.table.Table` are the options of the Tcl widget, without the leading
`-` (e.g. `rows`, `cols`, `variable`, `titlerows`). See the
[Tktable manual](https://wiki.tcl-lang.org/page/Tktable) for all of them.

## Example

[`examples/planets.py`](https://github.com/nbro/tktable/blob/main/examples/planets.py) shows the
8 planets of the Solar System, from NASA's Planetary Fact Sheet, in an editable table:

```{image} images/planets.png
:alt: A window with a table of the 8 planets of the Solar System, made with pytktable
```

The screenshot was taken on Windows 11; the window looks native on each OS.

To run it without installing Tktable, use Docker: see the instructions for
{ref}`Linux <try-in-docker-linux>` and {ref}`Windows <try-in-docker-windows>`.

```{literalinclude} ../examples/planets.py
:language: python
```

## Callbacks

Callbacks such as `command`, `browsecommand` and `validatecommand` receive a
{py:class}`tkinter.Event` with these attributes (the Tcl `%`-substitutions):

| Attribute | Meaning |
|---|---|
| `r`, `c` | row and column of the cell |
| `C` | the index `"r,c"` |
| `i` | 1 if the cell is being written to, 0 if read |
| `s`, `S` | the current and new value |
| `W` | the widget |

## More examples

Each of these small examples shows one feature. Run one from the repository's root, e.g.
`poetry run python -m examples.tags`. CI runs all of them, so they are known to work.

| Example | Shows |
|---|---|
| [`callback_values.py`](https://github.com/nbro/tktable/blob/main/examples/callback_values.py) | Cell values computed on demand by a callback (`usecommand`, `command`) |
| [`tags.py`](https://github.com/nbro/tktable/blob/main/examples/tags.py) | Styling cells, rows and columns with tags |
| [`spans.py`](https://github.com/nbro/tktable/blob/main/examples/spans.py) | Merged cells (`spans`) |
| [`embedded_widgets.py`](https://github.com/nbro/tktable/blob/main/examples/embedded_widgets.py) | Buttons and checkboxes inside cells (`window_configure`) |
| [`resizing.py`](https://github.com/nbro/tktable/blob/main/examples/resizing.py) | Rows and columns resizable with the mouse (`resizeborders`), and sizes set in code |
| [`selection.py`](https://github.com/nbro/tktable/blob/main/examples/selection.py) | Selecting cells, rows or columns, and `browsecommand` |
| [`insert_delete.py`](https://github.com/nbro/tktable/blob/main/examples/insert_delete.py) | Inserting and deleting rows and columns |
| [`validation.py`](https://github.com/nbro/tktable/blob/main/examples/validation.py) | Rejecting invalid edits (`validate`, `validatecommand`) |
