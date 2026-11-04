# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, too-few-public-methods
from __future__ import annotations

import sys
import tkinter
import types
from pathlib import Path

import pytest

from tktable import utils


class FakeTk:
    """Records Tcl calls instead of running them."""

    def __init__(self, versions: tuple[str, ...] = ()) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.versions = versions

    def call(self, *args: str) -> object:
        self.calls.append(args)
        if args[:2] == ("package", "versions"):
            return self.versions
        if args[:2] == ("package", "require"):
            return "2.10"
        return ""

    def eval(self, script: str) -> str:
        self.calls.append((script,))
        return ""

    def splitlist(self, value: tuple[str, ...]) -> tuple[str, ...]:
        return value


class FakeInterp:
    def __init__(self, versions: tuple[str, ...] = ()) -> None:
        self.tk = FakeTk(versions)


@pytest.fixture(autouse=True)
def without_bundled_tktable(monkeypatch):
    """Run these tests as if pytktable-binaries were not installed, unless a test says otherwise."""
    monkeypatch.setattr(utils, "_bundled_library", lambda: None)


def test_extend_auto_path_with_env(monkeypatch):
    monkeypatch.setenv(utils.TKTABLE_LIBRARY_ENV_VAR, "/opt/Tktable2.10")
    interp = FakeInterp()
    utils.extend_auto_path(interp)  # type: ignore[arg-type]
    assert interp.tk.calls == [("lappend", "auto_path", "/opt/Tktable2.10")]


def test_extend_auto_path_without_env(monkeypatch):
    monkeypatch.delenv(utils.TKTABLE_LIBRARY_ENV_VAR, raising=False)
    interp = FakeInterp()
    utils.extend_auto_path(interp)  # type: ignore[arg-type]
    assert not interp.tk.calls


def test_extend_auto_path_with_bundled_tktable(monkeypatch):
    monkeypatch.delenv(utils.TKTABLE_LIBRARY_ENV_VAR, raising=False)
    monkeypatch.setattr(utils, "_bundled_library", lambda: "/site-packages/tktable_binaries")
    interp = FakeInterp()
    utils.extend_auto_path(interp)  # type: ignore[arg-type]
    assert interp.tk.calls == [("lappend", "auto_path", "/site-packages/tktable_binaries")]


def test_extend_auto_path_with_env_and_bundled_tktable(monkeypatch):
    monkeypatch.setenv(utils.TKTABLE_LIBRARY_ENV_VAR, "/opt/Tktable2.10")
    monkeypatch.setattr(utils, "_bundled_library", lambda: "/site-packages/tktable_binaries")
    interp = FakeInterp()
    utils.extend_auto_path(interp)  # type: ignore[arg-type]
    assert interp.tk.calls == [
        ("lappend", "auto_path", "/opt/Tktable2.10"),
        ("lappend", "auto_path", "/site-packages/tktable_binaries"),
    ]


def test_bundled_library_without_pytktable_binaries(monkeypatch):
    monkeypatch.undo()
    # None in sys.modules makes "import tktable_binaries" raise ImportError.
    monkeypatch.setitem(sys.modules, "tktable_binaries", None)
    assert utils._bundled_library() is None  # pylint: disable=protected-access


def test_bundled_library_with_pytktable_binaries(monkeypatch):
    monkeypatch.undo()
    fake = types.ModuleType("tktable_binaries")
    fake.library_dir = lambda: Path("/site-packages/tktable_binaries")  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "tktable_binaries", fake)
    expected = str(Path("/site-packages/tktable_binaries"))
    assert utils._bundled_library() == expected  # pylint: disable=protected-access


def test_find_tktable_scans_without_loading(monkeypatch):
    monkeypatch.delenv(utils.TKTABLE_LIBRARY_ENV_VAR, raising=False)
    interp = FakeInterp(versions=("2.10", "2.11"))
    assert utils.find_tktable(interp) == ["2.10", "2.11"]  # type: ignore[arg-type]
    assert not any(c[:2] == ("package", "require") for c in interp.tk.calls)


def test_find_tktable_not_found(monkeypatch):
    monkeypatch.delenv(utils.TKTABLE_LIBRARY_ENV_VAR, raising=False)
    assert utils.find_tktable(FakeInterp()) == []  # type: ignore[arg-type]


def test_load_tktable_requires_package(monkeypatch):
    monkeypatch.delenv(utils.TKTABLE_LIBRARY_ENV_VAR, raising=False)
    interp = FakeInterp()
    assert utils.load_tktable(interp) == "2.10"  # type: ignore[arg-type]
    assert interp.tk.calls == [("package", "require", "Tktable")]


def test_setup_master_returns_given_master():
    master = object()
    assert utils._setup_master(master) is master  # type: ignore[arg-type]  # pylint: disable=protected-access


def test_setup_master_without_default_root(monkeypatch):
    monkeypatch.setattr(tkinter, "_support_default_root", False)
    with pytest.raises(RuntimeError, match="No master specified"):
        utils._setup_master(None)  # pylint: disable=protected-access
