# pylint: disable=missing-module-docstring, missing-function-docstring, redefined-outer-name
from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

try:
    import tkinter

    from tktable.utils import load_tktable
except ImportError:  # Only test_main.py can run without tkinter.
    collect_ignore = ["test_array_var.py", "test_table.py", "test_utils.py"]

#: Set to 1 (e.g. in CI) to fail, instead of skip, the tests that need Tktable.
TKTABLE_REQUIRED = os.environ.get("TKTABLE_REQUIRED") == "1"


@pytest.fixture
def root() -> Iterator[tkinter.Tk]:
    try:
        tk = tkinter.Tk()
    except tkinter.TclError as exc:
        pytest.skip(f"Tk cannot start (no display?): {exc}")
    tk.withdraw()
    yield tk
    tk.destroy()


def tktable_available(tk: tkinter.Tk) -> bool:
    try:
        load_tktable(tk)
    except tkinter.TclError:
        return False
    return True


@pytest.fixture
def table_root(root: tkinter.Tk) -> tkinter.Tk:
    """A Tk root in which Tktable is loaded."""
    if not tktable_available(root):
        if TKTABLE_REQUIRED:
            pytest.fail("Tktable is required (TKTABLE_REQUIRED=1) but cannot be loaded")
        pytest.skip("Tktable is not installed")
    return root
