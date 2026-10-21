"""Run the simulator headless once per recipe and collect the metrics CSVs.

Usage:
    python experiments/run_batch.py --line line2 experiments/recipes/*.yaml

Each run launches Godot with ``--headless`` and passes the recipe and output
path as user args (after ``--``); the Godot side reads them in core/main.gd.
Phase 3 work: the Godot side does not consume recipes yet.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

GODOT = "/Applications/Godot.app/Contents/MacOS/Godot"
REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--line", required=True)
    p.add_argument("--godot", default=GODOT)
    p.add_argument("recipes", nargs="+", type=Path)
    args = p.parse_args()

    runs = REPO / "runs"
    runs.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for recipe in args.recipes:
        out = runs / f"{stamp}_{args.line}_{recipe.stem}.csv"
        cmd = [args.godot, "--headless", "--path", str(REPO / "godot"), "--",
               "--line", args.line, "--recipe", str(recipe), "--out", str(out)]
        print(" ".join(cmd))
        rc = subprocess.call(cmd)
        if rc != 0:
            print(f"run failed for {recipe}: exit {rc}", file=sys.stderr)
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
