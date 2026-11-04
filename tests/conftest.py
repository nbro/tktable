# pylint: disable=missing-module-docstring, redefined-outer-name
from __future__ import annotations

import os
import time
from collections.abc import Iterator
from pathlib import Path

import pytest

try:
    import tkinter

    from tktable.utils import load_tktable
except ImportError:  # Only test_main.py can run without tkinter.
    collect_ignore = ["test_array_var.py", "test_examples.py", "test_table.py", "test_utils.py"]

#: Set to 1 (e.g. in CI) to fail, instead of skip, the tests that need Tktable.
TKTABLE_REQUIRED = os.environ.get("TKTABLE_REQUIRED") == "1"

#: How many times to try to load Tktable, and how many seconds to wait between tries.
#: On GitHub's Windows runners, loading Tktable sometimes fails right after it was installed, most
#: likely while the antivirus is still scanning the new files: Tcl finds pkgIndex.tcl but can't read
#: it ("couldn't read file ... no such file or directory"), or runs it but Tktable isn't provided
#: ("no version of package Tktable provided"). A later try, or a rerun of the job, works. Only with
#: TKTABLE_REQUIRED=1, so a run without Tktable isn't slowed down.
TKTABLE_LOAD_TRIES = 3 if TKTABLE_REQUIRED else 1
TKTABLE_LOAD_RETRY_SECONDS = 2

#: What Tcl said, and what it saw, when Tktable couldn't be loaded; printed once at the end of the
#: test run (see pytest_terminal_summary), because the error alone often doesn't say why.
TKTABLE_LOAD_REPORT: list[str] = []


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

    errors: list[str] = []
    for tries in range(1, TKTABLE_LOAD_TRIES + 1):
        try:
            load_tktable(session_root)
            if errors:
                TKTABLE_LOAD_REPORT.extend([f"Tktable loaded at try {tries}, after:", *errors])
            return ""
        except tkinter.TclError as exc:
            errors.append(f"try {tries}: {exc}")
            # Tcl's stack trace: which command in pkgIndex.tcl failed, e.g. the load of the library.
            TKTABLE_LOAD_REPORT.append(
                f"Tcl errorInfo at try {tries}:\n{tcl(session_root, 'set ::errorInfo')}"
            )
            if tries < TKTABLE_LOAD_TRIES:
                time.sleep(TKTABLE_LOAD_RETRY_SECONDS)

    TKTABLE_LOAD_REPORT.extend(tktable_load_details(session_root))
    auto_path = session_root.tk.splitlist(session_root.tk.call("set", "auto_path"))
    folders = ", ".join(str(folder) for folder in auto_path)
    library = os.environ.get("TKTABLE_LIBRARY")
    details = (
        f"TKTABLE_LIBRARY={library}; auto_path: {folders}; see the Tktable load report at the end"
    )
    # The first error is the real one: later tries can fail just because the first one did.
    return f"{'; '.join(errors)} ({details})"


def tcl(tk: tkinter.Tk, script: str) -> str:
    """The result of a Tcl script, or its error, for the report: it must not raise."""
    try:
        return str(tk.tk.eval(script))
    except tkinter.TclError as exc:
        return f"error: {exc}"


def tktable_load_details(tk: tkinter.Tk) -> list[str]:
    """What Tcl knows about Tktable, and which files are in TKTABLE_LIBRARY."""
    ifneeded = "lmap v [package versions Tktable] {package ifneeded Tktable $v}"
    details = [
        f"Tcl {tcl(tk, 'info patchlevel')}",
        f"Tktable versions known to Tcl: {tcl(tk, 'package versions Tktable')}",
        f"package ifneeded scripts: {tcl(tk, ifneeded)}",
        # If Tktable's library is listed here, it was loaded, but its init didn't provide Tktable.
        f"Loaded libraries: {tcl(tk, 'info loaded')}",
    ]
    library = os.environ.get("TKTABLE_LIBRARY")
    if library:
        try:
            files = [
                f"{path} ({path.stat().st_size} bytes)"
                for path in sorted(Path(library).rglob("*"))
                if path.is_file()
            ]
            details.append("Files in TKTABLE_LIBRARY:\n" + "\n".join(files))
        except OSError as exc:
            details.append(f"Files in TKTABLE_LIBRARY: cannot be listed: {exc}")
    return details


def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter) -> None:
    """Print the Tktable load report once, if there is one, instead of in every failed test."""
    if TKTABLE_LOAD_REPORT:
        terminalreporter.section("Tktable load report")
        for line in TKTABLE_LOAD_REPORT:
            terminalreporter.line(line)


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
