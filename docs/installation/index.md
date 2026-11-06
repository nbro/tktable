# Installation

pytktable requires Python >= 3.11 with {py:mod}`tkinter`, Python's interface to Tcl/Tk.

(check-tkinter)=
## Check tkinter first

pytktable can't install or fix tkinter, so first check that your Python has a working one:

```sh
python -c "import tkinter; print(tkinter.TkVersion)"
```

It should print the version of Tcl/Tk your Python uses, e.g. `8.6` or `9.0`. If it fails instead,
install or fix tkinter first, then install pytktable. The python.org installers for Windows and
macOS include tkinter. On Linux, install your distribution's tkinter package:

| Distribution | Command |
|---|---|
| Debian | `sudo apt install python3-tk` |
| Ubuntu | `sudo apt install python3-tk` |
| Linux Mint | `sudo apt install python3-tk` |
| Kali Linux | `sudo apt install python3-tk` |
| Fedora | `sudo dnf install python3-tkinter` |
| RHEL 10 | `sudo dnf install python3-tkinter` |
| CentOS Stream 10 | `sudo dnf install python3-tkinter` |
| RHEL 9 | `sudo dnf install python3.12 python3.12-tkinter` |
| Rocky Linux 9 | `sudo dnf install python3.12 python3.12-tkinter` |
| AlmaLinux 9 | `sudo dnf install python3.12 python3.12-tkinter` |
| openSUSE | `sudo zypper install python3-tk` |
| Alpine | `sudo apk add python3-tkinter` |
| Arch Linux | `sudo pacman -S tk` |
| Manjaro | `sudo pacman -S tk` |
| Gentoo | Python built with the `tk` USE flag |

On RHEL 9 and its rebuilds, `python3` is Python 3.9, older than pytktable requires, so use
`python3.12`. Most of these are tested with the prebuilt Tktable (see
[Testing](https://github.com/nbro/pytktable-binaries/blob/main/docs/testing.md)). If tkinter
still doesn't work, see {doc}`troubleshooting`.

(prebuilt-tktable)=
## With prebuilt Tktable (recommended)

```sh
pip install "pytktable[binary]"
```

Keep the quotes: some shells, e.g. zsh (the default on macOS), would otherwise treat the brackets
as a file pattern. This also installs
[pytktable-binaries](https://github.com/nbro/pytktable-binaries), which contains [Tktable](https://wiki.tcl-lang.org/page/Tktable), the Tcl/Tk extension that provides the table
widget, compiled for Tcl/Tk 8.6 and 9.0 for:

| OS | Architectures |
|---|---|
| Linux with glibc 2.28 or newer (most distributions, e.g. Debian 10+, Ubuntu 20.04+, RHEL 8+) | x86_64, ARM (aarch64) |
| Linux with musl (e.g. Alpine) | x86_64, ARM (aarch64) |
| macOS 11 and later | Intel, Apple silicon |
| Windows | x64, x86, ARM |

See [Platforms](https://github.com/nbro/pytktable-binaries/blob/main/docs/platforms.md) for where
they are tested.

pytktable finds it automatically, so you don't need to install Tktable or set `TKTABLE_LIBRARY`.
You only need tkinter ({ref}`see above <check-tkinter>`). Tktable also needs the X11 library
(`libX11`), which every desktop Linux has.

(without-prebuilt-tktable)=
## Without prebuilt Tktable

Install only the Python wrapper, and Tktable yourself, if:

- your platform is not in the list above (e.g. 32-bit ARM Linux, FreeBSD);
- you prefer the Tktable of your OS's package manager;
- the prebuilt Tktable doesn't work for you (please
  [report it](https://github.com/nbro/pytktable-binaries/issues)).

```sh
pip install pytktable
```

Then install these, which `pip install pytktable` does not install:

1. [Tcl](https://www.tcl-lang.org/) and [Tk](https://wiki.tcl-lang.org/page/Tk), and
   {py:mod}`tkinter`;
2. [Tktable](https://wiki.tcl-lang.org/page/Tktable). It usually does not come with Tk.

How to install them depends on your OS:

- [Linux](linux.md)
- [macOS](macos.md)
- [Windows](windows.md)
- [Other systems](other-systems.md): FreeBSD, OpenBSD, NetBSD and conda

Tktable from different sources isn't always the same version, so it can behave slightly
differently: e.g. the default colors of the title rows of the prebuilt Tktable (2.12) and of
Tktable 2.11, from [apnadkarni/tktable](https://github.com/apnadkarni/tktable), which older
Magicsplat releases had, differ. Magicsplat's latest releases (1.18.0 and 2.0.7) have Tktable
2.12.1, from [bohagan1/TkTable](https://github.com/bohagan1/TkTable), like the prebuilt one.

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

```{toctree}
:hidden:

linux
macos
windows
other-systems
troubleshooting
```
