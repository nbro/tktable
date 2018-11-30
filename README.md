# tktable

[![Python 2, 3](https://img.shields.io/badge/python-2%2C%203-blue.svg)](https://www.python.org/downloads/)
[![license](https://img.shields.io/badge/license-BSD%202--Clause-orange.svg)](./LICENSE.md)

This is a wrapper library for Python of the homonymous Tcl/Tk library written by [Guilherme Polo](https://github.com/gpip).

## Notes and warnings

- This is a wrapper library of an **extension library** for the [Tk widget toolkit](https://en.wikipedia.org/wiki/Tk_(software)). This means that before using this Python module you need to have installed the corresponding Tk library.
- on windows the Tk toolkit can be found as part of the [ActiveTcl] (https://www.activestate.com/products/activetcl/) distribution, ensure you download the same version as your python install (32 bit or 64 bit)
- The original tktable library could not be anymore maintained or maintained rarely and this also means that if you need support about it or you want to report a bug, nobody could listen to you. Use this library at your own risk!

- This repository only tries to _make more visible_ this wrapper library to Python users. Eventually it can also be a good way to _start maintaining it_ and a _help center_ for the Python community that would like to use this library.

## How to use?

This package is still not on PyPI, even though my intention is to upload it there too.

For now, just copy the file [`tktable.py`](tktable.py) to your working directory and import `tktable.py` normally. You could also, for example, copy the module to the `site-packages` folder under your Python distribution, so that you don't have to copy everytime the module to all your projects.

## Resources and help

- [http://tktable.sourceforge.net/](http://tktable.sourceforge.net/)

- [http://wiki.tcl.tk/1877](http://wiki.tcl.tk/1877)

- [http://www.tcl.tk/community/hobbs/tcl/](http://www.tcl.tk/community/hobbs/tcl/)

- [http://tkinter.unpythonic.net/wiki/TkTableWrapper](http://tkinter.unpythonic.net/wiki/TkTableWrapper)

- [http://tkinter.unpythonic.net/wiki/TkTable](http://tkinter.unpythonic.net/wiki/TkTable)

### Search for tktable on Stack Overflow

- [http://stackoverflow.com/search?q=tktable](http://stackoverflow.com/search?q=tktable)

### Search for tktable on Google

- [https://www.google.com/search?q=tktable](https://www.google.com/search?q=tktable)


## TODO 

- Upload this repository to PyPI

    - Before that we may need first to provide an automated way of installing the dependencies of this library, i.e., I'm referring to an automatic installation of the original Tk extension.

- Write more examples of how to use this module