# pylint: disable=missing-function-docstring, protected-access

"""
A module that contains a class for using Tcl arrays,
which are, in some instances, required by tktable.
"""

import tkinter

from tktable.utils import _setup_master


class ArrayVar(tkinter.Variable):
    """Class for handling Tcl arrays.

    An array is actually an associative array in Tcl, so this class supports
    some dict operations.
    """

    # pylint: disable=super-init-not-called  # TODO: can this be solve more properly?
    def __init__(self, master=None, name=None):
        # Tkinter.Variable.__init__ is not called on purpose! I don't wanna
        # see an ugly _default value in the pretty array.
        self._master = _setup_master(master)
        self._tk = self._master.tk
        if name:
            self._name = name
        else:
            self._name = f"PY_VAR{id(self)}"

    def __del__(self):
        if bool(self._tk.call("info", "exists", self._name)):
            self._tk.globalunsetvar(self._name)

    def __len__(self):
        return int(self._tk.call("array", "size", str(self)))

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(**{str(key): value})

    def names(self):
        return self._tk.call("array", "names", self._name)

    def get(self, key=None):
        if key is None:
            flatten_pairs = self._tk.call("array", "get", str(self))
            return dict(list(zip(flatten_pairs[::2], flatten_pairs[1::2])))
        return self._tk.globalgetvar(str(self), str(key))

    # pylint: disable=arguments-differ  # TODO: maybe consider calling this method differently?
    def set(self, **kw):
        self._tk.call("array", "set", str(self), tkinter._flatten(list(kw.items())))

    def unset(self, pattern=None):
        """Unsets all of the elements in the array. If pattern is given, only
        the elements that match pattern are unset."""
        self._tk.call("array", "unset", str(self), pattern)
