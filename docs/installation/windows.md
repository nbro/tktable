# Installation on Windows

The python.org installers for Windows include tkinter, Tcl and Tk: Tcl 8.6 up to Python 3.13, and
Tcl 9.0 from Python 3.14.

## Install Tktable

Tktable comes with [Magicsplat Tcl/Tk for Windows](https://magicsplat.com/tcl-installer), a Tcl/Tk
distribution by a member of the Tcl Core Team. Its Tktable works with python.org's Python, as long
as its Tcl major version matches your Python's (CI tests this with Python 3.11 to 3.15).

Check which Tcl version your Python uses:

```powershell
python -c "import tkinter; print(tkinter.TclVersion)"
```

Install Magicsplat with [Chocolatey](https://chocolatey.org/), choosing the release that matches:
1.x for Tcl 8.6, 2.x for Tcl 9.0. These are the versions tested in CI. For Tcl 8.6 (Python 3.11 to
3.13):

```powershell
choco install magicsplat-tcl-tk --version 1.16.0
```

For Tcl 9.0 (Python 3.14 and later):

```powershell
choco install magicsplat-tcl-tk --version 2.0.6
```

You can also download the installer from [Magicsplat's site](https://magicsplat.com/tcl-installer);
the folder below may then differ.

Point {ref}`TKTABLE_LIBRARY <tktable-library>` at Magicsplat's Tktable, for your user, permanently:

```powershell
[Environment]::SetEnvironmentVariable("TKTABLE_LIBRARY", "C:\Program Files\Tcl\lib\Tktable2.12", "User")
```

Then open a new terminal, so it sees the variable, and check the installation (below).

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
