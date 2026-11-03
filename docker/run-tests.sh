#!/bin/sh
# Runs inside the test containers: starts a virtual display, diagnoses Tktable, runs the tests.
set -eu

Xvfb :99 -screen 0 1024x768x24 >/dev/null 2>&1 &
export DISPLAY=:99
sleep 1

python -m tktable
TKTABLE_REQUIRED=1 python -m pytest -v -rs
