# Installation on macOS

These instructions are for installing Tktable yourself, with `pip install pytktable`. With
`pip install "pytktable[binary]"`, you don't need them: see {ref}`prebuilt-tktable`.

## Install tkinter and Tktable

The python.org installers for macOS include tkinter. With [MacPorts](https://www.macports.org/),
install [Tktable](https://ports.macports.org/port/tktable/) (version 2.11):

```sh
sudo port install tktable
```

[conda](other-systems.md#conda) also has Tktable.

If tkinter doesn't work with a Python built by pyenv or Homebrew, see
[Troubleshooting](index.md#troubleshooting).

## Check the installation

```sh
python -m tktable
```

## Tktable in a non-standard location

Set {ref}`TKTABLE_LIBRARY <tktable-library>`, e.g.:

```sh
TKTABLE_LIBRARY=/opt/local/lib/Tktable2.11 python -m tktable
```
