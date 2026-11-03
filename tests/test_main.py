# pylint: disable=missing-module-docstring, missing-function-docstring
from tktable.__main__ import main


def test_check_reports_tktable(capsys):
    status = main()
    out = capsys.readouterr().out
    if "tkinter:   NOT AVAILABLE" in out:
        assert status == 1
        return
    assert "Tcl:" in out
    assert "Tktable:" in out
    assert status == (0 if "Tktable:   found" in out and "FAILED" not in out else 1)
