#!/bin/bash
set -e

# Check Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi

# Create venv
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

mkdir -p logs reports

echo
echo "SentinelIR is now installed!"
echo "Run using:"
echo "  sentinelir analyse"
echo "  sentinelir monitor"
echo "  sentinelir generate"
echo "  sentinelir web"

exit 0