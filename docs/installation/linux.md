# Installation on Linux

These instructions are for installing Tktable yourself, with `pip install pytktable`. With
`pip install "pytktable[binary]"`, you don't need them: see {ref}`prebuilt-tktable`.

## Install tkinter and Tktable

Where the distribution has a Tktable package, install it with tkinter:

| Distribution | Command | Tktable version |
|---|---|---|
| Debian, Ubuntu, Linux Mint, Kali Linux | `sudo apt install python3-tk tk-table` | 2.10.8 ([Kali](https://pkg.kali.org/pkg/tk-table)) |
| Gentoo | `sudo emerge dev-tcltk/tktable`, with Python built with the `tk` USE flag | [2.12.1](https://packages.gentoo.org/packages/dev-tcltk/tktable) |
| Slackware | the [`tktable` SlackBuild](https://slackbuilds.org/repository/15.0/development/tktable/), built from source | 2.10.8 |

Fedora, RHEL and its rebuilds (CentOS, Rocky Linux, AlmaLinux), openSUSE, Alpine and Arch Linux
have no Tktable package that we know of: there, install only tkinter
([see the commands](index.md#prebuilt-tktable)) and use the prebuilt Tktable, or
[conda](other-systems.md#conda). `perl-Tk-TableMatrix` (Fedora, Arch Linux, Manjaro) is a
different table widget, for Perl/Tk, not Tktable.

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
