"""Cell values computed on demand by a callback, instead of stored in an ArrayVar.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.callback_values

Pass ``-test`` to close the window after a second.
"""

import tkinter

from examples.window import create_window, run
from tktable import Table

DESCRIPTION = (
    "A 10x10 multiplication table where no value is stored anywhere: with usecommand=1, Tktable "
    "asks the command callback for each value it draws."
)
SIZE = 10


def cell_value(event: tkinter.Event) -> str:
    """Return the value of cell (event.r, event.c). Row 0 and column 0 are the titles."""
    if event.r == 0 and event.c == 0:
        return "×"
    if event.r == 0:
        return str(event.c)
    if event.c == 0:
        return str(event.r)
    return str(event.r * event.c)


def main() -> None:
    """Create a window with the multiplication table."""
    root, frame = create_window("Values from a callback", DESCRIPTION)

    table = Table(
        frame,
        rows=SIZE + 1,
        cols=SIZE + 1,
        titlerows=1,
        titlecols=1,
        colwidth=5,
        rowstretch="all",
        colstretch="all",
        state="disabled",
        usecommand=1,
        command=cell_value,
    )
    table.pack(expand=True, fill="both")
    table.tag_configure("title", background="#1e293b", foreground="#ffffff")

    run(root)


if __name__ == "__main__":
    main()
