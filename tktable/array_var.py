"""ArrayVar, a tkinter variable for Tcl arrays, which a Table can store its cells in."""

import tkinter
from typing import Any

from tktable.utils import _setup_master


class ArrayVar(tkinter.Variable):
    """A Tcl array, the usual store for a Table's cells (its variable option).

    A Tcl array is an associative array, so this class supports some dict operations: cells are
    keyed by "row,col" indices, e.g. ``cells["0,1"] = "Hello"``.
    """

    # Tkinter.Variable.__init__ is not called on purpose, so the array has no default value.
    def __init__(  # pylint: disable=super-init-not-called
        self, master: tkinter.Misc | None = None, name: str | None = None
    ) -> None:
        self._master = _setup_master(master)
        self._tk = self._master.tk
        self._name = name or f"PY_VAR{id(self)}"

    def __del__(self) -> None:
        if bool(self._tk.call("info", "exists", self._name)):
            self._tk.globalunsetvar(self._name)

    def __len__(self) -> int:
        return int(self._tk.call("array", "size", str(self)))

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(**{str(key): value})

    def names(self) -> tuple[str, ...]:
        """Return the keys (indices) of the array."""
        return tuple(
            str(name) for name in self._tk.splitlist(self._tk.call("array", "names", self._name))
        )

    def get(self, key: str | None = None) -> Any:
        """Return the value at key, or all the array as a dict if key is None."""
        if key is None:
            # splitlist: tkinter may return the Tcl list as a Tcl_Obj, which can't be sliced.
            flatten_pairs = self._tk.splitlist(self._tk.call("array", "get", str(self)))
            return dict(zip(flatten_pairs[::2], flatten_pairs[1::2]))
        return self._tk.globalgetvar(str(self), str(key))

    # Unlike tkinter.Variable.set(value), this sets several keys at once.
    def set(self, **kw: Any) -> None:  # type: ignore[override]  # pylint: disable=arguments-differ
        """Set the values of the given keys, e.g. ``set(**{"0,0": "a", "0,1": "b"})``."""
        flattened = tuple(item for pair in kw.items() for item in pair)
        self._tk.call("array", "set", str(self), flattened)

    def unset(self, pattern: str | None = None) -> None:
        """Unsets all of the elements in the array. If pattern is given, only
        the elements that match pattern are unset."""
        if pattern is None:
            self._tk.call("array", "unset", str(self))
        else:
            self._tk.call("array", "unset", str(self), pattern)
