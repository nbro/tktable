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

# GitHub's logo (the "mark-github" Octicon), in the format Furo's footer icons expect.
GITHUB_ICON = (
    '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">'
    '<path fill-rule="evenodd" d="'
    "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-."
    "01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.6"
    "3-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89"
    "-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1"
    ".32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.8"
    "2 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2."
    "2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"
    '"></path>'
    "</svg>"
)

html_theme = "furo"
html_title = f"pytktable {release}"
html_theme_options = {
    "source_repository": "https://github.com/nbro/tktable/",
    "source_branch": "main",
    "source_directory": "docs/",
    # A GitHub icon in the footer of every page, linking to the repository.
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/nbro/tktable",
            "html": GITHUB_ICON,
            "class": "",
        },
    ],
}
