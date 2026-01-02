#!/usr/bin/env bash
set -euo pipefail

# Create or Update Python Virtual Environment
echo "Creating/Updating Python Virtual Environment..."

# Move to script directory and then project root
cd "$(dirname "$0")/.." || { echo "Failed to change directory to project root"; exit 1; }

# Detect Python command (prefer `python`, fallback to `python3`)
PYTHON_CMD=""
if command -v python >/dev/null 2>&1; then
	PYTHON_CMD=python
elif command -v python3 >/dev/null 2>&1; then
	PYTHON_CMD=python3
else
	echo "Python is not installed or not in PATH." >&2
	exit 1
fi

# Use a local venv to avoid modifying system-managed Python
VENV_DIR=".venv"
VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

echo "Ensuring local venv exists at $VENV_DIR..."
if [ ! -x "$VENV_PY" ]; then
	echo "Creating virtual environment..."
	if ! $PYTHON_CMD -m venv "$VENV_DIR"; then
		echo "Failed to create virtual environment with $PYTHON_CMD." >&2
		exit 1
	fi
fi

echo "Upgrading pip inside venv and installing uv..."
if ! "$VENV_PY" -m pip install --upgrade pip; then
	echo "Failed to upgrade pip inside venv." >&2
	exit 1
fi

if ! "$VENV_PIP" install uv; then
	echo "Failed to install uv into venv." >&2
	exit 1
fi

echo "Creating/updating project venv using uv inside local venv..."
if ! "$VENV_PY" -m uv venv --allow-existing; then
	echo "Failed to sync dependencies with uv inside venv." >&2
	exit 1
fi

echo "Completed venv creation."
exit 0
