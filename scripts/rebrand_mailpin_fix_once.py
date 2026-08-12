#!/usr/bin/env python3
"""Targeted one-shot adjustments after the MailPin migration. Removes itself."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

fr_path = ROOT / "extension/_locales/fr/messages.json"
data = json.loads(fr_path.read_text(encoding="utf-8"))
data["brandSubtitle"]["message"] = "Suivi d’e-mails & productivité pour Thunderbird."
fr_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

# Active brand asset references converge on the canonical scalable SVG.
text_suffixes = {".md", ".js", ".mjs", ".json", ".css", ".html", ".py", ".yml", ".yaml", ".txt", ".svg"}
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in text_suffixes:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    updated = text.replace("mailperch-icon", "mailpin-icon")
    for size in (16, 24, 32, 48, 64, 96, 128):
        updated = updated.replace(f"mailpin-icon-{size}.png", "mailpin-icon.svg")
    if updated != text:
        path.write_text(updated.rstrip() + "\n", encoding="utf-8", newline="\n")

# Keep static regressions strict while aligning them with the new canonical SVG and palette.
static_path = ROOT / "tests/static_checks.py"
static = static_path.read_text(encoding="utf-8")
static = static.replace("'viewBox=\"0 0 64 64\"' if icon.name.startswith(\"mailpin-icon\")", "'viewBox=\"0 0 128 128\"' if icon.name.startswith(\"mailpin-icon\")")
palette_replacements = {
    "#0f6cbd": "#4f7f75", "#115ea3": "#426f67", "#0e4775": "#355b55",
    "#ebf3fc": "#e8f0ee", "#dcecff": "#d9e8e4", "#77b7e8": "#86aaa2",
    "#0e8f8f": "#3d536b", "#0b7777": "#31465a", "#087f7f": "#3d536b", "#e3f7f5": "#e9edf1",
    "#f7f9fa": "#f4f1ea", "#f0f4f6": "#eeeae2", "#e7edef": "#e5e0d7", "#f4f7fb": "#f7f5f0",
    "#17232b": "#1a1d21", "#4e626d": "#566066", "#657983": "#6f777b", "#d5e0e4": "#d7d3ca", "#e2e9eb": "#e7e2d9", "#71848d": "#737b7e", "#07577d": "#3d536b",
    "#479ef5": "#9bc3bb", "#62abf5": "#b0d0c9", "#0c3156": "#203a36", "#0f3d69": "#294741", "#2886de": "#5e8f86",
    "#123b3a": "#202c36", "#5bd6d1": "#aebdcc"
}
for old, new in palette_replacements.items():
    static = static.replace(old, new)
static_path.write_text(static.rstrip() + "\n", encoding="utf-8", newline="\n")

Path(__file__).unlink()
print("MailPin targeted localization, SVG and palette-regression adjustments complete")
