"""A spreadsheet-like table widget for tkinter, wrapping the Tcl/Tk Tktable extension.

Why the public classes are imported lazily
------------------------------------------
``python -m tktable`` (the diagnostic in ``__main__.py``) always imports this file first.
``ArrayVar`` and ``Table`` import ``tkinter`` at module level, so importing them here
eagerly would make the diagnostic crash with ``ModuleNotFoundError`` exactly when it is
most needed: when tkinter is not installed.

Instead, the module-level ``__getattr__`` below (PEP 562) imports them on first access, so
``from tktable import Table`` works as usual, while ``python -m tktable`` never imports
tkinter until it checks for it. The ``TYPE_CHECKING`` block is never executed, but lets
type checkers, linters and IDEs see ``tktable.Table`` and ``tktable.ArrayVar``.
"""

from typing import TYPE_CHECKING, Any

__all__ = ["ArrayVar", "Table"]

if TYPE_CHECKING:
    from tktable.array_var import ArrayVar
    from tktable.table import Table


def __getattr__(name: str) -> Any:
    # Called only for attributes not yet defined in this module (see the module docstring).
    # pylint: disable=import-outside-toplevel
    if name == "ArrayVar":
        from tktable.array_var import ArrayVar

        return ArrayVar
    if name == "Table":
        from tktable.table import Table

        return Table
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
