"""Inserting and deleting rows and columns.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.insert_delete

Pass ``-test`` to close the window after a second.
"""

import sys
from tkinter import ttk

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    "Click a cell, then use the buttons to insert or delete a row or column next to it. "
    "insert_rows(index, count) inserts after index, and the cells' values move with their rows."
)
ROWS, COLS = 5, 4


def main() -> None:
    """Create a window with a table and buttons to insert and delete rows and columns."""
    root, frame = create_window("Insert and delete", DESCRIPTION)

    cells = ArrayVar(root)
    for row in range(ROWS):
        for col in range(COLS):
            cells[f"{row},{col}"] = f"{row},{col}"

    buttons = ttk.Frame(frame)
    buttons.pack(side="bottom", pady=(12, 0))

    table = Table(
        frame, rows=ROWS, cols=COLS, colwidth=8, rowstretch="all", colstretch="all", variable=cells
    )
    table.pack(expand=True, fill="both")
    table.activate("0,0")

    def active(kind: str) -> int:
        return table.index("active", kind)

    actions = {
        "Insert row": lambda: table.insert_rows(active("row"), 1),
        "Delete row": lambda: table.delete_rows(active("row"), 1),
        "Insert column": lambda: table.insert_cols(active("col"), 1),
        "Delete column": lambda: table.delete_cols(active("col"), 1),
    }
    for text, action in actions.items():
        ttk.Button(buttons, text=text, command=action).pack(side="left", padx=4)

    if "-test" in sys.argv:
        root.after(300, actions["Insert row"])
        root.after(600, actions["Delete column"])

    run(root)


if __name__ == "__main__":
    main()
