# pylint: disable=missing-module-docstring, missing-function-docstring, unused-argument
import os
import subprocess  # nosec B404: runs this repository's own examples
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent

# Every example, run as a module (e.g. examples.tags). window.py is the examples' shared setup.
EXAMPLES = sorted(
    f"examples.{path.stem}"
    for path in (ROOT / "examples").glob("*.py")
    if path.stem not in ("__init__", "window")
)


@pytest.mark.tktable
@pytest.mark.parametrize("example", EXAMPLES)
def test_example_runs_without_errors(example, table_root):
    """Runs each example with -test (it closes after a second), in a separate process.

    The table_root fixture skips this when Tktable is not available. Errors raised in Tk callbacks
    don't change the exit status, so the output is checked for tracebacks too.
    """
    result = subprocess.run(  # nosec B603: fixed command
        [sys.executable, "-m", example, "-test"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
        env=os.environ.copy(),
    )

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr, result.stderr
