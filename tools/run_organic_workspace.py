from pathlib import Path
import runpy

root = Path(__file__).resolve().parents[1]
script = Path(__file__).with_name("apply_organic_workspace.py")
text = script.read_text(encoding="utf-8")

# Keep small one-shot repairs outside product files so transformer mistakes
# fail closed before any validated UI delta is committed.
text = text.replace(
    """'--mp-font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI Variable\", \"Aptos\", \"Segoe UI\", sans-serif;';\n""",
    """'--mp-font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI Variable\", \"Aptos\", \"Segoe UI\", sans-serif;',\n""",
    1,
)
text = text.replace(
    """'  <link rel=\"stylesheet\" href=\"dashboard.css\">\\n',""",
    """'  <link rel=\"stylesheet\" href=\"./dashboard.css\">\\n',""",
    1,
)
text = text.replace(
    """'  <link rel=\"stylesheet\" href=\"dashboard.css\">\\n  <link rel=\"stylesheet\" href=\"../styles/workspace.css\">\\n',""",
    """'  <link rel=\"stylesheet\" href=\"./dashboard.css\">\\n  <link rel=\"stylesheet\" href=\"../styles/workspace.css\">\\n',""",
    1,
)

script.write_text(text, encoding="utf-8", newline="\n")
compile(text, str(script), "exec")
runpy.run_path(str(script), run_name="__main__")

# Typography guard: local preferred faces + guaranteed system fallback.
guard = root / "tests/test_ui_regressions.py"
guard_text = guard.read_text(encoding="utf-8")
old_guard = "assert '--mp-font-family: system-ui,' in tokens\nassert '--mp-font-family: Inter,' not in tokens\n"
new_guard = (
    "assert '--mp-font-family: \\\"Segoe UI Variable Text\\\", \\\"Aptos\\\", system-ui,' in tokens\n"
    "assert '--mp-font-family-display: \\\"Segoe UI Variable Display\\\", \\\"Aptos Display\\\"' in tokens\n"
    "assert '--mp-font-family: Inter,' not in tokens\n"
)
if old_guard not in guard_text:
    raise RuntimeError("test_ui_regressions.py: typography guard anchor not found")
guard.write_text(guard_text.replace(old_guard, new_guard, 1), encoding="utf-8", newline="\n")

# Historical visual-polish guard: preserve its intent while accepting the new
# shared workspace layer and the new canonical palette.
polish = root / "tests/test_ui_polish_3_2_3.py"
polish_text = polish.read_text(encoding="utf-8")
polish_text = polish_text.replace(
    'options_css = (ROOT / "extension/options/options.css").read_text(encoding="utf-8")\n',
    'options_css = (ROOT / "extension/options/options.css").read_text(encoding="utf-8")\nworkspace_css = (ROOT / "extension/styles/workspace.css").read_text(encoding="utf-8")\n',
    1,
)
old_identity = '''# Fluent identity remains shared rather than duplicated by each HTML surface.\nfor token in (\n    "--mp-brand-background: #4f7f75", "--mp-secondary-background: #3d536b",\n    ":root[data-mp-theme=\\"dark\\"]", "--mp-radius-lg: var(--mp-radius-xxlarge)",\n    "--mp-shadow-low",\n):\n    assert token in tokens_css, token\n'''
new_identity = '''# Organic Workspace identity remains shared rather than duplicated by each HTML surface.\nfor token in (\n    "--mp-brand-background: #4e7569", "--mp-secondary-background: #46575d",\n    ":root[data-mp-theme=\\"dark\\"]", "--mp-radius-organic-lg: 20px",\n    "--mp-shadow-organic-low", "--mp-ease-organic",\n):\n    assert token in tokens_css, token\nassert "linear-gradient" not in workspace_css\nassert "radial-gradient" not in workspace_css\n'''
if old_identity not in polish_text:
    raise RuntimeError("test_ui_polish_3_2_3.py: Fluent identity guard anchor not found")
polish_text = polish_text.replace(old_identity, new_identity, 1)
polish_text = polish_text.replace(
    'assert re.search(rf"\\.{re.escape(class_name)}(?=[\\s,:.#>+~\\[]|\\{{)", options_css), f"Missing options CSS class: {class_name}"',
    'assert re.search(rf"\\.{re.escape(class_name)}(?=[\\s,:.#>+~\\[]|\\{{)", options_css + "\\n" + workspace_css), f"Missing options CSS class: {class_name}"',
    1,
)
polish.write_text(polish_text, encoding="utf-8", newline="\n")
