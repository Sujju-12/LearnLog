#!/usr/bin/env bash
set -euo pipefail

# Idempotent install for Cloud Agent environments.
# Uses python3 -m so the learnlog CLI works without ~/.local/bin on PATH.
python3 -m pip install -e ".[dev]"
