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

Path(__file__).unlink()
print("MailPin targeted localization and scalable asset-reference adjustments complete")
