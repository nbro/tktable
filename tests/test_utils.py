# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, too-few-public-methods
from __future__ import annotations

import tkinter

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
