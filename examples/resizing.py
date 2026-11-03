"""Resizable rows and columns: drag a border between cells with the mouse.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.resizing

Pass ``-test`` to close the window after a second.
"""

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    'With resizeborders="both", drag the border between two rows or two columns to resize them. '
    "Sizes can also be set in code: column 0 is made wider with width(), and row 0 taller with "
    "height()."
)
ROWS, COLS = 5, 4


def main() -> None:
    """Create a window with a table whose rows and columns can be resized."""
    root, frame = create_window("Resizing", DESCRIPTION)

    cells = ArrayVar(root)
    for row in range(ROWS):
        for col in range(COLS):
            cells[f"{row},{col}"] = "Drag my borders"

    table = Table(frame, rows=ROWS, cols=COLS, resizeborders="both", variable=cells)
    table.pack(expand=True, fill="both")

    table.width(**{"0": 24})
    table.height(**{"0": 3})

    run(root)


if __name__ == "__main__":
    main()
