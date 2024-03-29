# tktable

[![license](https://img.shields.io/badge/license-BSD%202--Clause-orange.svg)](./LICENSE.md)

This is a wrapper library for Python of the homonymous Tcl/Tk library written by [Guilherme Polo](https://github.com/gpip).

## Dependencies

You need to install a few dependencies (or make sure they are already installed) to use this wrapper library.

1. [Tcl](https://www.tcl.tk/software/tcltk/) (a programming language)
2. [Tk](https://wiki.tcl-lang.org/page/Tk) (a cross-platform windowing toolkit for Tcl)
3. [Tkinter](https://docs.python.org/3/library/tkinter.html) (the Python wrapper around Tk)
4. [TkTable](https://wiki.tcl-lang.org/page/Tktable) (the Tcl library that extends Tk, so it doesn't usually come with Tk)

If those dependencies are satisfied, you can proceed. It might be the case that some, all or none of these dependencies are installed, so you need to install them, because this package does not install them for you.

## How to use?

TODO

## WARNINGS

- It can be difficult to use this library because it depends on other external libraries ([Tcl](http://www.tcl.tk/community/hobbs/tcl/), Tk and TkTable), which might not be installed on your system. Even if they are installed, they might not be linked correctly. 

- This repository tries to _make more visible_ this wrapper library to Python users. However, it's not under development or really maintained, so don't expect someone to help you if you encounter a problem.

- The original Tk extension, TkTable, is also not developed anymore. The last time it was modified was in 2008. See [this](https://sourceforge.net/projects/tktable/files/tktable/) and [this](https://chiselapp.com/user/pooryorick/repository/tktable/brlist)

## Installation issues

The issue tracker contains some potentially useful info on how to solve certain installation issues. In particular, read [this comment](https://github.com/nbro/tktable/issues/1#issuecomment-244519589).

## Development

I use [poetry](https://python-poetry.org/) to manage the dependencies and packaging.

## TODO

See [here](https://github.com/nbro/tktable/issues/7).