# pylint: disable=missing-module-docstring
import subprocess  # nosec B404: runs this package's own diagnostic
import sys

# Lines `python -m tktable` prints when something is missing or broken.
PROBLEMS = ("NOT AVAILABLE", "NOT FOUND", "FAILED TO LOAD")


def test_diagnostic_exit_status_matches_its_output():
    """Runs `python -m tktable` as users do, in a separate process.

    Whatever is installed, the exit status must be 1 if a problem is reported, and 0 otherwise.
    """
    result = subprocess.run(  # nosec B603: fixed command
        [sys.executable, "-m", "tktable"], capture_output=True, text=True, check=False
    )

    assert result.stdout.startswith("Python:")

    problem_reported = any(problem in result.stdout for problem in PROBLEMS)
    assert result.returncode == (1 if problem_reported else 0), result.stdout
