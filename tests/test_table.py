# pylint: disable=missing-module-docstring, missing-function-docstring, redefined-outer-name
from __future__ import annotations

import tkinter

import pytest

import tktable.table as table_module
from tktable import ArrayVar, Table
from tktable.table import CannotUseError


@pytest.fixture
def table(table_root: tkinter.Tk) -> Table:
    """A 4x3 table backed by an ArrayVar, with no title rows/cols."""
    var = ArrayVar(table_root)
    t = Table(table_root, rows=4, cols=3, variable=var, cache=1)
    t.var = var  # keep the variable alive as long as the table
    t.pack()
    table_root.update_idletasks()
    return t


def test_cannot_use_error_when_tktable_cannot_be_loaded(root, monkeypatch):
    """Simulates a missing Tktable, so the test gives the same result whether it is installed."""

    def fail_to_load(_master):
        raise tkinter.TclError("can't find package Tktable")

    monkeypatch.setattr(table_module, "load_tktable", fail_to_load)

    with pytest.raises(CannotUseError, match="python -m tktable"):
        Table(root)


@pytest.mark.tktable
def test_options_are_passed_to_the_widget(table):
    assert int(table.cget("rows")) == 4
    assert int(table.cget("cols")) == 3
    assert table.version


@pytest.mark.tktable
def test_set_and_get_cells(table):
    table.var["0,0"] = "from var"
    assert table.get("0,0") == "from var"
    table.set(**{"1,1": "kw"})
    assert table.get("1,1") == "kw"
    assert table.set(index="1,1") == "kw"


@pytest.mark.tktable
def test_set_row_and_get_range(table):
    table.set("a", "b", "c", rc="row", index="2,0")
    assert table.get("2,0", "2,2") == ("a", "b", "c")


@pytest.mark.tktable
def test_insert_and_delete_rows_and_cols(table):
    table.insert_rows(0, 2)
    assert int(table.cget("rows")) == 6
    table.delete_rows(0, 1)
    assert int(table.cget("rows")) == 5
    table.insert_cols(0, 1)
    assert int(table.cget("cols")) == 4
    table.delete_cols(0, 2)
    assert int(table.cget("cols")) == 2


@pytest.mark.tktable
def test_activate_and_index(table):
    table.activate("2,1")
    assert table.index("active") == "2,1"
    assert table.index("active", "row") == 2
    assert table.index("active", "col") == 1


@pytest.mark.tktable
def test_selection(table):
    table.selection_set("0,0", "1,1")
    assert table.selection_includes("1,0")
    assert set(table.curselection()) == {"0,0", "0,1", "1,0", "1,1"}
    table.selection_clear("all")
    assert not table.curselection()


@pytest.mark.tktable
def test_width_and_height(table):
    table.width(**{"0": 12})
    assert table.width(0) == 12
    table.height(**{"0": 3})
    assert table.height(0) == 3  # regression: row 0 returned all heights


@pytest.mark.tktable
def test_tags(table):
    table.tag_configure("mytag", background="yellow")
    assert table.tag_exists("mytag")
    assert "mytag" in table.tag_names()
    assert str(table.tag_cget("mytag", "background")) == "yellow"
    table.tag_cell("mytag", "1,1")
    assert table.tag_includes("mytag", "1,1")
    assert not table.tag_includes("mytag", "0,0")
    table.tag_configure("other", background="red")
    table.tag_raise("mytag")
    table.tag_lower("mytag")  # regression: used to omit the tag name
    table.tag_delete("mytag")
    assert not table.tag_exists("mytag")


@pytest.mark.tktable
def test_spans(table):
    table.spans(**{"0,0": "1,1"})
    assert table.spans("0,0") == "1,1"


@pytest.mark.tktable
def test_callable_options_are_registered(table_root):
    """Regression test: callables used to be detected with collections.Callable."""
    calls = []

    def command(event):
        calls.append((event.r, event.c, event.C))
        return event.C

    table = Table(table_root, rows=2, cols=2, usecommand=1, command=command)
    table.pack()
    table_root.update()
    assert table.get("1,1") == "1,1"
    assert (1, 1, "1,1") in calls
