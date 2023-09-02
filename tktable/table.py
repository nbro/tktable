# pylint: disable=missing-function-docstring, protected-access, inconsistent-return-statements


"""
A module that contains a Python wrapper class for the Tcl/tk tktable widget.
"""


import collections
import logging
import os
import tkinter

from tktable.utils import _setup_master

logger = logging.getLogger(__name__)

# TODO: consider solving the inconsistent-return-statements in more appropriate ways,
#  e.g. split a method into 2, etc.


class CannotUseError(RuntimeError):
    """
    The exception raised when you cannot use the Table because of missing dependencies.
    """


# pylint: disable=too-many-public-methods
class Table(tkinter.Widget):
    """Create and manipulate tables."""

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

    def __init__(self, master=None, **kw):
        master = _setup_master(master)

        env_var = os.environ.get("TKTABLE_LIBRARY")
        if env_var:
            logger.info("Add %s to auto_path", env_var)
            master.tk.eval(f"global auto_path; lappend auto_path {{{env_var}}}")
        else:
            logger.info("The environment variable TKTABLE_LIBRARY is not defined.")

        try:
            logger.info("Require the Tcl/Tk widget: tktable.")

            # https://wiki.tcl-lang.org/page/package+require
            master.tk.call("package", "require", "Tktable")

            tkinter.Widget.__init__(self, master, "table", kw)
        except tkinter.TclError as exc:
            raise CannotUseError(
                f"You cannot instantiate {self.__class__.__name__} "
                f"unless you have installed in your system the following tools:\n"
                "1. Tcl (a programming language: https://www.tcl-lang.org/)\n"
                "2. Tk (a Tcl package to create and manipulate GUI widgets)\n"
                "3. Tkinter (a Python interface to Tk: "
                "https://docs.python.org/3/library/tkinter.html), "
                "which is installed.\n"
                "4. The original Tk widget: tktable,\n"
                "which you may be able to install using the instructions here:\n"
                "https://github.com/nbro/tktable/issues/1#issuecomment-244519589."
            ) from exc

    def _options(self, cnf, kw=None):
        if kw:
            cnf = tkinter._cnfmerge((cnf, kw))
        else:
            cnf = tkinter._cnfmerge(cnf)
        res = ()
        for k, v in cnf.items():
            if isinstance(v, collections.Callable):
                if k in self._tabsubst_commands:
                    v = f"{self._register(v, self._tabsubst)} {' '.join(self._tabsubst_format)}"
                else:
                    v = self._register(v)
            res += (f"-{k}", v)
        return res

    def _tabsubst(self, *args):
        if len(args) != len(self._tabsubst_format):
            return args
        tk = self.tk
        c, C, i, r, s, S, W = args  # pylint: disable=unused-variable
        e = tkinter.Event()
        e.widget = self
        e.c = tk.getint(c)
        e.i = tk.getint(i)
        e.r = tk.getint(r)
        e.C = f"{e.r:d},{e.c:d}"
        e.s = s
        e.S = S
        try:
            e.W = self._nametowidget(W)
        except KeyError:
            e.W = None
        return (e,)

    def _handle_switches(self, args):
        args = args or ()
        return tuple(f"-{x}" for x in args if x in self._switches)

    def activate(self, index):
        """Set the active cell to the one indicated by index."""
        self.tk.call(self._w, "activate", index)

    def bbox(self, first, last=None):
        """Return the bounding box for the specified cell (range) as a
        4-tuple of x, y, width and height in pixels. It clips the box to
        the visible portion, if any, otherwise an empty tuple is returned."""
        return self._getints(self.tk.call(self._w, "bbox", first, last)) or ()

    def clear(self, option, first=None, last=None):
        """This is a convenience routine to clear certain state information
        managed by the table. first and last represent valid table indices.
        If neither are specified, then the command operates on the whole
        table."""
        self.tk.call(self._w, "clear", option, first, last)

    def clear_cache(self, first=None, last=None):
        """Clear the specified section of the cache, if the table has been
        keeping one."""
        self.clear("cache", first, last)

    def clear_sizes(self, first=None, last=None):
        """Clear the specified row and column areas of specific height/width
        dimensions. When just one index is specified, for example 2,0, that
        is interpreted as row 2 and column 0."""
        self.clear("sizes", first, last)

    def clear_tags(self, first=None, last=None):
        """Clear the specified area of tags (all row, column and cell tags)."""
        self.clear("tags", first, last)

    def clear_all(self, first=None, last=None):
        """Perform all of the above clear functions on the specified area."""
        self.clear("all", first, last)

    def curselection(self, value=None):
        """With no arguments, it returns the sorted indices of the currently
        selected cells. Otherwise it sets all the selected cells to the given
        value if there is an associated ArrayVar and the state is not
        disabled."""
        result = self.tk.call(self._w, "curselection", value)
        if value is None:
            return result

    def curvalue(self, value=None):
        """If no value is given, the value of the cell being edited (indexed
        by active) is returned, else it is set to the given value."""
        return self.tk.call(self._w, "curvalue", value)

    def delete_active(self, index1, index2=None):
        """Deletes text from the active cell. If only one index is given,
        it deletes the character after that index, otherwise it deletes from
        the first index to the second. index can be a number, insert or end."""
        self.tk.call(self._w, "delete", "active", index1, index2)

    def delete_cols(self, index, count=None, switches=None):
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._w, "delete", "cols", *args)

    def delete_rows(self, index, count=None, switches=None):
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._w, "delete", "rows", *args)

    def get(self, first, last=None):
        """Returns the value of the cells specified by the table indices
        first and (optionally) last."""
        return self.tk.call(self._w, "get", first, last)

    def height(self, row=None, **kwargs):
        """If row and kwargs are not given, a list describing all rows for
        which a width has been set is returned.
        If row is given, the height of that row is returned.
        If kwargs is given, then it sets the key/value pairs, where key is a
        row and value represents the height for the row."""
        if row is None and not kwargs:
            pairs = self.tk.splitlist(self.tk.call(self._w, "height"))
            return dict(pair.split() for pair in pairs)
        if row:
            return int(self.tk.call(self._w, "height", str(row)))
        args = tkinter._flatten(list(kwargs.items()))
        self.tk.call(self._w, "height", *args)

    def hidden(self, *args):
        """When called without args, it returns all the hidden cells (those
        cells covered by a spanning cell). If one index is specified, it
        returns the spanning cell covering that index, if any. If multiple
        indices are specified, it returns 1 if all indices are hidden cells,
        0 otherwise."""
        return self.tk.call(self._w, "hidden", *args)

    def icursor(self, arg=None):
        """If arg is not specified, return the location of the insertion
        cursor in the active cell. Otherwise, set the cursor to that point in
        the string.

        0 is before the first character, you can also use insert or end for
        the current insertion point or the end of the text. If there is no
        active cell, or the cell or table is disabled, this will return -1."""
        return self.tk.call(self._w, "icursor", arg)

    def index(self, index, rc=None):
        """Return the integer cell coordinate that corresponds to index in the
        form row, col. If rc is specified, it must be either 'row' or 'col' so
        only the row or column index is returned."""
        res = self.tk.call(self._w, "index", index, rc)
        if rc is None:
            return res
        return int(res)

    def insert_active(self, index, value):
        """The value is a text string which is inserted at the index position
        of the active cell. The cursor is then positioned after the new text.
        index can be a number, insert or end."""
        self.tk.call(self._w, "insert", "active", index, value)

    def insert_cols(self, index, count=None, switches=None):
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._w, "insert", "cols", *args)

    def insert_rows(self, index, count=None, switches=None):
        args = self._handle_switches(switches) + (index, count)
        self.tk.call(self._w, "insert", "rows", *args)

    # def postscript(self, **kwargs):
    #    """Skip this command if you are under Windows.
    #
    #    Accepted options:
    #        colormap, colormode, file, channel, first, fontmap, height,
    #        last, pageanchor, pageheight, pagewidth, pagex, pagey, rotate,
    #        width, x, y
    #    """
    #    args = ()
    #    for key, val in kwargs.iteritems():
    #        args += ('-%s' % key, val)
    #
    #    return self.tk.call(self._w, 'postscript', *args)

    def reread(self):
        """Rereads the old contents of the cell back into the editing buffer.
        Useful for a key binding when <Escape> is pressed to abort the edit
        (a default binding)."""
        self.tk.call(self._w, "reread")

    def scan_mark(self, x, y):
        self.tk.call(self._w, "scan", "mark", x, y)

    def scan_dragto(self, x, y):
        self.tk.call(self._w, "scan", "dragto", x, y)

    def see(self, index):
        self.tk.call(self._w, "see", index)

    def selection_anchor(self, index):
        self.tk.call(self._w, "selection", "anchor", index)

    # pylint: disable=arguments-differ  # TODO: maybe consider calling this method differently?
    def selection_clear(self, first, last=None):
        self.tk.call(self._w, "selection", "clear", first, last)

    def selection_includes(self, index):
        return self.getboolean(self.tk.call(self._w, "selection", "includes", index))

    def selection_set(self, first, last=None):
        self.tk.call(self._w, "selection", "set", first, last)

    def set(self, *args, rc=None, index=None, **kwargs):
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
            return self.tk.call(self._w, "set", *args)
        if rc is None:
            args = tkinter._flatten(list(kwargs.items()))
            self.tk.call(self._w, "set", *args)
        else:
            self.tk.call(self._w, "set", rc, index, args)

    def spans(self, index=None, **kwargs):
        """Manipulate row/col spans.

        When called with no arguments, all known spans are returned as a dict.
        When called with only the index, the span for that index only is
        returned, if any. Otherwise kwargs is assumed to contain keys/values
        pairs used to set spans. A span starts at the row,col defined by a key
        and continues for the specified number of rows,cols specified by
        its value. A span of 0,0 unsets any span on that cell."""
        if kwargs:
            args = tkinter._flatten(list(kwargs.items()))
            self.tk.call(self._w, "spans", *args)
        else:
            return self.tk.call(self._w, "spans", index)

    def tag_cell(self, tagname, *args):
        return self.tk.call(self._w, "tag", "cell", tagname, *args)

    def tag_cget(self, tagname, option):
        return self.tk.call(self._w, "tag", "cget", tagname, f"-{option}")

    def tag_col(self, tagname, *args):
        return self.tk.call(self._w, "tag", "col", tagname, *args)

    def tag_configure(self, tagname, option=None, **kwargs):
        """Query or modify options associated with the tag given by tagname.

        If no option is specified, a dict describing all of the available
        options for tagname is returned. If option is specified, then the
        command returns a list describing the one named option. Lastly, if
        kwargs is given then it corresponds to option-value pairs that should
        be modified."""
        if option is None and not kwargs:
            split1 = self.tk.splitlist(
                self.tk.call(self._w, "tag", "configure", tagname)
            )
            result = {}
            for item in split1:
                res = self.tk.splitlist(item)
                result[res[0]] = res[1:]
            return result
        if option:
            return self.tk.call(self._w, "tag", "configure", tagname, f"-{option}")
        args = ()
        for key, val in kwargs.items():
            args += (f"-{key}", val)
        self.tk.call(self._w, "tag", "configure", tagname, *args)

    def tag_delete(self, tagname):
        self.tk.call(self._w, "tag", "delete", tagname)

    def tag_exists(self, tagname):
        return self.getboolean(self.tk.call(self._w, "tag", "exists", tagname))

    def tag_includes(self, tagname, index):
        return self.getboolean(self.tk.call(self._w, "tag", "includes", tagname, index))

    def tag_lower(self, tagname, belowthis=None):  # pylint: disable=unused-argument
        self.tk.call(self._w, "tag", "lower", belowthis)

    def tag_names(self, pattern=None):
        return self.tk.call(self._w, "tag", "names", pattern)

    def tag_raise(self, tagname, abovethis=None):
        self.tk.call(self._w, "tag", "raise", tagname, abovethis)

    def tag_row(self, tagname, *args):
        return self.tk.call(self._w, "tag", "row", tagname, *args)

    def validate(self, index):
        """Explicitly validates the specified index based on the current
        callback set for the validatecommand option. Return 0 or 1 based on
        whether the cell was validated."""
        return self.tk.call(self._w, "validate", index)

    @property
    def version(self):
        """Return tktable's package version."""
        return self.tk.call(self._w, "version")

    def width(self, column=None, **kwargs):
        """If column and kwargs are not given, a dict describing all columns
        for which a width has been set is returned.
        If column is given, the width of that column is returned.
        If kwargs is given, then it sets the key/value pairs, where key is a
        column and value represents the width for the column."""
        if column is None and not kwargs:
            pairs = self.tk.splitlist(self.tk.call(self._w, "width"))
            return dict(pair.split() for pair in pairs)
        if column is not None:
            return int(self.tk.call(self._w, "width", str(column)))
        args = tkinter._flatten(list(kwargs.items()))
        self.tk.call(self._w, "width", *args)

    def window_cget(self, index, option):
        return self.tk.call(self._w, "window", "cget", index, option)

    def window_configure(self, index, option=None, **kwargs):
        """Query or modify options associated with the embedded window given
        by index. This should also be used to add a new embedded window into
        the table.

        If no option is specified, a dict describing all of the available
        options for index is returned. If option is specified, then the
        command returns a list describing the one named option. Lastly, if
        kwargs is given then it corresponds to option-value pairs that should
        be modified."""
        if option is None and not kwargs:
            return self.tk.call(self._w, "window", "configure", index)
        if option:
            return self.tk.call(self._w, "window", "configure", index, f"-{option}")
        args = ()
        for key, val in kwargs.items():
            args += (f"-{key}", val)
        self.tk.call(self._w, "window", "configure", index, *args)

    def window_delete(self, *indexes):
        self.tk.call(self._w, "window", "delete", *indexes)

    def window_move(self, index_from, index_to):
        self.tk.call(self._w, "window", "move", index_from, index_to)

    def window_names(self, pattern=None):
        return self.tk.call(self._w, "window", "names", pattern)

    def xview(self, index=None):
        """If index is not given a tuple containing two fractions is returned,
        each fraction is between 0 and 1. Together they describe the
        horizontal span that is visible in the window.

        If index is given the view in the window is adjusted so that the
        column given by index is displayed at the left edge of the window."""
        res = self.tk.call(self._w, "xview", index)
        if index is None:
            return self._getdoubles(res)

    def xview_moveto(self, fraction):
        """Adjusts the view in the window so that fraction of the total width
        of the table text is off-screen to the left. The fraction parameter
        must be a fraction between 0 and 1."""
        self.tk.call(self._w, "xview", "moveto", fraction)

    def xview_scroll(self, *L):
        # change by frank gao for attach scrollbar 11/11/2010
        """Shift the view in the window left or right according to number and
        what. The 'number' parameter must be an integer. The 'what' parameter
        must be either units or pages or an abbreviation of one of these.

        If 'what' is units, the view adjusts left or right by number cells on
        the display; if it is pages then the view adjusts by number screenfuls.
        If 'number' is negative then cells farther to the left become visible;
        if it is positive then cells farther to the right become visible."""
        # self.tk.call(self._w, 'xview', 'scroll', number, what)
        op, howMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.tk.call(self._w, "xview", "scroll", howMany, units)
        elif op == "moveto":
            self.tk.call(self._w, "xview", "moveto", howMany)

    def yview(self, index=None):
        """If index is not given a tuple containing two fractions is returned,
        each fraction is between 0 and 1. The first element gives the position
        of the table element at the top of the window, relative to the table
        as a whole. The second element gives the position of the table element
        just after the last one in the window, relative to the table as a
        whole.

        If index is given the view in the window is adjusted so that the
        row given by index is displayed at the top of the window."""
        res = self.tk.call(self._w, "yview", index)
        if index is None:
            return self._getdoubles(res)

    def yview_moveto(self, fraction):
        """Adjusts the view in the window so that the element given by
        fraction appears at the top of the window. The fraction parameter
        must be a fraction between 0 and 1."""
        self.tk.call(self._w, "yview", "moveto", fraction)

    def yview_scroll(self, *L):
        # change by frank gao for attach scrollbar 11/11/2010
        """Adjust the view in the window up or down according to number and
        what. The 'number' parameter must be an integer. The 'what' parameter
        must be either units or pages or an abbreviation of one of these.

        If 'what' is units, the view adjusts up or down by number cells; if it
        is pages then the view adjusts by number screenfuls.
        If 'number' is negative then earlier elements become visible; if it
        is positive then later elements become visible."""
        # self.tk.call(self._w, 'yview', 'scroll', number, what)
        op, howMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.tk.call(self._w, "yview", "scroll", howMany, units)
        elif op == "moveto":
            self.tk.call(self._w, "yview", "moveto", howMany)
