from pathlib import Path
import runpy

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

# Replace the old Fluent-era literal with a stronger invariant: the preferred
# faces must be local, system-ui remains the guaranteed fallback, and Inter is
# still forbidden because MailPin ships no third-party font asset.
guard = Path(__file__).resolve().parents[1] / "tests/test_ui_regressions.py"
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
