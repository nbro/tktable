"""Flashing cells when their value changes, with a custom flash color.

Needs Tktable (check with ``python -m tktable``). Run it from the repository's root:

    poetry run python -m examples.flash

Pass ``-test`` to close the window after a second.
"""

import random

from examples.window import create_window, run
from tktable import ArrayVar, Table

DESCRIPTION = (
    'With flashmode="on", a cell whose value changes is drawn for a moment with the built-in '
    '"flash" tag, which is red by default. Here, prices change every second, and the flash tag is '
    "a soft yellow for half a second (flashtime=2, in quarter seconds). To stop flashing, leave "
    "flashmode off, its default."
)
STOCKS = ("ACME", "Globex", "Initech", "Umbrella", "Hooli")
UPDATE_EVERY = 1000  # milliseconds


def main() -> None:
    """Create a window with prices that change, and flash, every second."""
    root, frame = create_window("Flashing cells", DESCRIPTION)

    cells = ArrayVar(root)
    cells["0,0"], cells["0,1"] = "Stock", "Price"
    for row, stock in enumerate(STOCKS, start=1):
        cells[f"{row},0"], cells[f"{row},1"] = stock, "100.00"

    table = Table(
        frame,
        rows=len(STOCKS) + 1,
        cols=2,
        titlerows=1,
        colwidth=14,
        rowstretch="all",
        colstretch="all",
        flashmode="on",
        flashtime=2,
        variable=cells,
    )
    table.pack(expand=True, fill="both")
    table.tag_configure("flash", background="#fef3c7")

    def update_prices() -> None:
        row = random.randint(1, len(STOCKS))  # nosec B311: not for security
        price = float(cells[f"{row},1"]) * random.uniform(0.95, 1.05)  # nosec B311
        # With flashmode on, Tktable flashes the cell whose value changed.
        table.set(**{f"{row},1": f"{price:.2f}"})
        root.after(UPDATE_EVERY, update_prices)

    root.after(UPDATE_EVERY, update_prices)
    run(root)


if __name__ == "__main__":
    main()
