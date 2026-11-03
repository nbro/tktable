# Releasing

Releases are published to [PyPI](https://pypi.org/project/pytktable/) and GitHub by the
`release.yml` workflow when a version tag is pushed.

## One-time setup

1. On PyPI, add a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) for the project
   `pytktable`: owner `nbro`, repository `tktable`, workflow `release.yml`, environment `pypi`.
   This lets the workflow publish without an API token.
2. On GitHub, create the environment `pypi` (Settings → Environments).

## Release a version

1. Update the version in `pyproject.toml`, e.g. `poetry version 0.2.0` (or `patch`, `minor`,
   `major`).
2. Move the entries under *Unreleased* in `CHANGELOG.md` to a section for the new version.
3. Commit, then tag the commit with the same version:

   ```sh
   git tag 0.2.0
   ```

4. Push the commit and the tag:

   ```sh
   git push origin main 0.2.0
   ```

The workflow then:

1. runs the tests;
2. checks that the tag equals the version in `pyproject.toml`;
3. builds the sdist and wheel;
4. publishes them to PyPI;
5. creates a GitHub release with the files and generated release notes. Versions that are not plain
   `X.Y.Z` (e.g. `0.2.0rc1`) are marked as pre-releases.
