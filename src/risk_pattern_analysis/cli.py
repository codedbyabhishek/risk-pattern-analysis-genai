from __future__ import annotations

import argparse
import json

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run risk pattern analysis pipeline")
    parser.add_argument("--input", required=True, help="Path to signup CSV")
    parser.add_argument("--output", default="outputs", help="Output directory")
    args = parser.parse_args()

    summary = run_pipeline(args.input, args.output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
