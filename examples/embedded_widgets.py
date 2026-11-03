"""Embedded widgets: any tkinter widget (button, checkbox, ...) inside a cell.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.embedded_widgets

Pass ``-test`` to close the window after a second.
"""

import tkinter
from tkinter import ttk

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    "A task list with a checkbox and a button in each row: window_configure(index, window=widget) "
    "puts a widget in a cell, and sticky makes it fill the cell. Edit a task's text, tick it, then "
    "click Show: the button reads the cell's current value."
)
TASKS = ("Write the docs", "Add tests", "Release 0.2.0")


def main() -> None:
    """Create a window with a task list: a checkbox and a button in each row."""
    root, frame = create_window("Embedded widgets", DESCRIPTION)

    cells = ArrayVar(root)
    cells["0,0"], cells["0,1"], cells["0,2"] = "Task", "Done", "Action"
    for row, task in enumerate(TASKS, start=1):
        cells[f"{row},0"] = task

    status = ttk.Label(frame, text="Edit a task, tick it, or click Show")
    status.pack(side="bottom", fill="x", pady=(12, 0))

    table = Table(
        frame,
        rows=len(TASKS) + 1,
        cols=3,
        titlerows=1,
        colwidth=16,
        rowstretch="all",
        colstretch="all",
        variable=cells,
    )
    table.pack(expand=True, fill="both")

    # ttk buttons are taller than one line of text.
    table.height(**{str(row): 2 for row in range(1, len(TASKS) + 1)})

    done = [tkinter.BooleanVar(root) for _ in TASKS]

    def show(row: int) -> None:
        """Show the task's current text (cells can be edited) and whether it is done."""
        state = "done" if done[row - 1].get() else "not done"
        status.configure(text=f"{cells[f'{row},0']}: {state}")

    for row in range(1, len(TASKS) + 1):
        checkbox = ttk.Checkbutton(table, variable=done[row - 1])
        button = ttk.Button(table, text="Show", command=lambda row=row: show(row))

        table.window_configure(f"{row},1", window=checkbox, sticky="nsew")
        table.window_configure(f"{row},2", window=button, sticky="nsew")

    run(root)


if __name__ == "__main__":
    main()
