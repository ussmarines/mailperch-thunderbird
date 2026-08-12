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
Path(__file__).unlink()
print("MailPin targeted localization adjustment complete")
