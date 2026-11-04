# Installation on Linux and macOS

These instructions are for installing Tktable yourself, with `pip install pytktable`. With
`pip install "pytktable[binary]"`, you don't need them: see {ref}`prebuilt-tktable`.

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

(try-in-docker-linux)=
## Try the example without installing Tktable

On Linux with [Docker](https://docs.docker.com/engine/install/), you can run
[the example](../usage.md) in an Ubuntu container, which has Python, Tk and Tktable. Its window opens
on your X11 desktop (or Wayland, through XWayland).

From the repository's root, build the image:

```sh
docker build -f docker/Dockerfile.ubuntu -t tktable-test:ubuntu .
```

Allow local containers to open windows on your display:

```sh
xhost +local:
```

Run the example:

```sh
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix tktable-test:ubuntu python -m examples.planets
```

On macOS this needs an X server such as [XQuartz](https://www.xquartz.org/), and is untested.
