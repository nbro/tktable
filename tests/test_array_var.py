# pylint: disable=missing-module-docstring, missing-function-docstring
from tktable import ArrayVar


def test_set_get_len(root):
    var = ArrayVar(root)
    var["0,0"] = "a"
    var.set(**{"0,1": "b"})
    assert len(var) == 2
    assert var["0,0"] == "a"
    assert var.get() == {"0,0": "a", "0,1": "b"}
    assert sorted(var.names()) == ["0,0", "0,1"]


def test_unset(root):
    var = ArrayVar(root)
    var.set(a="1", b="2")
    var.unset("a")
    assert var.get() == {"b": "2"}
    var.unset()
    assert len(var) == 0
