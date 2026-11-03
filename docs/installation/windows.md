# Installation on Windows

The python.org installers for Windows include tkinter, Tcl and Tk.

## Install Tktable

Not supported yet: there is no tested way to install Tktable for python.org's Python
([#1](https://github.com/nbro/tktable/issues/1)). An experimental CI job is testing whether
[Magicsplat Tcl/Tk](https://magicsplat.com/tcl-installer)'s Tktable works; this page will be
updated with the results.

## Check the installation

```powershell
python -m tktable
```

## Tktable in a non-standard location

Set {ref}`TKTABLE_LIBRARY <tktable-library>` in PowerShell for the current session:

```powershell
$env:TKTABLE_LIBRARY = "C:\path\to\Tktable2.12.1"
```
