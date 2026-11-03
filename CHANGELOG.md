# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased] - 0.1.0

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
- Dockerfiles (`docker/`) to run the tests with each Linux distro's own packages.
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
