# Installation on Windows

The python.org installers for Windows include tkinter, Tcl and Tk: Tcl 8.6 up to Python 3.13, and
Tcl 9.0 from Python 3.14.

## Install Tktable

Tktable comes with [Magicsplat Tcl/Tk for Windows](https://magicsplat.com/tcl-installer), a Tcl/Tk
distribution by a member of the Tcl Core Team. Its Tktable works with python.org's Python, as long
as its Tcl major version matches your Python's: Magicsplat 1.x has Tcl 8.6, and 2.x has Tcl 9.0.

Check which Tcl version your Python uses:

```powershell
python -c "import tkinter; print(tkinter.TclVersion)"
```

Then install Magicsplat in one of the ways below, and
{ref}`point TKTABLE_LIBRARY at its Tktable <point-tktable-library>`.

### With winget (Tcl 8.6)

[winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) comes with Windows 11.
It only has Magicsplat 1.x, so it only works for Python 3.11 to 3.13 (Tcl 8.6):

```powershell
winget install Magicsplat.TclTk
```

It installs for your user, with Tktable in `%LOCALAPPDATA%\Apps\Tcl86\lib\Tktable2.12`.

### With Chocolatey (Tcl 8.6 or 9.0)

[Chocolatey](https://chocolatey.org/) has both Magicsplat 1.x and 2.x. If it is not installed, you
can install it with winget, from an administrator PowerShell:

```powershell
winget install -e --id Chocolatey.Chocolatey
```

Or follow [Chocolatey's install instructions](https://chocolatey.org/install). winget and Chocolatey
can be installed together; just don't install the same app with both.

Then, from an administrator PowerShell, install the release that matches your Python. For
Tcl 8.6, that is Python 3.11 to 3.13:

```powershell
choco install magicsplat-tcl-tk --version 1.16.0
```

For Tcl 9.0, that is Python 3.14 and later:

```powershell
choco install magicsplat-tcl-tk --version 2.0.6
```

These are the versions tested in CI. They install for all users, with Tktable in
`C:\Program Files\Tcl\lib\Tktable2.12`.

### With Magicsplat's installer

Download the installer of the release that matches your Python from
[Magicsplat's site](https://magicsplat.com/tcl-installer), and run it. Tktable is in the `lib`
folder of where you install it, e.g. `lib\Tktable2.12`.

(point-tktable-library)=
### Point TKTABLE_LIBRARY at Tktable

If you don't know where Tktable was installed, find it:

```powershell
Get-ChildItem "C:\Program Files", "$env:LOCALAPPDATA" -Recurse -Filter pkgIndex.tcl -ErrorAction SilentlyContinue | Where-Object DirectoryName -match "Tktable" | Select-Object -ExpandProperty DirectoryName
```

Save {ref}`TKTABLE_LIBRARY <tktable-library>` for your user, so new terminals see it. For example,
after installing with winget:

```powershell
[Environment]::SetEnvironmentVariable("TKTABLE_LIBRARY", "$env:LOCALAPPDATA\Apps\Tcl86\lib\Tktable2.12", "User")
```

This doesn't change the terminal you're in. Either open a new one, or also set it there:

```powershell
$env:TKTABLE_LIBRARY = "$env:LOCALAPPDATA\Apps\Tcl86\lib\Tktable2.12"
```

## Check the installation

```powershell
python -m tktable
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
