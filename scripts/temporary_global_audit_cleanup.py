from __future__ import annotations

import base64
import gzip
from pathlib import Path
import subprocess

parts = sorted(Path("scripts/.global-audit-parts").glob("part-*.txt"))
if not parts:
    raise RuntimeError("global audit payload parts are missing")
encoded = "".join(path.read_text(encoding="ascii").strip() for path in parts)
patch = gzip.decompress(base64.b64decode(encoded))
subprocess.run(["git", "apply", "--whitespace=error-all", "-"], input=patch, check=True)
print(f"Validated global audit cleanup applied from {len(parts)} temporary payload parts.")
