# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- A History page in the docs: where Tcl/Tk, `tkinter` and Tktable come from.

### Changed

- When Tktable cannot be loaded, the tests show the error of every try, and print a
  `Tktable load report` at the end, with Tcl's stack trace, what Tcl knows about Tktable and the
  files in `TKTABLE_LIBRARY`, to find the cause of the flaky failures on Windows.

## [0.3.0] - 2026-11-04

### Added

- `pip install "pytktable[binary]"` also installs Tktable, prebuilt for Linux, macOS and Windows
  ([pytktable-binaries](https://github.com/nbro/pytktable-binaries)). pytktable finds it
  automatically, without installing Tktable or setting `TKTABLE_LIBRARY`.

### Changed

- The installation docs recommend `pip install "pytktable[binary]"`, and keep the instructions to
  install Tktable yourself for platforms without prebuilt Tktable, or if you prefer your OS's.

## [0.2.0] - 2026-11-04

### Added

- Type hints on the whole library, checked by mypy, and a `py.typed` marker so your type checker
  and IDE use them (#21). Callbacks receive a documented `TableEvent`.

- Windows installation docs: install Tktable with Magicsplat Tcl/Tk and set `TKTABLE_LIBRARY`,
  tested in CI with Python 3.11 to 3.15 (Tcl 8.6 and 9.0).
  Covers winget (Tcl 8.6), Chocolatey (Tcl 8.6 and 9.0) and Magicsplat's installer.
- A screenshot of the example, and a list of features, in the README and the docs.
- A warning at the top of the README and the docs that Tktable must be installed separately.
- One small example per feature (e.g. `examples/tags.py`), each describing itself in its window,
  listed in the docs, and a test that runs every example in CI.

### Changed

- The library only uses tkinter's public API, instead of private helpers (`_w`, `_register`,
  `_flatten`, ...) that may change between Python versions.

- The `tags.py` example explains tag priority correctly (the tag created first wins) and shows
  how to style a single title cell with `tag_raise()` (#5). A new `flash.py` example shows the
  red flash on changed cells (`flashmode`) and how to restyle or avoid it (#5).

- The examples are run as modules from the repository's root, e.g.
  `poetry run python -m examples.planets`, and share their window setup (`examples/window.py`).
- The example shows real data, the 8 planets from NASA's Planetary Fact Sheet, saved in
  `examples/data/planets.json` (refresh it with `poetry run poe update_example_data`). It is an
  editable table with a modern look: larger fonts, the native ttk theme, sharp text on high-DPI
  Windows screens, and the window centered on screen, never smaller than its contents, with the
  table growing with the window.
  Editing works like a spreadsheet: Left/Right move within the cell, Tab/Shift+Tab move between
  cells, Enter moves down, and clicking puts the cursor where you click.
- `python -m tktable` prints Tcl's `auto_path` as one plain folder per line.

## [0.1.0] - 2026-11-03

First release on PyPI. These changes were made with the help of
[Claude](https://claude.ai) (Anthropic), and reviewed by the maintainer.

### Fixed

- `Table` crashed on Python >= 3.10 when given any callback option (e.g. `command`,
  `browsecmd`), because `collections.Callable` was removed in Python 3.10.
  It now uses `callable()`.
- `ArrayVar.unset()` without a pattern passed `None` to Tcl instead of unsetting all
  elements.
- `ArrayVar.get()` (without a key) failed with `TypeError` on modern Python/tkinter, which
  returns Tcl lists as `Tcl_Obj`; `ArrayVar.names()` could return a `Tcl_Obj` for the same reason.
- `Table.tag_lower()` did not pass the tag name to Tcl, so it always failed.
- `Table.height(0)` returned the heights of all rows instead of the height of row 0.

### Added

- `python -m tktable`: diagnoses whether tkinter, Tcl/Tk and Tktable can be found and
  loaded, and prints the Tcl version, `TKTABLE_LIBRARY` and Tcl's `auto_path`. It works
  without a display (e.g. in CI) and without tkinter installed.
- Documentation (Sphinx + Markdown), published to GitHub Pages: installation per OS, usage,
  API reference (one page per module), development and releasing.
- Tests (pytest) for `ArrayVar`, `Table`, `tktable.utils` and the diagnostic. Tests that need Tktable are
  skipped when it is missing, or fail if `TKTABLE_REQUIRED=1`.
- Development commands (set up, format, check, test, docs, ...) as [Poe the Poet](https://pypi.org/project/poethepoet/)
  tasks in `pyproject.toml`, the same on Linux, macOS and Windows. Run `poetry run poe` to list
  them.
- GitHub Actions workflows:
  - tests on Linux, macOS and Windows with Python 3.11 to 3.15, plus quality checks;
  - tests in Debian and Ubuntu containers using their Tktable packages;
  - an experimental job testing Magicsplat's Tktable with python.org's Python on Windows;
  - release to PyPI (Trusted Publishing) and GitHub when a version tag is pushed.
- Dockerfiles (`docker/`) to run the tests with each Linux distro's own packages, and docs on
  running the example in the Ubuntu container on Windows (WSLg) and Linux, without installing
  Tktable.
- pre-commit hooks that run all quality checks on every commit (install them with
  `poetry run pre-commit install`): the Poe check tasks (lock file, isort, black, mypy, pylint),
  YAML linting (yamllint), secret scanning (gitleaks) and security checks (bandit).
- `AGENTS.md`: code style and workflow guidelines for contributors and AI agents.
- README: badges, short description and installation, pointing to the documentation.

### Changed

- Published on PyPI as `pytktable`, because `tktable` is taken by an unrelated project.
  The import name is still `tktable`.
- Requires Python >= 3.11.
- `pyproject.toml` uses the standard `[project]` table (Poetry 2); dev dependencies
  updated.
- `CannotUseError` now tells users to run `python -m tktable` and links to the README.
- Loading Tktable (including `TKTABLE_LIBRARY` support) moved to `tktable.utils`, shared
  by `Table` and the diagnostic.
- The library logs at `DEBUG` level instead of `INFO`; the example logs instead of printing.
- `tktable/__init__.py` imports `ArrayVar` and `Table` lazily, so the diagnostic works
  without tkinter (explained in the module docstring).

[Unreleased]: https://github.com/nbro/tktable/compare/0.3.0...HEAD
[0.3.0]: https://github.com/nbro/tktable/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/nbro/tktable/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/nbro/tktable/releases/tag/0.1.0
