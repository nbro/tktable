# Installation on Linux

These instructions are for installing Tktable yourself, with `pip install pytktable`. With
`pip install "pytktable[binary]"`, you don't need them: see {ref}`prebuilt-tktable`.

## Install## Install tkinter and Tktable

On Debian and its derivatives, e.g. Ubuntu, Linux Mint and Kali Linux:

```sh
sudo apt install python3-tk tk-table
```

On Gentoo, with Python built with the `tk` USE flag:

```sh
sudo emerge dev-tcltk/tktable
```

On other distributions, look for a package called `tktable` or `tk-table`. These are the ones we
know of:

| Distribution | Package | Version | Notes |
|---|---|---|---|
| Debian, Ubuntu, Linux Mint | [`tk-table`](https://community.linuxmint.com/software/view/tk-table) | | |
| Kali Linux | [`tk-table`](https://pkg.kali.org/pkg/tk-table) | 2.10.8 | From Debian |
| Gentoo | [`dev-tcltk/tktable`](https://packages.gentoo.org/packages/dev-tcltk/tktable) | 2.12.1 | |
| Slackware | [`tktable`](https://slackbuilds.org/repository/15.0/development/tktable/) (SlackBuild) | 2.10.8 | Built from source |
| Fedora, RHEL, CentOS, Rocky Linux | none | | Use the prebuilt Tktable |

`perl-Tk-TableMatrix` (Fedora, Arch Linux, Manjaro) is a different table widget, for Perl/Tk, not
Tktable. For distributions without a package, use the prebuilt Tktable
({ref}`prebuilt-tktable`), [conda](other-systems.md#conda), or build Tktable from source.

he installation

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
