#!/usr/bin/env python3
"""Build compact QA contact sheets from rendered slide PNGs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Folder containing slide PNG files")
    parser.add_argument("--output", required=True, help="Output folder")
    parser.add_argument("--per-sheet", type=int, default=8)
    args = parser.parse_args()

    source = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    files = sorted(source.glob("*.png"))

    if not files:
        raise SystemExit(f"No PNG files found in {source}")

    output.mkdir(parents=True, exist_ok=True)
    per_sheet = max(1, min(args.per_sheet, 8))
    columns = 4
    thumb_w = 392
    thumb_h = 221
    slot_w = 400
    slot_h = 252

    for sheet_index in range(math.ceil(len(files) / per_sheet)):
        batch = files[
            sheet_index * per_sheet : (sheet_index + 1) * per_sheet
        ]
        rows = math.ceil(len(batch) / columns)
        canvas = Image.new("RGB", (columns * slot_w, rows * slot_h), (18, 18, 18))
        draw = ImageDraw.Draw(canvas)

        for index, file in enumerate(batch):
            image = Image.open(file).convert("RGB")
            image.thumbnail((thumb_w, thumb_h))
            x = (index % columns) * slot_w + 4
            y = (index // columns) * slot_h + 24
            canvas.paste(image, (x, y))
            draw.text((x + 6, 6 + (index // columns) * slot_h), file.stem, fill="white")

        destination = output / f"contact-sheet-{sheet_index + 1:02d}.jpg"
        canvas.save(destination, quality=92)
        print(destination)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
