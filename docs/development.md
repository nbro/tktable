# Development

The project uses [Poetry](https://python-poetry.org/) for dependencies and packaging, and
[Poe the Poet](https://pypi.org/project/poethepoet/) for the common commands. They are defined in
`pyproject.toml` (`[tool.poe.tasks]`) and work the same on Linux, macOS and Windows.

## Set up

Install Poetry, if it is not installed, following its
[installation guide](https://python-poetry.org/docs/#installation). Then, from the repository's
root, create the virtual environment and install the dependencies, including Poe:

```sh
poetry install
```

To list all commands:

```sh
poetry run poe
```

Install the [pre-commit](https://pre-commit.com/) hooks, so the quality checks run automatically on
every `git commit` and a commit that fails them is refused:

```sh
poetry run pre-commit install
```

## Format and check

Format Python (isort, black):

```sh
poetry run poe format
```

Run the quality checks (lock file, formatting, types, style):

```sh
poetry run poe check
```

`check` runs, in order:

1. `check_lock`: `poetry.lock` is consistent with `pyproject.toml`;
2. `check_format`: Python is formatted with isort and black;
3. `check_types`: type checks with mypy;
4. `check_style`: style checks with pylint.

Each of them can also be run on its own, e.g. `poetry run poe check_types`.

The pre-commit hooks (`.pre-commit-config.yaml`) run these Poe tasks, and also check file hygiene
(trailing whitespace, final newlines, valid YAML and TOML, no large files), lint YAML
([yamllint](https://yamllint.readthedocs.io/)), scan for secrets
([gitleaks](https://github.com/gitleaks/gitleaks)) and check security
([bandit](https://bandit.readthedocs.io/)). On a commit, a hook only runs if the commit changes
files it checks. If a hook fixes files (e.g. trailing whitespace), add them and commit again.

To run all hooks on all files, as CI does:

```sh
poetry run pre-commit run --all-files
```

Tests are not hooks, because they need a display and take longer; CI runs them.

## Tests

```sh
poetry run poe test
```

Tests that need Tktable are skipped when it is missing. Set `TKTABLE_REQUIRED=1` to make them fail
instead, as CI does when Tktable is installed.

On Linux without a display (e.g. a server), Tk needs a virtual one, from
[`xvfb-run`](https://manpages.debian.org/xvfb-run):

```sh
xvfb-run -a poetry run poe test
```

To diagnose Tktable:

```sh
poetry run poe check_tktable
```

To test with the Python, Tcl, Tk and Tktable packages of Debian and Ubuntu, in Docker (on Windows
and macOS, with [Docker Desktop](https://www.docker.com/products/docker-desktop/)):

```sh
poetry run poe docker_test
```

To test with only one of them, use `docker_debian` or `docker_ubuntu`:

```sh
poetry run poe docker_debian
```

## Documentation

The docs are written in Markdown ([MyST](https://myst-parser.readthedocs.io/)) and built with
[Sphinx](https://www.sphinx-doc.org/). The API pages are generated from the docstrings. This builds
them into `docs/_build/html` (warnings are errors) and prints the link to open them:

```sh
poetry run poe docs
```

## Dependencies

Upgrade the dev and docs dependencies to their latest versions:

```sh
poetry run poe upgrade_dev_deps
```

## Example data

The example's data, `examples/data/planets.json`, comes from NASA's
[Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html). It is saved in
the repository, so the example works offline. To download it again, then review the changes with
`git diff`:

```sh
poetry run poe update_example_data
```

## Clean

Remove build and test artifacts, including the built docs:

```sh
poetry run poe clean
```

## Continuous integration

GitHub Actions workflows in `.github/workflows/`, which use the same Poe commands. Longer steps are
scripts in `.github/scripts/`. All run on pushes to `main`, and all but
`windows-magicsplat.yml` on pull requests to `main`:

- `tests.yml`: quality checks (all pre-commit hooks), and tests on Linux, macOS and Windows with
  Python 3.11 to 3.15 (on pull requests, only the oldest, 3.11, to keep them fast);
- `docker.yml`: tests in Debian and Ubuntu containers, with their own Python, Tk and Tktable;
- `windows-magicsplat.yml`: tests the documented Windows installation, python.org's Python with
  [Magicsplat](https://magicsplat.com/tcl-installer)'s Tktable (not on pull requests);
- `docs.yml`: builds the docs, and publishes them to GitHub Pages on pushes to `main`;
- `release.yml`: see [Releasing](releasing.md).
