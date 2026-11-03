# Installation on Windows

The python.org installers for Windows include tkinter, Tcl and Tk: Tcl 8.6 up to Python 3.13, and
Tcl 9.0 from Python 3.14.

## Install Tktable

There is no official way to install Tktable for python.org's Python yet
([#1](https://github.com/nbro/tktable/issues/1)). CI shows that a Tktable built for the same Tcl
major version (8.6 or 9.0) as your Python can be used, by pointing
{ref}`TKTABLE_LIBRARY <tktable-library>` at it (see below). An experimental CI job is testing
[Magicsplat Tcl/Tk](https://magicsplat.com/tcl-installer)'s Tktable as such a source; this page will
be updated with the results.

## Check the installation

```powershell
python -m tktable
```

## Tktable in a non-standard location

Set {ref}`TKTABLE_LIBRARY <tktable-library>` in PowerShell for the current session:

```powershell
$env:TKTABLE_LIBRARY = "C:\path\to\Tktable2.12.1"
```

(try-in-docker-windows)=
## Try the example without installing Tktable

With [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows 11 (or Windows 10
build 19044 or later), you can run [the example](../usage.md) in an Ubuntu container, which has
Python, Tk and Tktable. Its window opens on your desktop through
[WSLg](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

From the repository's root in PowerShell, build the image:

```powershell
docker build -f docker/Dockerfile.ubuntu -t tktable-test:ubuntu .
```

Run the example:

```powershell
docker run --rm -e DISPLAY=:0 -v /run/desktop/mnt/host/wslg/.X11-unix:/tmp/.X11-unix tktable-test:ubuntu python examples/example1.py
```

If no window opens, run the same image from a WSL shell instead, where WSLg sets `DISPLAY`:

```bash
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix tktable-test:ubuntu python examples/example1.py
```
