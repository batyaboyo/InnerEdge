#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_EXE="$ROOT_DIR/.venv/Scripts/python.exe"

if [[ ! -x "$PYTHON_EXE" ]]; then
  echo "Python venv executable not found at: $PYTHON_EXE"
  echo "Run setup first or adjust the script for your environment."
  exit 1
fi

echo "[1/3] Running backend tests"
"$PYTHON_EXE" -m pytest -q

echo "[2/3] Running frontend verify"
cd "$ROOT_DIR/frontend"
npm run verify

echo "[3/3] Verification complete"
