from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_between(text, start, end, replacement, label):
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"missing start marker: {label}")
    b = text.find(end, a)
    if b < 0:
        raise SystemExit(f"missing end marker: {label}")
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]

options_path = ROOT / "extension/options/options.js"
options = options_path.read_text(encoding="utf-8")
options = replace_between(options, "function reorderSettingsFamilies() {", "function renderRules(){", '''function reorderSettingsFamilies() {
  const form = $("settings-form");
  const tail = form.querySelector(".form-footer");
  if (!tail) return;
  for (const heading of form.querySelectorAll(".settings-family-heading")) heading.remove();
  for (const family of ["Essentiel", "Automatisation", "Organisation", "Avancé"]) {
    const sections = [...form.querySelectorAll(`:scope > .settings-section[data-nav-group="${family}"]`)];
    for (const section of sections) form.insertBefore(section, tail);
  }
}''', "reorderSettingsFamilies")
options = replace_between(options, "function enhanceOrganicSettingsWorkspace() {", "function installCriticalSettingsActions() {", '''function enhanceOrganicSettingsWorkspace() {
  if (document.body.dataset.workspaceEnhanced === "true") return;
  const app = document.querySelector(".settings-app");
  const layout = app?.querySelector(".settings-layout");
  const sidebar = layout?.querySelector(".settings-sidebar");
  const header = app?.querySelector(".page-header");
  const overview = app?.querySelector(".quick-overview");
  const loading = $("settings-loading");
  const failure = $("settings-error");
  const form = $("settings-form");
  const status = $("status");
  const saveDock = $("save-dock");
  if (!app || !layout || !sidebar || !header || !overview || !loading || !failure || !form) throw new Error("Structure Options incompatible avec Organic Workspace.");
  document.body.classList.add("mp-organic-settings");
  document.body.dataset.workspaceEnhanced = "true";
  const frame = node("div", "settings-organic-frame");
  const brand = node("div", "settings-organic-brand");
  const icon = document.createElement("img");
  icon.src = "../icons/mailpin-icon.svg"; icon.alt = ""; icon.width = 34; icon.height = 34;
  const brandCopy = node("div", "");
  brandCopy.append(node("strong", "", "MailPin"), node("span", "", "Workspace settings"));
  brand.append(icon, brandCopy); sidebar.prepend(brand);
  const headerActions = header.querySelector(".header-actions");
  if (saveDock && headerActions) { saveDock.classList.add("header-save-dock"); headerActions.prepend(saveDock); }
  const stage = node("section", "settings-organic-stage");
  stage.append(header);
  if (status) stage.append(status);
  stage.append(overview, loading, failure, form);
  frame.append(sidebar, stage);
  app.replaceChildren(frame);
}''', "enhanceOrganicSettingsWorkspace")
options_path.write_text(options, encoding="utf-8")

dashboard_path = ROOT / "extension/dashboard/dashboard.js"
dashboard = dashboard_path.read_text(encoding="utf-8")
old = '  const stage = node("main", "workspace-stage");\n  stage.append(header, stats, reminders, content);'
new = '  const stage = node("main", "workspace-stage");\n  const status = $("status");\n  stage.append(header);\n  if (status) stage.append(status);\n  stage.append(stats, reminders, content);'
if old not in dashboard: raise SystemExit("dashboard stage marker missing")
dashboard_path.write_text(dashboard.replace(old, new, 1), encoding="utf-8")

workspace_path = ROOT / "extension/styles/workspace.css"
workspace = workspace_path.read_text(encoding="utf-8")
workspace = workspace.replace(".settings-organic-stage > .settings-inline-status {", ".settings-organic-stage > #status {")
workspace = workspace.replace(".workspace-stage > .status {", ".workspace-stage > #status {")
workspace_path.write_text(workspace, encoding="utf-8")

test_path = ROOT / "tests/test_organic_workspace_ui.py"
test = test_path.read_text(encoding="utf-8")
needle = '    assert \'body.mp-organic-settings[data-dirty] #settings-form\' in workspace_css\n'
replacement = '''    assert ".header-save-dock" in workspace_css
    assert ".item-more-menu { position: static" in workspace_css
    assert ".stats-secondary { position: static" in workspace_css
    assert "Canonical workspace stylesheet" in workspace_css
    assert "Organic Workspace V2 — responsive composition" not in workspace_css
    assert 'saveDock.classList.add("header-save-dock")' in options_js
    assert 'for (const family of ["Essentiel", "Automatisation", "Organisation", "Avancé"])' in options_js
    assert 'node("div", "settings-family-heading")' not in options_js
    assert 'const status = $("status");' in dashboard_js
'''
if needle not in test: raise SystemExit("test contract marker missing")
test_path.write_text(test.replace(needle, replacement, 1), encoding="utf-8")
print("Canonical UI rebuild applied directly to source files.")
