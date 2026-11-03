"""Validating edits: reject what the user types, as they type it.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.validation

Pass ``-test`` to close the window after a second.
"""

import tkinter
from tkinter import ttk

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    "With validate=1, Tktable calls validatecommand before each change to a cell, with the new "
    "value in event.S; returning False rejects it. Try typing letters in the Quantity column."
)
ITEMS = (("Apples", "12"), ("Pears", "7"), ("Plums", "30"))
QUANTITY_COLUMN = 1


def main() -> None:
    """Create a window with a table whose second column only accepts digits."""
    root, frame = create_window("Validation", DESCRIPTION)

    cells = ArrayVar(root)
    cells["0,0"], cells["0,1"] = "Item", "Quantity (digits only)"
    for row, (item, quantity) in enumerate(ITEMS, start=1):
        cells[f"{row},0"], cells[f"{row},1"] = item, quantity

    status = ttk.Label(frame, text="Edit a quantity: letters are rejected")
    status.pack(side="bottom", fill="x", pady=(12, 0))

    def validate(event: tkinter.Event) -> bool:
        if event.c != QUANTITY_COLUMN or event.S.isdigit() or event.S == "":
            return True
        status.configure(text=f"Rejected {event.S!r}: quantities are digits only")
        return False

    table = Table(
        frame,
        rows=len(ITEMS) + 1,
        cols=2,
        titlerows=1,
        colwidth=22,
        rowstretch="all",
        colstretch="all",
        variable=cells,
        validate=1,
        validatecommand=validate,
    )
    table.pack(expand=True, fill="both")

    run(root)


if __name__ == "__main__":
    main()
