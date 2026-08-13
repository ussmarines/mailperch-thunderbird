from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_organic_workspace_shell_is_loaded_and_structural():
    dashboard_html = text("extension/dashboard/dashboard.html")
    options_html = text("extension/options/options.html")
    dashboard_js = text("extension/dashboard/dashboard.js")
    options_js = text("extension/options/options.js")

    assert '../styles/workspace.css' in dashboard_html
    assert '../styles/workspace.css' in options_html
    assert "function enhanceOrganicDashboard()" in dashboard_js
    assert 'node("div", "workspace-frame")' in dashboard_js
    assert 'node("aside", "workspace-rail")' in dashboard_js
    assert 'node("aside", "workspace-inspector")' in dashboard_js
    assert "enhanceOrganicDashboard();" in dashboard_js
    assert "function enhanceOrganicSettingsWorkspace()" in options_js
    assert 'node("div", "settings-organic-frame")' in options_js
    assert 'node("section", "settings-organic-stage")' in options_js
    assert "enhanceOrganicSettingsWorkspace();" in options_js


def test_organic_design_avoids_generic_effects_and_remote_assets():
    workspace = text("extension/styles/workspace.css").lower()
    tokens = text("extension/styles/tokens.css").lower()
    combined = workspace + "\n" + tokens

    assert "linear-gradient" not in combined
    assert "radial-gradient" not in combined
    assert "backdrop-filter" not in combined
    assert "@import url(http" not in combined
    assert "--mp-font-family-display" in tokens
    assert "--mp-ease-organic" in tokens
    assert "prefers-reduced-motion" in workspace
    assert "forced-colors" in workspace


def test_panel_and_spec_follow_organic_workspace_contract():
    panel = text("extension/styles/pin.css")
    spec = text("docs/UI_SPEC.md")

    assert "Organic Workspace companion panel" in panel
    assert "@container threadPane" in panel
    assert "MailPin Organic Workspace" in spec
    assert "Typographie Fluent 2" not in spec
    assert "pas de dégradé" in spec.lower() or "dégradés" in spec.lower()
    assert "zoom 200 %" in spec
