# pytktable

[![PyPI](https://img.shields.io/pypi/v/pytktable)](https://pypi.org/project/pytktable/)
[![Python](https://img.shields.io/pypi/pyversions/pytktable)](https://pypi.org/project/pytktable/)
[![Tests](https://github.com/nbro/tktable/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/nbro/tktable/actions/workflows/tests.yml)
[![Docs](https://github.com/nbro/tktable/actions/workflows/docs.yml/badge.svg?branch=main)](https://nbro.github.io/tktable/)
[![License](https://img.shields.io/badge/license-BSD%202--Clause-orange.svg)](LICENSE.md)

A spreadsheet-like table widget for tkinter, wrapping the Tcl/Tk
[Tktable](https://wiki.tcl-lang.org/page/Tktable) extension.

The wrapper was originally written by [Guilherme Polo](https://github.com/gpip).

## Installation

```sh
pip install pytktable
```

It is imported as `tktable` (`from tktable import Table`). It also needs the Tktable extension,
which `pip` does not install: see [Installation](https://nbro.github.io/tktable/installation/)
for how to install it on your OS, and run `python -m tktable` to check that it works.

## Documentation

<https://nbro.github.io/tktable/>: usage, API reference, development and releasing.

## License

[BSD 2-Clause](LICENSE.md).

Copyright (c) 2008, Guilherme Polo\
Copyright (c) 2016-2026, nbro

See the [changelog](CHANGELOG.md) for what changed in this fork.
