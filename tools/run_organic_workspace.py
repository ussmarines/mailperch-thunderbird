from pathlib import Path
import runpy

script = Path(__file__).with_name("apply_organic_workspace.py")
text = script.read_text(encoding="utf-8")
broken = """'--mp-font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI Variable\", \"Aptos\", \"Segoe UI\", sans-serif;',\n"""
# The source must use a comma between str.replace arguments. Keep this one-shot
# repair outside product files so a syntax mistake cannot reach the UI commit.
text = text.replace(
    """'--mp-font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI Variable\", \"Aptos\", \"Segoe UI\", sans-serif;';\n""",
    broken,
    1,
)
script.write_text(text, encoding="utf-8", newline="\n")
compile(text, str(script), "exec")
runpy.run_path(str(script), run_name="__main__")
