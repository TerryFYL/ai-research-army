#!/usr/bin/env python3
"""Basic gate checker for the public AI Research Army pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED = {
    "intake": ["requirement_v1.md"],
    "data-explore": ["data_dictionary.md"],
    "research-design": ["research_plan.md"],
    "statistics": ["analysis_results.md"],
    "literature": ["verified_ref_pool.md"],
    "manuscript": ["manuscript.md"],
    "review": ["quality_report.md"],
    "submission": ["submission_package"],
    "delivery": ["delivery"],
}


def has_any(root: Path, names: list[str]) -> bool:
    return any((root / name).exists() for name in names)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True)
    parser.add_argument("--dir", required=True)
    args = parser.parse_args()

    root = Path(args.dir)
    phase = args.phase

    if phase not in REQUIRED:
        print(f"UNKNOWN_PHASE {phase}")
        return 2

    missing = [name for name in REQUIRED[phase] if not (root / name).exists()]
    if missing and not has_any(root, REQUIRED[phase]):
        print(f"BLOCK {phase}: missing required artifacts -> {', '.join(missing)}")
        return 1

    print(f"PASS {phase}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
