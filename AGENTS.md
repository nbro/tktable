# Guidelines for contributors and AI agents

These apply to everyone changing this repository, people and AI coding agents alike.

## Readability first

Code is read far more often than it is written, by people and by agents. Prefer the version that is
easiest to understand.

- Separate logical steps with blank lines: inside functions, between workflow steps, between
  sections of a config file.
- Write modular code: small functions that each do one thing, with clear names. But don't make it
  too abstract: no layers, classes or helpers that don't pay for themselves.
- Keep lines at most 100 characters (120 in YAML).
- Put comments on their own line above the code they explain, and explain *why*, not *what*.
- Don't put long scripts inline in GitHub workflows: move them to `.github/scripts/`.

## Tools

- Use reliable, stable tools. No betas, and no new tool when an existing one does the job.
- Commands are Poe tasks in `pyproject.toml`; run `poetry run poe` to list them. Define a command
  once, and reuse it (pre-commit and CI call the Poe tasks).
- Run `poetry run pre-commit run --all-files` before pushing; the hooks also run on every commit
  once installed with `poetry run pre-commit install`.

## Commits

- Start the subject with an imperative verb, as if completing "This commit will ...": "Fix ...",
  "Add ...", "Make ...", not "Fixed ..." or "Fixes ...".
- Keep the subject at most 72 characters, without a final period. Explain *why* in the body if it
  isn't obvious.

## Code

- Python >= 3.11, with type hints on new code.
- Use `logging` in the library, never `print` (except in the `python -m tktable` diagnostic, whose
  output is its result).
- Add or update tests for every fix or feature, and the docs and `CHANGELOG.md` when behavior
  changes.

## Docs

- Markdown (MyST) in `docs/`. One command per code block, with explanations outside the block.
- Separate pages for Linux/macOS and Windows instructions when they differ.
