# pylint: disable=missing-module-docstring, redefined-outer-name
from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

try:
    import tkinter

    from tktable.utils import load_tktable
except ImportError:  # Only test_main.py can run without tkinter.
    collect_ignore = ["test_array_var.py", "test_examples.py", "test_table.py", "test_utils.py"]

#: Set to 1 (e.g. in CI) to fail, instead of skip, the tests that need Tktable.
TKTABLE_REQUIRED = os.environ.get("TKTABLE_REQUIRED") == "1"


@pytest.fixture(scope="session")
def session_root() -> Iterator[tkinter.Tk | str]:
    """One Tk interpreter for the whole test session, or why it can't start.

    Creating one per test is slow, and on Windows CI, Tcl's startup occasionally fails when many
    interpreters are created and destroyed in a row.
    """
    try:
        tk = tkinter.Tk()
    except tkinter.TclError as exc:
        yield f"Tk cannot start (no display?): {exc}"
        return
    tk.withdraw()
    yield tk
    tk.destroy()


@pytest.fixture(scope="session")
def session_tktable_error(session_root: tkinter.Tk | str) -> str:
    """Why Tktable cannot be loaded, or "" if it can, checked once for the whole session.

    The reason is kept, so a test that fails or is skipped without Tktable shows Tcl's error.
    """
    if isinstance(session_root, str):
        return session_root
    try:
        load_tktable(session_root)
    except tkinter.TclError as exc:
        auto_path = session_root.tk.splitlist(session_root.tk.call("set", "auto_path"))
        return f"{exc} (TKTABLE_LIBRARY={os.environ.get('TKTABLE_LIBRARY')}, auto_path={auto_path})"
    return ""


@pytest.fixture
def root(session_root: tkinter.Tk | str) -> Iterator[tkinter.Tk]:
    """The session's Tk root; the widgets a test creates in it are destroyed after the test."""
    if isinstance(session_root, str):
        pytest.skip(session_root)
    yield session_root
    for widget in session_root.winfo_children():
        widget.destroy()


@pytest.fixture
def table_root(root: tkinter.Tk, session_tktable_error: str) -> tkinter.Tk:
    """A Tk root in which Tktable is loaded."""
    if session_tktable_error:
        if TKTABLE_REQUIRED:
            pytest.fail(f"Tktable is required (TKTABLE_REQUIRED=1) but: {session_tktable_error}")
        pytest.skip(f"Tktable cannot be loaded: {session_tktable_error}")
    return root
