"""Sphinx configuration. Build with: poetry run poe docs"""

# pylint: disable=invalid-name

from importlib.metadata import version as _version

project = "pytktable"
author = "Guilherme Polo, nbro"
copyright = "2008, Guilherme Polo; 2016-2026, nbro"  # pylint: disable=redefined-builtin
release = _version("pytktable")
version = release

extensions = [
    "myst_parser",  # Markdown pages
    "sphinx.ext.autodoc",  # API pages from docstrings
    "sphinx.ext.intersphinx",  # links to the Python docs (e.g. tkinter types)
    "sphinx.ext.viewcode",  # "[source]" links
    "sphinx_copybutton",  # copy button on code blocks
]

source_suffix = {".md": "markdown"}
exclude_patterns = ["_build"]

# Every heading up to level 3 gets an anchor, so sections can be linked to.
myst_heading_anchors = 3
myst_enable_extensions = ["colon_fence", "deflist"]

autodoc_default_options = {"members": True, "show-inheritance": True}
autodoc_member_order = "bysource"
autodoc_typehints = "description"

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

html_theme = "furo"
html_title = f"pytktable {release}"
html_theme_options = {
    "source_repository": "https://github.com/nbro/tktable/",
    "source_branch": "main",
    "source_directory": "docs/",
}
