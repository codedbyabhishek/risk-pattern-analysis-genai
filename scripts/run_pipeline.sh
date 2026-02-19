#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHONPATH="$ROOT_DIR/src" python3 -m risk_pattern_analysis.cli \
  --input "$ROOT_DIR/data/sample_signups.csv" \
  --output "$ROOT_DIR/outputs"
