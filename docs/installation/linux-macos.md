# Installation on Linux and macOS

## Install tkinter and Tktable

On Debian and Ubuntu:

```sh
sudo apt install python3-tk tk-table
```

Fedora has no Tktable package in its current releases (e.g. Fedora 45).

On macOS, with [MacPorts](https://www.macports.org/):

```sh
sudo port install tktable
```

## Check the installation

```sh
python -m tktable
```

## Tktable in a non-standard location

Set {ref}`TKTABLE_LIBRARY <tktable-library>` for one command:

```sh
TKTABLE_LIBRARY=/usr/lib/Tktable2.10 python -m tktable
```

Or for the whole shell session:

```sh
export TKTABLE_LIBRARY=/usr/lib/Tktable2.10
```
