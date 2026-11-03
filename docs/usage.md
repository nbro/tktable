# Usage

A {py:class}`~tktable.table.Table` is a {py:class}`tkinter.Widget`. Its cells are usually stored in
an {py:class}`~tktable.array_var.ArrayVar`, a Tcl array keyed by `"row,col"` indices. The keyword
arguments of {py:class}`~tktable.table.Table` are the options of the Tcl widget, without the leading
`-` (e.g. `rows`, `cols`, `variable`, `titlerows`). See the
[Tktable manual](https://wiki.tcl-lang.org/page/Tktable) for all of them.

## Example

This is [`examples/example1.py`](https://github.com/nbro/tktable/blob/main/examples/example1.py).
To run it without installing Tktable, use Docker: see the instructions for
{ref}`Linux <try-in-docker-linux>` and {ref}`Windows <try-in-docker-windows>`.

```{literalinclude} ../examples/example1.py
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
