"""The Table widget, a Python wrapper of the Tcl/Tk Tktable widget."""

import logging
import tkinter
from collections.abc import Callable
from typing import Any, TypeAlias

from tktable.utils import _setup_master, load_tktable

logger = logging.getLogger(__name__)

#: A table index: "row,col" (e.g. "2,3"), or a special one such as "active", "anchor", "end",
#: "origin", "topleft", "bottomright" or "@x,y" (the cell at pixel x,y).
TableIndex: TypeAlias = str

#: A row or column number.
RowCol: TypeAlias = int | str


def _merge(*configs: Any) -> dict[str, Any]:
    """Merge option dicts (or tuples/lists of them), like tkinter's private _cnfmerge."""
    merged: dict[str, Any] = {}
    for config in configs:
        if isinstance(config, (tuple, list)):
            merged.update(_merge(*config))
        elif config:
            merged.update(config)
    return merged


def _flatten(options: dict[str, Any]) -> tuple[Any, ...]:
    """Turn {"a": 1, "b": 2} into ("a", 1, "b", 2), as Tcl commands expect."""
    return tuple(item for pair in options.items() for item in pair)


class CannotUseError(RuntimeError):
    """The exception raised when you cannot use the Table because of missing dependencies."""


# A plain data holder: one attribute per Tktable %-substitution, plus tkinter's widget.
# pylint: disable-next=too-few-public-methods,too-many-instance-attributes
class TableEvent(tkinter.Event):
    """The event given to the callbacks of a Table (browsecommand, command, validatecommand, ...).

    Its attributes are Tktable's %-substitutions.
    """

    #: The row of the cell.
    r: int
    #: The column of the cell.
    c: int
    #: The index of the cell, "r,c".
    C: str
    #: 1 if the cell is being written to, 0 if it is being read.
    i: int
    #: The current value of the cell.
    s: str
    #: The new value of the cell (e.g. what validatecommand should accept or reject).
    S: str
    #: The widget, if known.
    W: tkinter.Misc | None


# pylint: disable=too-many-public-methods
class Table(tkinter.Widget):
    """A table (spreadsheet-like) widget.

    The keyword arguments are the options of the Tktable widget, without the leading "-", e.g.
    ``Table(root, rows=10, cols=5, variable=array_var)``.

    :raise CannotUseError: if Tktable cannot be loaded.
    """

    @property
    def _path(self) -> str:
        """The widget's Tk path name, used in Tcl commands (what tkinter calls _w)."""
        return str(self)

    _switches = (
        "holddimensions",
        "holdselection",
        "holdtags",
        "holdwindows",
        "keeptitles",
        "-",
    )
    _tabsubst_format = ("%c", "%C", "%i", "%r", "%s", "%S", "%W")
    _tabsubst_commands = (
        "browsecommand",
        "browsecmd",
        "command",
        "selectioncommand",
        "selcmd",
        "validatecommand",
        "valcmd",
    )

    def __init__(self, master: tkinter.Misc | None = None, **kw: Any) -> None:
        master = _setup_master(master)

        try:
            load_tktable(master)
            tkinter.Widget.__init__(self, master, "table", kw)
        except tkinter.TclError as exc:
            raise CannotUseError(
                f"You cannot instantiate {self.__class__.__name__} because the Tcl/Tk "
                "extension Tktable could not be loaded by your Tcl/Tk installation.\n"
                "Run `python -m tktable` to diagnose the problem, and see "
                "https://nbro.github.io/tktable/installation/ for how to install Tktable "
                "or point the TKTABLE_LIBRARY environment variable to it."
            ) from exc

    def _options(self, cnf: Any, kw: Any = None) -> tuple[Any, ...]:
        res: tuple[Any, ...] = ()
        for k, v in _merge(cnf, kw).items():
            if callable(v):
                if k in self._tabsubst_commands:
                    v = f"{self.register(v, self._tabsubst)} {' '.join(self._tabsubst_format)}"
                else:
                    v = self.register(v)
            res += (f"-{k}", v)
        return res

    def _tabsubst(self, *args: str) -> tuple[Any, ...]:
        if len(args) != len(self._tabsubst_format):
            return args
        tk = self.tk
        c, C, i, r, s, S, W = args  # pylint: disable=unused-variable
        e = TableEvent()
        # widget is a standard tkinter.Event attribute, which tkinter also sets this way.
        e.widget = self  # pylint: disable=attribute-defined-outside-init
        e.c = tk.getint(c)
        e.i = tk.getint(i)
        e.r = tk.getint(r)
        e.C = f"{e.r:d},{e.c:d}"
        e.s = s
        e.S = S
        try:
            e.W = self.nametowidget(W)
        except KeyError:
            e.W = None
        return (e,)

    def _handle_switches(self, args: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
        args = args or ()
        return tuple(f"-{x}" for x in args if x in self._switches)

    def activate(self, index: TableIndex) -> None:
        """Set the active cell to the one indicated by index."""
        self.tk.call(self._path, "activate", index)

    def bbox(  # type: ignore[override]  # tkinter's Misc.bbox is grid_bbox, unrelated
        self, first: TableIndex, last: TableIndex | None = None
    ) -> tuple[int, ...]:
        """Return the bounding box for the specified cell (range) as a
        4-tuple of x, y, width and height in pixels. It clips the box to
        the visible portion, if any, otherwise an empty tuple is returned."""
        return tuple(
            int(x) for x in self.tk.splitlist(self.tk.call(self._path, "bbox", first, last))
        )

    def clear(
        self, option: str, first: TableIndex | None = None, last: TableIndex | None = None
    ) -> None:
        """This is a convenience routine to clear certain state information
        managed by the table. first and last represent valid table indices.
        If neither are specified, then the command operates on the whole
        table."""
        self.tk.call(self._path, "clear", option, first, last)

    def clear_cache(self, first: TableIndex | None = None, last: TableIndex | None = None) -> None:
        """Clear the specified section of the cache, if the table has been
        keeping one."""
        self.clear("cache", first, last)

    def clear_sizes(self, first: TableIndex | None = None, last: TableIndex | None = None) -> None:
        """Clear the specified row and column areas of specific height/width
        dimensions. When just one index is specified, for example 2,0, that
        is interpreted as row 2 and column 0."""
        self.clear("sizes", first, last)

    def clear_tags(self, first: TableIndex | None = None, last: TableIndex | None = None) -> None:
        """Clear the specified area of tags (all row, column and cell tags)."""
        self.clear("tags", first, last)

    def clear_all(self, first: TableIndex | None = None, last: TableIndex | None = None) -> None:
        """Perform all of the above clear functions on the specified area."""
        self.clear("all", first, last)

    def curselection(self, value: str | None = None) -> Any:
        """With no arguments, it returns the sorted indices of the currently
        selected cells. Otherwise it sets all the selected cells to the given
        value if there is an associated ArrayVar and the state is not
        disabled."""
        result = self.tk.call(self._path, "curselection", value)
        if value is None:
            return result
        return None

    def curvalue(self, value: str | None = None) -> Any:
        """If no value is given, the value of the cell being edited (indexed
        by active) is returned, else it is set to the given value."""
        return self.tk.call(self._path, "curvalue", value)

    def delete_active(self, index1: int | str, index2: int | str | None = None) -> None:
        """Deletes text from the active cell. If only one index is given,
        it deletes the character after that index, otherwise it deletes from
        the first index to the second. index can be a number, insert or end."""
        self.tk.call(self._path, "delete", "active", index1, index2)

    def delete_cols(
        self, index: RowCol, count: int | None = None, switches: tuple[str, ...] | None = None
    ) -> None:
        """Delete count columns (1 by default) starting at column index."""
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._path, "delete", "cols", *args)

    def delete_rows(
        self, index: RowCol, count: int | None = None, switches: tuple[str, ...] | None = None
    ) -> None:
        """Delete count rows (1 by default) starting at row index."""
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._path, "delete", "rows", *args)

    def get(self, first: TableIndex, last: TableIndex | None = None) -> Any:
        """Returns the value of the cells specified by the table indices
        first and (optionally) last."""
        return self.tk.call(self._path, "get", first, last)

    def height(self, row: RowCol | None = None, **kwargs: int) -> dict[str, str] | int | None:
        """If row and kwargs are not given, a dict describing all rows for
        which a height has been set is returned.
        If row is given, the height of that row is returned.
        If kwargs is given, then it sets the key/value pairs, where key is a
        row and value represents the height for the row."""
        if row is None and not kwargs:
            pairs = self.tk.splitlist(self.tk.call(self._path, "height"))
            return dict(pair.split() for pair in pairs)
        if row is not None:
            return int(self.tk.call(self._path, "height", str(row)))
        args = _flatten(kwargs)
        self.tk.call(self._path, "height", *args)
        return None

    def hidden(self, *args: TableIndex) -> Any:
        """When called without args, it returns all the hidden cells (those
        cells covered by a spanning cell). If one index is specified, it
        returns the spanning cell covering that index, if any. If multiple
        indices are specified, it returns 1 if all indices are hidden cells,
        0 otherwise."""
        return self.tk.call(self._path, "hidden", *args)

    def icursor(self, arg: int | str | None = None) -> Any:
        """If arg is not specified, return the location of the insertion
        cursor in the active cell. Otherwise, set the cursor to that point in
        the string.

        0 is before the first character, you can also use insert or end for
        the current insertion point or the end of the text. If there is no
        active cell, or the cell or table is disabled, this will return -1."""
        return self.tk.call(self._path, "icursor", arg)

    def index(self, index: TableIndex, rc: str | None = None) -> Any:
        """Return the integer cell coordinate that corresponds to index in the
        form row, col. If rc is specified, it must be either 'row' or 'col' so
        only the row or column index is returned."""
        res = self.tk.call(self._path, "index", index, rc)
        if rc is None:
            return res
        return int(res)

    def insert_active(self, index: int | str, value: str) -> None:
        """The value is a text string which is inserted at the index position
        of the active cell. The cursor is then positioned after the new text.
        index can be a number, insert or end."""
        self.tk.call(self._path, "insert", "active", index, value)

    def insert_cols(
        self, index: RowCol, count: int | None = None, switches: tuple[str, ...] | None = None
    ) -> None:
        """Insert count columns (1 by default) after column index."""
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._path, "insert", "cols", *args)

    def insert_rows(
        self, index: RowCol, count: int | None = None, switches: tuple[str, ...] | None = None
    ) -> None:
        """Insert count rows (1 by default) after row index."""
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._path, "insert", "rows", *args)

    def reread(self) -> None:
        """Rereads the old contents of the cell back into the editing buffer.
        Useful for a key binding when <Escape> is pressed to abort the edit
        (a default binding)."""
        self.tk.call(self._path, "reread")

    def scan_mark(self, x: int, y: int) -> None:
        """Record x and y and the current view, for a later scan_dragto()."""
        self.tk.call(self._path, "scan", "mark", x, y)

    def scan_dragto(self, x: int, y: int) -> None:
        """Scroll the view by 10 times the distance between x,y and the last scan_mark()."""
        self.tk.call(self._path, "scan", "dragto", x, y)

    def see(self, index: TableIndex) -> None:
        """Scroll the view so that the cell index is visible."""
        self.tk.call(self._path, "see", index)

    def selection_anchor(self, index: TableIndex) -> None:
        """Set the selection anchor to the cell index."""
        self.tk.call(self._path, "selection", "anchor", index)

    # pylint: disable-next=arguments-differ
    def selection_clear(  # type: ignore[override]
        self, first: TableIndex, last: TableIndex | None = None
    ) -> None:
        """Deselect the cells from first to last; first can be "all"."""
        self.tk.call(self._path, "selection", "clear", first, last)

    def selection_includes(self, index: TableIndex) -> bool:
        """Return whether the cell index is selected."""
        return self.getboolean(self.tk.call(self._path, "selection", "includes", index))

    def selection_set(self, first: TableIndex, last: TableIndex | None = None) -> None:
        """Select the cells from first to last."""
        self.tk.call(self._path, "selection", "set", first, last)

    def set(
        self, *args: Any, rc: str | None = None, index: TableIndex | None = None, **kwargs: Any
    ) -> Any:
        """If rc is specified (either 'row' or 'col') then it is assumes that
        args (if given) represents values which will be set into the
        subsequent columns (if row is specified) or rows (for col).
        If index is not None and args is not given, then it will return the
        value(s) for the cell(s) specified.

        If kwargs is given, assumes that each key in kwargs is a index in this
        table and sets the specified index to the associated value. Table
        validation will not be triggered via this method.

        Note that the table must have an associated array (defined through the
        variable option) in order to this work."""
        if not args and index is not None:
            if rc:
                args = (rc, index)
            else:
                args = (index,)
            return self.tk.call(self._path, "set", *args)
        if rc is None:
            args = _flatten(kwargs)
            self.tk.call(self._path, "set", *args)
        else:
            self.tk.call(self._path, "set", rc, index, args)
        return None

    def spans(self, index: TableIndex | None = None, **kwargs: str) -> Any:
        """Manipulate row/col spans.

        When called with no arguments, all known spans are returned as a dict.
        When called with only the index, the span for that index only is
        returned, if any. Otherwise kwargs is assumed to contain keys/values
        pairs used to set spans. A span starts at the row,col defined by a key
        and continues for the specified number of rows,cols specified by
        its value. A span of 0,0 unsets any span on that cell."""
        if kwargs:
            args = _flatten(kwargs)
            self.tk.call(self._path, "spans", *args)
            return None
        return self.tk.call(self._path, "spans", index)

    def tag_cell(self, tagname: str, *args: TableIndex) -> Any:
        """Apply the tag to the given cells, or return the cells with the tag."""
        return self.tk.call(self._path, "tag", "cell", tagname, *args)

    def tag_cget(self, tagname: str, option: str) -> Any:
        """Return the value of the tag's option (without the leading "-")."""
        return self.tk.call(self._path, "tag", "cget", tagname, f"-{option}")

    def tag_col(self, tagname: str, *args: RowCol) -> Any:
        """Apply the tag to the given columns, or return the columns with the tag."""
        return self.tk.call(self._path, "tag", "col", tagname, *args)

    def tag_configure(self, tagname: str, option: str | None = None, **kwargs: Any) -> Any:
        """Query or modify options associated with the tag given by tagname.

        If no option is specified, a dict describing all of the available
        options for tagname is returned. If option is specified, then the
        command returns a list describing the one named option. Lastly, if
        kwargs is given then it corresponds to option-value pairs that should
        be modified."""
        if option is None and not kwargs:
            split1 = self.tk.splitlist(self.tk.call(self._path, "tag", "configure", tagname))
            result = {}
            for item in split1:
                res = self.tk.splitlist(item)
                result[res[0]] = res[1:]
            return result
        if option:
            return self.tk.call(self._path, "tag", "configure", tagname, f"-{option}")
        args: tuple[Any, ...] = ()
        for key, val in kwargs.items():
            args += (f"-{key}", val)
        self.tk.call(self._path, "tag", "configure", tagname, *args)
        return None

    def tag_delete(self, tagname: str) -> None:
        """Delete the tag."""
        self.tk.call(self._path, "tag", "delete", tagname)

    def tag_exists(self, tagname: str) -> bool:
        """Return whether the tag exists."""
        return self.getboolean(self.tk.call(self._path, "tag", "exists", tagname))

    def tag_includes(self, tagname: str, index: TableIndex) -> bool:
        """Return whether the cell index has the tag."""
        return self.getboolean(self.tk.call(self._path, "tag", "includes", tagname, index))

    def tag_lower(self, tagname: str, belowthis: str | None = None) -> None:
        """Lower the tag's priority below the tag belowthis, or to the lowest."""
        self.tk.call(self._path, "tag", "lower", tagname, belowthis)

    def tag_names(self, pattern: str | None = None) -> Any:
        """Return the names of the tags, optionally only those matching pattern."""
        return self.tk.call(self._path, "tag", "names", pattern)

    def tag_raise(self, tagname: str, abovethis: str | None = None) -> None:
        """Raise the tag's priority above the tag abovethis, or to the highest."""
        self.tk.call(self._path, "tag", "raise", tagname, abovethis)

    def tag_row(self, tagname: str, *args: RowCol) -> Any:
        """Apply the tag to the given rows, or return the rows with the tag."""
        return self.tk.call(self._path, "tag", "row", tagname, *args)

    def validate(self, index: TableIndex) -> Any:
        """Explicitly validates the specified index based on the current
        callback set for the validatecommand option. Return 0 or 1 based on
        whether the cell was validated."""
        return self.tk.call(self._path, "validate", index)

    @property
    def version(self) -> Any:
        """Return tktable's package version."""
        return self.tk.call(self._path, "version")

    def width(self, column: RowCol | None = None, **kwargs: int) -> dict[str, str] | int | None:
        """If column and kwargs are not given, a dict describing all columns
        for which a width has been set is returned.
        If column is given, the width of that column is returned.
        If kwargs is given, then it sets the key/value pairs, where key is a
        column and value represents the width for the column."""
        if column is None and not kwargs:
            pairs = self.tk.splitlist(self.tk.call(self._path, "width"))
            return dict(pair.split() for pair in pairs)
        if column is not None:
            return int(self.tk.call(self._path, "width", str(column)))
        args = _flatten(kwargs)
        self.tk.call(self._path, "width", *args)
        return None

    def window_cget(self, index: TableIndex, option: str) -> Any:
        """Return the value of the option of the embedded window at index."""
        return self.tk.call(self._path, "window", "cget", index, option)

    def window_configure(self, index: TableIndex, option: str | None = None, **kwargs: Any) -> Any:
        """Query or modify options associated with the embedded window given
        by index. This should also be used to add a new embedded window into
        the table.

        If no option is specified, a dict describing all of the available
        options for index is returned. If option is specified, then the
        command returns a list describing the one named option. Lastly, if
        kwargs is given then it corresponds to option-value pairs that should
        be modified."""
        if option is None and not kwargs:
            return self.tk.call(self._path, "window", "configure", index)
        if option:
            return self.tk.call(self._path, "window", "configure", index, f"-{option}")
        args: tuple[Any, ...] = ()
        for key, val in kwargs.items():
            args += (f"-{key}", val)
        self.tk.call(self._path, "window", "configure", index, *args)
        return None

    def window_delete(self, *indexes: TableIndex) -> None:
        """Remove the embedded windows at the given indexes."""
        self.tk.call(self._path, "window", "delete", *indexes)

    def window_move(self, index_from: TableIndex, index_to: TableIndex) -> None:
        """Move the embedded window at index_from to index_to."""
        self.tk.call(self._path, "window", "move", index_from, index_to)

    def window_names(self, pattern: str | None = None) -> Any:
        """Return the indexes of the embedded windows, optionally only those matching pattern."""
        return self.tk.call(self._path, "window", "names", pattern)

    def xview(self, index: RowCol | None = None) -> tuple[float, ...] | None:
        """If index is not given a tuple containing two fractions is returned,
        each fraction is between 0 and 1. Together they describe the
        horizontal span that is visible in the window.

        If index is given the view in the window is adjusted so that the
        column given by index is displayed at the left edge of the window."""
        res = self.tk.call(self._path, "xview", index)
        if index is None:
            return tuple(float(x) for x in self.tk.splitlist(res))
        return None

    def xview_moveto(self, fraction: float) -> None:
        """Adjusts the view in the window so that fraction of the total width
        of the table text is off-screen to the left. The fraction parameter
        must be a fraction between 0 and 1."""
        self.tk.call(self._path, "xview", "moveto", fraction)

    def xview_scroll(self, *L: Any) -> None:
        # change by frank gao for attach scrollbar 11/11/2010
        """Shift the view in the window left or right according to number and
        what. The 'number' parameter must be an integer. The 'what' parameter
        must be either units or pages or an abbreviation of one of these.

        If 'what' is units, the view adjusts left or right by number cells on
        the display; if it is pages then the view adjusts by number screenfuls.
        If 'number' is negative then cells farther to the left become visible;
        if it is positive then cells farther to the right become visible."""
        op, howMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.tk.call(self._path, "xview", "scroll", howMany, units)
        elif op == "moveto":
            self.tk.call(self._path, "xview", "moveto", howMany)

    def yview(self, index: RowCol | None = None) -> tuple[float, ...] | None:
        """If index is not given a tuple containing two fractions is returned,
        each fraction is between 0 and 1. The first element gives the position
        of the table element at the top of the window, relative to the table
        as a whole. The second element gives the position of the table element
        just after the last one in the window, relative to the table as a
        whole.

        If index is given the view in the window is adjusted so that the
        row given by index is displayed at the top of the window."""
        res = self.tk.call(self._path, "yview", index)
        if index is None:
            return tuple(float(x) for x in self.tk.splitlist(res))
        return None

    def yview_moveto(self, fraction: float) -> None:
        """Adjusts the view in the window so that the element given by
        fraction appears at the top of the window. The fraction parameter
        must be a fraction between 0 and 1."""
        self.tk.call(self._path, "yview", "moveto", fraction)

    def yview_scroll(self, *L: Any) -> None:
        # change by frank gao for attach scrollbar 11/11/2010
        """Adjust the view in the window up or down according to number and
        what. The 'number' parameter must be an integer. The 'what' parameter
        must be either units or pages or an abbreviation of one of these.

        If 'what' is units, the view adjusts up or down by number cells; if it
        is pages then the view adjusts by number screenfuls.
        If 'number' is negative then earlier elements become visible; if it
        is positive then later elements become visible."""
        op, howMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.tk.call(self._path, "yview", "scroll", howMany, units)
        elif op == "moveto":
            self.tk.call(self._path, "yview", "moveto", howMany)


#: The type of a Table callback, e.g. for browsecommand or validatecommand.
TableCallback: TypeAlias = Callable[[TableEvent], Any]
