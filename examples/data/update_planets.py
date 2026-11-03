"""Download the planets' data from NASA's Planetary Fact Sheet into planets.json.

The example reads planets.json, so it works offline; run this only to refresh the data:

    poetry run poe update_example_data

It only uses the standard library. Review the changes (git diff) before committing them.
"""

import json
import re
import urllib.request
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path

SOURCE_URL = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html"
OUTPUT = Path(__file__).with_name("planets.json")
PLANETS = ("MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE")

# JSON key -> the start of the row label in NASA's table.
ROWS = {
    "diameter_km": "Diameter",
    "mass_1e24_kg": "Mass",
    "distance_from_sun_1e6_km": "Distance from Sun",
    "day_hours": "Length of Day",
    "year_days": "Orbital Period",
    "moons": "Number of Moons",
    "mean_temperature_c": "Mean Temperature",
}


class TableParser(HTMLParser):
    """Collects the text of each cell of each row of the page's first table."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._in_table = False
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table" and not self.rows:
            self._in_table = True
        elif self._in_table and tag == "tr":
            self.rows.append([])
        elif self._in_table and tag in ("td", "th"):
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            self._in_table = False
        elif tag in ("td", "th") and self._cell is not None and self.rows:
            self.rows[-1].append(" ".join("".join(self._cell).split()))
            self._cell = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def download(url: str) -> str:
    """Return the page's HTML."""
    request = urllib.request.Request(url, headers={"User-Agent": "pytktable-example-data"})
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310: fixed https URL
        return response.read().decode("utf-8", errors="replace")


def to_number(text: str) -> int | float:
    """Convert e.g. "12,104" or "0.384*" to a number."""
    cleaned = text.replace(",", "").replace("*", "").strip()
    return float(cleaned) if "." in cleaned else int(cleaned)


def last_updated(html: str) -> str | None:
    """Return the page's "Last Updated" date as YYYY-MM-DD, if found."""
    match = re.search(r"Last Updated:\s*(\d{1,2} \w+ \d{4})", html)
    if not match:
        return None
    return datetime.strptime(match.group(1), "%d %B %Y").date().isoformat()


def parse_planets(html: str) -> list[dict[str, str | int | float]]:
    """Extract the planets' rows we use from NASA's table."""
    parser = TableParser()
    parser.feed(html)

    header = next(row for row in parser.rows if "MERCURY" in [c.upper() for c in row])
    columns = {name: [c.upper() for c in header].index(name) for name in PLANETS}

    planets: list[dict[str, str | int | float]] = [{"name": name.title()} for name in PLANETS]
    for key, label in ROWS.items():
        row = next(row for row in parser.rows if row and row[0].startswith(label))
        for planet, name in zip(planets, PLANETS):
            planet[key] = to_number(row[columns[name]])

    return planets


def main() -> None:
    """Download, parse and save the data."""
    html = download(SOURCE_URL)
    data = {
        "source": "NASA Planetary Fact Sheet (metric)",
        "source_url": SOURCE_URL,
        "source_last_updated": last_updated(html),
        "retrieved": date.today().isoformat(),
        "update_with": "poetry run poe update_example_data",
        "planets": parse_planets(html),
    }
    OUTPUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(data['planets'])} planets to {OUTPUT}")


if __name__ == "__main__":
    main()
