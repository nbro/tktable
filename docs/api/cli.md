# python -m tktable

```sh
python -m tktable
```

Diagnoses whether Tktable can be used, step by step:

1. imports {py:mod}`tkinter`;
2. starts a Tcl interpreter (no window, so no display is needed) and prints its version,
   `TKTABLE_LIBRARY` and `auto_path`;
3. looks for Tktable with {py:func}`~tktable.utils.find_tktable`, without loading it;
4. if a display is available, starts Tk and loads Tktable with
   {py:func}`~tktable.utils.load_tktable`.

It exits with status 0 if Tktable is found (and loaded, when a display is available), and 1
otherwise, so it can be used in scripts and CI.

```{eval-rst}
.. automodule:: tktable.__main__
```
