"""Merged cells (spans): one cell covering several rows and/or columns.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.spans

Pass ``-test`` to close the window after a second.
"""

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    'A span is set on its top-left cell as "rows,cols": how many extra rows and columns it '
    'covers. Cell 0,0 spans "0,2" (3 columns of one row), and cell 2,2 spans "1,1" (a 2x2 block).'
)
ROWS, COLS = 6, 6


def main() -> None:
    """Create a window with a header spanning 3 columns and a 2x2 merged block."""
    root, frame = create_window("Spans", DESCRIPTION)

    cells = ArrayVar(root)
    for row in range(ROWS):
        for col in range(COLS):
            cells[f"{row},{col}"] = f"{row},{col}"
    cells["0,0"] = "Spans 3 columns"
    cells["2,2"] = "Spans 2 rows and 2 columns"

    table = Table(
        frame, rows=ROWS, cols=COLS, colwidth=12, rowstretch="all", colstretch="all", variable=cells
    )
    table.pack(expand=True, fill="both")

    table.spans(**{"0,0": "0,2", "2,2": "1,1"})

    table.tag_configure("merged", background="#e0e7ff", anchor="center")
    table.tag_cell("merged", "0,0", "2,2")

    run(root)


if __name__ == "__main__":
    main()
