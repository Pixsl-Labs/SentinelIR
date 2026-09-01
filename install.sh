#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

set -euo pipefail

# Check Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi

# Create venv
python3 -m venv .venv

# Update pip
.venv/bin/python -m pip install --upgrade pip

# Install dependencies
.venv/bin/python -m pip install -r requirements.txt

mkdir -p logs reports

chmod +x analyse monitor generate web

echo
echo "SentinelIR is now installed!"
echo
echo "Run using:"
echo "  ./analyse"
echo "  ./monitor"
echo "  ./generate"
echo "  ./web"

exit 0
