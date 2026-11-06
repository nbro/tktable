# Installation on other systems

These instructions are for installing Tktable yourself, with `pip install pytktable`, on systems
without prebuilt Tktable, or if you prefer your system's own. Install tkinter for your Python from
the same package manager.

## FreeBSD, OpenBSD and NetBSD

| System | Command | Version |
|---|---|---|
| [FreeBSD](https://www.freshports.org/x11-toolkits/tktable/) | `sudo pkg install tktable` | 2.10 |
| [OpenBSD](https://openports.pl/search?file=tktable) | `doas pkg_add Tktable` | 2.10 |
| [NetBSD](https://pkgsrc.se/x11/tktable) (pkgsrc) | `pkgin install tktable` | 2.10 |

(conda)=
## conda

On Linux, macOS and Windows, [conda-forge](https://github.com/conda-forge/tktable-feedstock) has
Tktable, for the Tcl/Tk of a conda environment:

```sh
conda install -c conda-forge tktable
```

## Check the installation

```sh
python -m tktable
```
