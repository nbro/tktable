"""Selection and the active cell: select cells, rows or columns, and react to the active cell.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.selection

Pass ``-test`` to close the window after a second.
"""

import sys
import tkinter
from tkinter import ttk

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    'With selectmode="extended", drag or Shift/Ctrl+click to select several cells. The buttons '
    "change selecttype, so a click selects a cell, a row or a column, or select a block in code. "
    "browsecommand updates the label below whenever the active cell changes."
)
ROWS, COLS = 6, 5


def main() -> None:
    """Create a window with a table, buttons to change what is selected, and a status label."""
    root, frame = create_window("Selection", DESCRIPTION)

    cells = ArrayVar(root)
    for row in range(ROWS):
        for col in range(COLS):
            cells[f"{row},{col}"] = f"{row},{col}"

    status = ttk.Label(frame, text="Click or drag over cells")
    status.pack(side="bottom", fill="x", pady=(8, 0))

    def show_state(_event: tkinter.Event | None = None) -> None:
        selected = ", ".join(map(str, table.tk.splitlist(table.curselection()))) or "nothing"
        try:
            active = table.index("active")
        except tkinter.TclError:  # No active cell yet.
            active = "none"
        status.configure(text=f"Active cell: {active}. Selected: {selected}")

    def select_block() -> None:
        table.selection_clear("all")
        table.selection_set("1,1", "3,3")
        show_state()

    buttons = ttk.Frame(frame)
    buttons.pack(side="bottom", pady=(12, 0))
    for select_type in ("cell", "row", "col"):
        ttk.Button(
            buttons,
            text=f"Click selects a {select_type}",
            command=lambda t=select_type: table.configure(selecttype=t),
        ).pack(side="left", padx=4)
    ttk.Button(buttons, text="Select 1,1 to 3,3", command=select_block).pack(side="left", padx=4)

    table = Table(
        frame,
        rows=ROWS,
        cols=COLS,
        colwidth=8,
        rowstretch="all",
        colstretch="all",
        selectmode="extended",
        selecttype="cell",
        variable=cells,
        browsecommand=show_state,
    )
    table.pack(expand=True, fill="both")
    table.tag_configure("sel", background="#c7d2fe")
    table.bind("<ButtonRelease-1>", show_state, add="+")

    if "-test" in sys.argv:
        root.after(500, select_block)

    run(root)


if __name__ == "__main__":
    main()
