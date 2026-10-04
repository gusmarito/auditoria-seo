#!/usr/bin/env python3
"""Copy the canonical Colli&Co HTML deck starter to a new output folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Absolute or relative output folder")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite starter-owned files when they already exist",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    starter = skill_root / "assets" / "starter"
    output = Path(args.output).expanduser().resolve()

    if not starter.is_dir():
        raise SystemExit(f"Starter not found: {starter}")

    output.mkdir(parents=True, exist_ok=True)

    for source in starter.rglob("*"):
        relative = source.relative_to(starter)
        destination = output / relative

        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        if destination.exists() and not args.force:
            raise SystemExit(
                f"Refusing to overwrite {destination}. Use --force if intentional."
            )

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
