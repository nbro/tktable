"""Styling with tags: colors, fonts, alignment and relief, for cells, rows and columns.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.tags

Pass ``-test`` to close the window after a second.
"""

from tkinter import font

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    "A tag is a named style. Row 1 has a tag with a yellow background and bold text, column 3 one "
    "with blue, right-aligned text, and cell 4,1 one that is raised, red and centered. Where tags "
    "overlap, the one created first wins, and the built-in tags (like title) are created first: "
    "the title cell 0,2 only gets its own color because tag_raise() raises its tag above them."
)
ROWS, COLS = 6, 5


def main() -> None:
    """Create a window with a table styled by row, column and cell tags."""
    root, frame = create_window("Tags", DESCRIPTION)

    cells = ArrayVar(root)
    for row in range(ROWS):
        for col in range(COLS):
            cells[f"{row},{col}"] = f"{row},{col}"

    table = Table(
        frame,
        rows=ROWS,
        cols=COLS,
        titlerows=1,
        colwidth=10,
        rowstretch="all",
        colstretch="all",
        variable=cells,
    )
    table.pack(expand=True, fill="both")

    bold = font.nametofont("TkDefaultFont").copy()
    bold.configure(weight="bold")

    table.tag_configure("highlighted_row", background="#fef3c7", font=bold)
    table.tag_row("highlighted_row", 1)

    table.tag_configure("right_column", anchor="e", foreground="#1d4ed8")
    table.tag_col("right_column", 3)

    table.tag_configure("special_cell", background="#fecaca", relief="raised", anchor="center")
    table.tag_cell("special_cell", "4,1")

    # Title cells have the built-in "title" tag, which has a higher priority than our tags: raise
    # ours above it, or its color won't show.
    table.tag_configure("title", background="#1e293b", foreground="#ffffff")
    table.tag_configure("important_title", background="#4f46e5")
    table.tag_cell("important_title", "0,2")
    table.tag_raise("important_title")

    run(root)


if __name__ == "__main__":
    main()
