from __future__ import annotations

from pathlib import Path
import subprocess

parts = sorted(Path("scripts/.global-audit-patch").glob("part-*.patch"))
if not parts:
    raise RuntimeError("global audit patch parts are missing")
patch = b"".join(path.read_bytes() for path in parts)
subprocess.run(["git", "apply", "--whitespace=error-all", "-"], input=patch, check=True)
print(f"Validated global audit cleanup applied from {len(parts)} temporary readable parts.")
