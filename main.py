#!/usr/bin/env python3
"""Deliver the finished page to the make.fun runner.

render.py paints the picture and leaves it next to this file as
entry.png. All this program does is carry those exact bytes into the
folder the grader points at, so repeat runs stay identical: no clock,
no network, no randomness anywhere in the chain.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "entry.png"
TARGET_NAME = "entry.png"


def destination() -> Path:
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(folder) / TARGET_NAME


def run() -> int:
    if not SOURCE.exists():
        print(f"entry image missing: {SOURCE}", file=sys.stderr)
        return 1
    out = destination()
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out)
    os.chmod(out, 0o644)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
