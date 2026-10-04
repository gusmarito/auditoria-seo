#!/usr/bin/env python3
"""Static guardrail checks for Colli&Co HTML slide decks."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


FORBIDDEN_TEXT = {
    "–": "en dash",
    "—": "em dash",
    "~": "approximation tilde",
}

META_PATTERNS = [
    r"\bneste slide\b",
    r"\bnesta apresentação\b",
    r"\bcomo podemos ver\b",
    r"\bgerad[oa] por (?:ia|inteligência artificial)\b",
    r"\bprompt\b",
    r"\bmetalinguagem\b",
    r"\bo layout\b",
]


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_style = 0
        self.in_script = 0
        self.in_slide = False
        self.current_slide = -1
        self.slides: list[dict] = []
        self.in_heading = 0
        self.in_paragraph = 0
        self.current_text: list[str] = []
        self.current_paragraph: list[str] = []
        self.li_depth = 0
        self.li_has_icon = False
        self.li_text: list[str] = []
        self.lists: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        classes = set((attrs_map.get("class") or "").split())

        if tag == "style":
            self.in_style += 1
        if tag == "script":
            self.in_script += 1

        if tag == "section" and "slide" in classes:
            self.in_slide = True
            self.current_slide += 1
            self.slides.append(
                {
                    "classes": classes,
                    "text": [],
                    "headings": [],
                    "paragraphs": [],
                }
            )
        if not self.in_slide or self.in_style or self.in_script:
            return

        if tag in {"h1", "h2", "h3"}:
            self.in_heading += 1
            self.current_text = []

        if tag == "p":
            self.in_paragraph += 1
            self.current_paragraph = []

        if tag == "li":
            self.li_depth = 1
            self.li_has_icon = False
            self.li_text = []
        elif self.li_depth:
            self.li_depth += 1

        if self.li_depth and (
            tag == "svg"
            or tag == "use"
            or "icon" in classes
            or "icon-box" in classes
        ):
            self.li_has_icon = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = max(0, self.in_style - 1)
        if tag == "script":
            self.in_script = max(0, self.in_script - 1)

        if self.in_slide and not self.in_style and not self.in_script:
            if tag in {"h1", "h2", "h3"} and self.in_heading:
                heading = normalize(" ".join(self.current_text))
                if heading:
                    self.slides[self.current_slide]["headings"].append(heading)
                self.in_heading -= 1
                self.current_text = []

            if tag == "p" and self.in_paragraph:
                paragraph = normalize(" ".join(self.current_paragraph))
                if paragraph:
                    self.slides[self.current_slide]["paragraphs"].append(paragraph)
                self.in_paragraph -= 1
                self.current_paragraph = []

            if tag == "li" and self.li_depth:
                self.lists.append(
                    {
                        "slide": self.current_slide + 1,
                        "text": normalize(" ".join(self.li_text)),
                        "has_icon": self.li_has_icon,
                    }
                )

            if self.li_depth:
                self.li_depth = max(0, self.li_depth - 1)

            if tag == "section":
                self.in_slide = False

    def handle_data(self, data: str) -> None:
        if not self.in_slide or self.in_style or self.in_script:
            return

        text = normalize(data)
        if not text:
            return

        self.slides[self.current_slide]["text"].append(text)

        if self.in_heading:
            self.current_text.append(text)
        if self.in_paragraph:
            self.current_paragraph.append(text)
        if self.li_depth:
            self.li_text.append(text)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="Path to index.html")
    args = parser.parse_args()

    html_path = Path(args.html).expanduser().resolve()
    if not html_path.is_file():
        print(f"ERROR: file not found: {html_path}")
        return 2

    source = html_path.read_text(encoding="utf-8")
    parsed = DeckParser()
    parsed.feed(source)

    errors: list[str] = []
    warnings: list[str] = []

    required_source = {
        "1600px slide width": r"\bwidth:\s*1600px",
        "900px slide height": r"\bheight:\s*900px",
        "centered deck transform": r"translate\(\s*-50%\s*,\s*-50%\s*\)\s*scale",
        "visualViewport scaling": r"visualViewport",
        "progress fill": r"class=[\"'][^\"']*progress-fill",
        "previous control": r"data-testid=[\"']prev-slide[\"']",
        "next control": r"data-testid=[\"']next-slide[\"']",
        "Colli red logo": r"colli-red\.png",
        "Colli white logo": r"colli-white\.png",
        "reduced motion support": r"prefers-reduced-motion",
    }

    for label, pattern in required_source.items():
        if not re.search(pattern, source, flags=re.I):
            errors.append(f"Missing {label}")

    if not parsed.slides:
        errors.append("No <section class=\"slide\"> elements found")

    for index, slide in enumerate(parsed.slides, start=1):
        text = normalize(" ".join(slide["text"]))

        if not text:
            errors.append(f"Slide {index:02d}: no visible text")
        if re.search(r"\b(?:título|conteúdo|categoria) aprovado\b", text, flags=re.I):
            errors.append(f"Slide {index:02d}: starter placeholder text remains")
        if re.search(r"\b(?:lorem ipsum|placeholder)\b", text, flags=re.I):
            errors.append(f"Slide {index:02d}: placeholder copy remains")
        if not slide["headings"]:
            warnings.append(f"Slide {index:02d}: no h1, h2, or h3 heading")

        for char, label in FORBIDDEN_TEXT.items():
            if char in text:
                errors.append(f"Slide {index:02d}: contains {label} ({char})")

        if re.search(r"\s-\s", text):
            errors.append(f"Slide {index:02d}: contains prose hyphen separator")

        for pattern in META_PATTERNS:
            if re.search(pattern, text, flags=re.I):
                errors.append(
                    f"Slide {index:02d}: contains metalinguage matching {pattern}"
                )

        for paragraph in slide["paragraphs"]:
            if len(paragraph) > 230:
                warnings.append(
                    f"Slide {index:02d}: paragraph has {len(paragraph)} characters"
                )

    for item in parsed.lists:
        if not item["has_icon"]:
            errors.append(
                f"Slide {item['slide']:02d}: bullet without icon: {item['text'][:70]}"
            )

    backgrounds = []
    for slide in parsed.slides:
        classes = slide["classes"]
        if "red" in classes:
            backgrounds.append("red")
        elif "dark" in classes:
            backgrounds.append("dark")
        elif "white" in classes:
            backgrounds.append("white")
        else:
            backgrounds.append("light")

    for index in range(len(backgrounds) - 2):
        group = backgrounds[index : index + 3]
        if len(set(group)) == 1:
            warnings.append(
                f"Slides {index + 1:02d}-{index + 3:02d}: repeated {group[0]} background"
            )

    for logo in ("colli-red.png", "colli-white.png"):
        if logo in source:
            candidate = html_path.parent / "assets" / logo
            if not candidate.is_file():
                errors.append(f"Missing referenced asset: {candidate}")

    print(f"Slides: {len(parsed.slides)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASSED: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
