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

# Reuse an existing localized string rather than growing FR/EN locale catalogs
# for a navigation landmark whose accessible name is already covered by the
# Dashboard title.
dashboard = root / "extension/dashboard/dashboard.js"
dashboard_text = dashboard.read_text(encoding="utf-8")
old_aria = 'rail.setAttribute("aria-label", msg("ariaDashboardViews", "Navigation MailPin"));'
new_aria = 'rail.setAttribute("aria-label", msg("dashboardTitle", "MailPin"));'
if old_aria not in dashboard_text:
    raise RuntimeError("dashboard.js: workspace rail aria anchor not found")
dashboard.write_text(dashboard_text.replace(old_aria, new_aria, 1), encoding="utf-8", newline="\n")

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

# Static token guard must follow the canonical design values rather than freeze
# the pre-Organic palette and motion timings.
static_checks = root / "tests/static_checks.py"
static_text = static_checks.read_text(encoding="utf-8")
replacements = {
    '"--mp-brand-background: #4f7f75", "--mp-secondary-background: #3d536b",': '"--mp-brand-background: #4e7569", "--mp-secondary-background: #46575d",',
    '"--mp-color-neutral-background-canvas: #f7f5f0", "--mp-color-neutral-background-canvas: #111315",': '"--mp-color-neutral-background-canvas: #f4f1e9", "--mp-color-neutral-background-canvas: #121512",',
    '"--mp-radius-lg: var(--mp-radius-xxlarge)", "--mp-duration-normal: 180ms"': '"--mp-radius-lg: var(--mp-radius-xxlarge)", "--mp-duration-normal: 220ms",\n    "--mp-radius-organic-lg: 20px", "--mp-ease-organic"',
}
for old, new in replacements.items():
    if old not in static_text:
        raise RuntimeError(f"tests/static_checks.py: token guard anchor not found: {old}")
    static_text = static_text.replace(old, new, 1)
static_checks.write_text(static_text, encoding="utf-8", newline="\n")
