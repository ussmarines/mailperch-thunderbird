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
