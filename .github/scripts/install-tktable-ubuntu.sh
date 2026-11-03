#!/usr/bin/env bash
# Installs Tktable and a virtual display on a GitHub Actions Ubuntu runner, and tells the next
# steps where Tktable is, because setup-python's Python may not search the distro's Tcl folders.
set -euo pipefail

sudo apt-get update
sudo apt-get install -y tk-table xvfb

pkg_index="$(dpkg -L tk-table | grep pkgIndex.tcl | head -1)"
echo "Found Tktable: $(dirname "$pkg_index")"

echo "TKTABLE_LIBRARY=$(dirname "$pkg_index")" >> "$GITHUB_ENV"
echo "TKTABLE_REQUIRED=1" >> "$GITHUB_ENV"
