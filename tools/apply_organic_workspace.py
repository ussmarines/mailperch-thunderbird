from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one occurrence, found {count}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")


# --- Shared tokens: keep semantic compatibility aliases, replace the Fluent look. ---
tokens_path = "extension/styles/tokens.css"
tokens = read(tokens_path)
tokens = tokens.replace(
    "/* MailPin product design tokens.\n * Global values are separated from semantic aliases so every surface can share\n * the same light, dark and high-contrast behavior without hard-coded overrides. */",
    "/* MailPin Organic Workspace design tokens.\n * Semantic aliases remain stable for Thunderbird integration while the visual\n * language is intentionally independent from Fluent or any external library. */",
)
tokens = tokens.replace(
    '--mp-font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI Variable", "Aptos", "Segoe UI", sans-serif;',
    '--mp-font-family: "Segoe UI Variable Text", "Aptos", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;\n'
    '  --mp-font-family-display: "Segoe UI Variable Display", "Aptos Display", "Segoe UI Variable Text", system-ui, sans-serif;\n'
    '  --mp-font-family-mono: "Cascadia Code", "SFMono-Regular", Consolas, monospace;'
)
tokens = tokens.replace("/* Fluent neutral aliases — light */", "/* Neutral workspace aliases — light */")
tokens = tokens.replace("--mp-brand-background: #4f7f75;", "--mp-brand-background: #4e7569;")
tokens = tokens.replace("--mp-brand-background-hover: #426f67;", "--mp-brand-background-hover: #3d655a;")
tokens = tokens.replace("--mp-brand-background-pressed: #355b55;", "--mp-brand-background-pressed: #2d5148;")
tokens = tokens.replace("--mp-brand-foreground: #4f7f75;", "--mp-brand-foreground: #466e63;")
tokens = tokens.replace("--mp-brand-foreground-hover: #426f67;", "--mp-brand-foreground-hover: #355d53;")
tokens = tokens.replace("--mp-brand-subtle: #e8f0ee;", "--mp-brand-subtle: #e2ebe6;")
tokens = tokens.replace("--mp-brand-subtle-hover: #d9e8e4;", "--mp-brand-subtle-hover: #d5e3dd;")
tokens = tokens.replace("--mp-brand-stroke: #86aaa2;", "--mp-brand-stroke: #83a79d;")
tokens = tokens.replace("--mp-secondary-background: #3d536b;", "--mp-secondary-background: #46575d;")
tokens = tokens.replace("--mp-secondary-background-hover: #31465a;", "--mp-secondary-background-hover: #394b51;")
tokens = tokens.replace("--mp-secondary-foreground: #3d536b;", "--mp-secondary-foreground: #46575d;")
tokens = tokens.replace("--mp-secondary-subtle: #e9edf1;", "--mp-secondary-subtle: #e5e9e8;")
tokens = tokens.replace("--mp-color-neutral-background-2: #f4f1ea;", "--mp-color-neutral-background-2: #efebe2;")
tokens = tokens.replace("--mp-color-neutral-background-3: #eeeae2;", "--mp-color-neutral-background-3: #e9e5dc;")
tokens = tokens.replace("--mp-color-neutral-background-4: #e5e0d7;", "--mp-color-neutral-background-4: #e1dcd1;")
tokens = tokens.replace("--mp-color-neutral-background-canvas: #f7f5f0;", "--mp-color-neutral-background-canvas: #f4f1e9;")
tokens = tokens.replace("--mp-color-neutral-foreground-1: #1a1d21;", "--mp-color-neutral-foreground-1: #171a18;")
tokens = tokens.replace("--mp-color-neutral-foreground-2: #566066;", "--mp-color-neutral-foreground-2: #59615d;")
tokens = tokens.replace("--mp-color-neutral-foreground-3: #6f777b;", "--mp-color-neutral-foreground-3: #767d78;")
tokens = tokens.replace("--mp-color-neutral-stroke-1: #d7d3ca;", "--mp-color-neutral-stroke-1: #d8d3c8;")
tokens = tokens.replace("--mp-color-neutral-stroke-2: #e7e2d9;", "--mp-color-neutral-stroke-2: #e5e0d6;")
tokens = tokens.replace("--mp-color-neutral-stroke-accessible: #737b7e;", "--mp-color-neutral-stroke-accessible: #787e79;")
tokens = tokens.replace("--mp-color-neutral-stroke-focus: #3d536b;", "--mp-color-neutral-stroke-focus: #466e63;")
tokens = tokens.replace("--mp-radius-small: 4px;", "--mp-radius-small: 6px;")
tokens = tokens.replace("--mp-radius-medium: 6px;", "--mp-radius-medium: 9px;")
tokens = tokens.replace("--mp-radius-large: 8px;", "--mp-radius-large: 12px;")
tokens = tokens.replace("--mp-radius-xlarge: 10px;", "--mp-radius-xlarge: 15px;")
tokens = tokens.replace("--mp-radius-xxlarge: 12px;", "--mp-radius-xxlarge: 20px;")
tokens = tokens.replace("--mp-shadow-2: 0 1px 2px rgb(18 39 51 / 0.05);", "--mp-shadow-2: 0 1px 2px rgb(23 26 24 / 0.05);")
tokens = tokens.replace("--mp-shadow-4: 0 2px 5px rgb(18 39 51 / 0.06);", "--mp-shadow-4: 0 2px 6px rgb(23 26 24 / 0.07);")
tokens = tokens.replace("--mp-shadow-8: 0 4px 10px rgb(18 39 51 / 0.08);", "--mp-shadow-8: 0 5px 14px rgb(23 26 24 / 0.09);")
tokens = tokens.replace("--mp-shadow-16: 0 8px 18px rgb(18 39 51 / 0.10);", "--mp-shadow-16: 0 10px 26px rgb(23 26 24 / 0.12);")
tokens = tokens.replace("--mp-shadow-28: 0 14px 30px rgb(18 39 51 / 0.14);", "--mp-shadow-28: 0 20px 48px rgb(23 26 24 / 0.16);")
tokens = tokens.replace("--mp-duration-fast: 100ms;", "--mp-duration-fast: 120ms;")
tokens = tokens.replace("--mp-duration-normal: 180ms;", "--mp-duration-normal: 220ms;")
tokens = tokens.replace("--mp-duration-slow: 260ms;", "--mp-duration-slow: 320ms;")
tokens = tokens.replace("--mp-ease-standard: cubic-bezier(0.2, 0, 0, 1);", "--mp-ease-standard: cubic-bezier(0.22, 1, 0.36, 1);")
tokens = tokens.replace("--mp-ease-decelerate: cubic-bezier(0.1, 0.9, 0.2, 1);", "--mp-ease-decelerate: cubic-bezier(0.16, 1, 0.3, 1);")
organic_tokens = '''  /* Organic Workspace vocabulary. These aliases are deliberately semantic so
   * light/dark/forced-color themes can change without rewriting components. */
  --mp-ink: var(--mp-color-neutral-foreground-1);
  --mp-paper: var(--mp-color-neutral-background-1);
  --mp-sage: var(--mp-brand-background);
  --mp-sage-deep: var(--mp-brand-background-pressed);
  --mp-slate: var(--mp-secondary-background);
  --mp-brass: #9b7040;
  --mp-brass-soft: #efe4d5;
  --mp-clay: #a95d4e;
  --mp-workspace-canvas: var(--mp-color-neutral-background-canvas);
  --mp-workspace-rail: var(--mp-color-neutral-background-2);
  --mp-workspace-inspector: var(--mp-color-neutral-background-2);
  --mp-workspace-surface: var(--mp-color-neutral-background-1);
  --mp-workspace-surface-strong: var(--mp-color-neutral-background-2);
  --mp-workspace-hover: var(--mp-color-neutral-background-3);
  --mp-border-soft: var(--mp-color-neutral-stroke-2);
  --mp-focus-soft: color-mix(in srgb, var(--mp-brand-foreground) 20%, transparent);
  --mp-radius-organic-sm: 10px;
  --mp-radius-organic-md: 15px;
  --mp-radius-organic-lg: 20px;
  --mp-radius-organic-xl: 26px;
  --mp-shadow-organic-low: 0 2px 8px rgb(23 26 24 / 0.07);
  --mp-shadow-organic-medium: 0 10px 28px rgb(23 26 24 / 0.11);
  --mp-shadow-organic-high: 0 24px 64px rgb(23 26 24 / 0.18);
  --mp-ease-organic: cubic-bezier(0.22, 1, 0.36, 1);

'''
anchor = "  /* Compatibility aliases retained for the injected Thunderbird panel. */\n"
if organic_tokens not in tokens:
    if anchor not in tokens:
        raise RuntimeError("tokens.css: compatibility anchor not found")
    tokens = tokens.replace(anchor, organic_tokens + anchor, 1)
# Dark theme keeps the same semantic vocabulary but needs a non-luminous brass note.
tokens = tokens.replace("--mp-color-neutral-background-1: #292929;", "--mp-color-neutral-background-1: #1d211e;")
tokens = tokens.replace("--mp-color-neutral-background-2: #1f1f1f;", "--mp-color-neutral-background-2: #171a18;")
tokens = tokens.replace("--mp-color-neutral-background-3: #141414;", "--mp-color-neutral-background-3: #252a26;")
tokens = tokens.replace("--mp-color-neutral-background-4: #333333;", "--mp-color-neutral-background-4: #2d332e;")
tokens = tokens.replace("--mp-color-neutral-background-canvas: #111315;", "--mp-color-neutral-background-canvas: #121512;")
tokens = tokens.replace("--mp-color-neutral-card-background: #292929;", "--mp-color-neutral-card-background: #1d211e;")
tokens = tokens.replace("--mp-color-neutral-card-background-hover: #333333;", "--mp-color-neutral-card-background-hover: #252a26;")
tokens = tokens.replace("--mp-color-neutral-foreground-2: #d6d6d6;", "--mp-color-neutral-foreground-2: #d2d7d2;")
tokens = tokens.replace("--mp-color-neutral-foreground-3: #adadad;", "--mp-color-neutral-foreground-3: #a4ada6;")
tokens = tokens.replace("--mp-color-neutral-stroke-1: #525252;", "--mp-color-neutral-stroke-1: #454c46;")
tokens = tokens.replace("--mp-color-neutral-stroke-2: #3d3d3d;", "--mp-color-neutral-stroke-2: #323833;")
tokens = tokens.replace("--mp-color-neutral-stroke-accessible: #8a8a8a;", "--mp-color-neutral-stroke-accessible: #89918b;")
# Occurs once in explicit dark and once in prefers-color-scheme block.
tokens = tokens.replace("--mp-brand-background: #426f67;", "--mp-brand-background: #537b70;")
tokens = tokens.replace("--mp-brand-background-hover: #4f7f75;", "--mp-brand-background-hover: #648c80;")
tokens = tokens.replace("--mp-brand-background-pressed: #5e8f86;", "--mp-brand-background-pressed: #345a50;")
tokens = tokens.replace("--mp-brand-foreground: #9bc3bb;", "--mp-brand-foreground: #9fc4b9;")
tokens = tokens.replace("--mp-brand-foreground-hover: #b0d0c9;", "--mp-brand-foreground-hover: #b5d2ca;")
tokens = tokens.replace("--mp-brand-subtle: #203a36;", "--mp-brand-subtle: #243a34;")
tokens = tokens.replace("--mp-brand-subtle-hover: #294741;", "--mp-brand-subtle-hover: #2c4941;")
write(tokens_path, tokens)

# --- Load workspace stylesheet after legacy surface CSS so it can reshape it. ---
replace_once(
    "extension/dashboard/dashboard.html",
    '  <link rel="stylesheet" href="dashboard.css">\n',
    '  <link rel="stylesheet" href="dashboard.css">\n  <link rel="stylesheet" href="../styles/workspace.css">\n',
)
replace_once(
    "extension/options/options.html",
    '  <link rel="stylesheet" href="options.css">\n',
    '  <link rel="stylesheet" href="options.css">\n  <link rel="stylesheet" href="../styles/workspace.css">\n',
)

# --- Dashboard: physically rebuild the document into rail / canvas / inspector. ---
dashboard_path = "extension/dashboard/dashboard.js"
dashboard = read(dashboard_path)
organic_dashboard = r'''
function enhanceOrganicDashboard() {
  if (document.body.dataset.workspaceEnhanced === "true") return;
  const shell = $("dashboard-main");
  const header = shell?.querySelector(".dashboard-header");
  const tabs = shell?.querySelector(".view-tabs");
  const layout = shell?.querySelector(".dashboard-layout");
  const legacySidebar = layout?.querySelector(".dashboard-sidebar");
  const content = layout?.querySelector(".dashboard-content");
  const stats = $("stats");
  const reminders = $("reminder-center");
  const technical = shell?.querySelector(".technical-panel");
  const support = shell?.querySelector(".support-panel");
  if (!shell || !header || !tabs || !legacySidebar || !content || !stats || !reminders) {
    throw new Error("Structure Dashboard incompatible avec Organic Workspace.");
  }

  document.body.classList.add("mp-organic-workspace");
  document.body.dataset.workspaceEnhanced = "true";

  const frame = node("div", "workspace-frame");
  const rail = node("aside", "workspace-rail");
  rail.setAttribute("aria-label", msg("ariaDashboardViews", "Navigation MailPin"));
  const railBrand = node("div", "workspace-rail-brand");
  const railIcon = document.createElement("img");
  railIcon.src = "../icons/mailpin-icon.svg";
  railIcon.alt = "";
  railIcon.width = 34;
  railIcon.height = 34;
  const railBrandCopy = node("div", "workspace-rail-brand-copy");
  railBrandCopy.append(
    node("strong", "", "MailPin"),
    node("span", "", "Follow-up workspace")
  );
  railBrand.append(railIcon, railBrandCopy);
  rail.append(railBrand);

  const searchField = legacySidebar.querySelector(".search-field");
  if (searchField) rail.append(searchField);
  rail.append(tabs);
  while (legacySidebar.firstChild) rail.append(legacySidebar.firstChild);

  const stage = node("main", "workspace-stage");
  stage.append(header, stats, reminders, content);

  const inspector = node("aside", "workspace-inspector");
  inspector.setAttribute("aria-label", msg("technicalDetails", "Contexte et outils"));
  if (technical) inspector.append(technical);
  if (support) inspector.append(support);

  frame.append(rail, stage, inspector);
  shell.replaceChildren(frame);
}
'''.strip()
listener_marker = 'window.addEventListener("DOMContentLoaded", async () => {\n'
if "function enhanceOrganicDashboard()" not in dashboard:
    if listener_marker not in dashboard:
        raise RuntimeError("dashboard.js: DOMContentLoaded marker not found")
    dashboard = dashboard.replace(listener_marker, organic_dashboard + "\n\n" + listener_marker, 1)
dashboard = dashboard.replace(
    'window.addEventListener("DOMContentLoaded", async () => {\n  localize();\n',
    'window.addEventListener("DOMContentLoaded", async () => {\n  localize();\n  enhanceOrganicDashboard();\n',
    1,
)
set_view_old = 'function setView(view) {\n  const next = Object.prototype.hasOwnProperty.call(VIEW_SECTION_IDS, view) ? view : "today";\n'
set_view_new = 'function setView(view) {\n  const next = Object.prototype.hasOwnProperty.call(VIEW_SECTION_IDS, view) ? view : "today";\n  document.body.dataset.workspaceView = next;\n'
if set_view_old in dashboard:
    dashboard = dashboard.replace(set_view_old, set_view_new, 1)
write(dashboard_path, dashboard)

# --- Options: turn the settings page into a persistent editor workspace. ---
options_path = "extension/options/options.js"
options = read(options_path)
organic_options = r'''
function enhanceOrganicSettingsWorkspace() {
  if (document.body.dataset.workspaceEnhanced === "true") return;
  const app = document.querySelector(".settings-app");
  const layout = app?.querySelector(".settings-layout");
  const sidebar = layout?.querySelector(".settings-sidebar");
  const header = app?.querySelector(".page-header");
  const overview = app?.querySelector(".quick-overview");
  const loading = $("settings-loading");
  const failure = $("settings-error");
  const form = $("settings-form");
  if (!app || !layout || !sidebar || !header || !overview || !loading || !failure || !form) {
    throw new Error("Structure Options incompatible avec Organic Workspace.");
  }

  document.body.classList.add("mp-organic-settings");
  document.body.dataset.workspaceEnhanced = "true";

  const frame = node("div", "settings-organic-frame");
  const brand = node("div", "settings-organic-brand");
  const icon = document.createElement("img");
  icon.src = "../icons/mailpin-icon.svg";
  icon.alt = "";
  icon.width = 34;
  icon.height = 34;
  const brandCopy = node("div", "");
  brandCopy.append(node("strong", "", "MailPin"), node("span", "", "Workspace settings"));
  brand.append(icon, brandCopy);
  sidebar.prepend(brand);

  const stage = node("section", "settings-organic-stage");
  stage.append(header, overview, loading, failure, form);
  frame.append(sidebar, stage);
  app.replaceChildren(frame);
}
'''.strip()
options_anchor = "\n\nfunction installCriticalSettingsActions() {"
if "function enhanceOrganicSettingsWorkspace()" not in options:
    if options_anchor not in options:
        raise RuntimeError("options.js: insertion anchor not found")
    options = options.replace(options_anchor, "\n\n" + organic_options + options_anchor, 1)
call_old = "    validateSettingsControlRegistry();\n    enhanceSettingsPage();\n"
call_new = "    validateSettingsControlRegistry();\n    enhanceSettingsPage();\n    enhanceOrganicSettingsWorkspace();\n"
if call_old not in options:
    raise RuntimeError("options.js: preparation call anchor not found")
options = options.replace(call_old, call_new, 1)
write(options_path, options)

# --- Thunderbird panel: compact companion, list-first rather than card stack. ---
panel_override = r'''
/* -------------------------------------------------------------------------
 * Organic Workspace companion panel
 * ------------------------------------------------------------------------- */
#pin-mails-panel {
  margin: 6px 8px 8px;
  max-inline-size: calc(100% - 16px);
  border: 1px solid color-mix(in srgb, var(--pin-mails-border) 78%, transparent);
  border-radius: var(--mp-radius-organic-md);
  background: var(--pin-mails-panel-bg);
  box-shadow: var(--mp-shadow-organic-low);
  overflow: clip;
}

.pin-mails-panel-header {
  min-block-size: 52px;
  gap: 7px;
  padding: 8px 9px;
  border-block-end: 1px solid color-mix(in srgb, var(--pin-mails-border) 70%, transparent);
  background: color-mix(in srgb, var(--pin-mails-header-bg) 78%, var(--pin-mails-panel-bg));
}

.pin-mails-header-icon {
  inline-size: 26px;
  block-size: 26px;
}

.pin-mails-title-wrap {
  display: grid;
  grid-template-columns: auto auto;
  gap: 0 7px;
  align-items: center;
}

.pin-mails-title {
  font-family: var(--mp-font-family-display);
  font-size: max(.95rem, 12px);
  font-weight: 650;
  letter-spacing: -.025em;
}

.pin-mails-summary {
  grid-column: 1 / -1;
  overflow: hidden;
  color: var(--layout-color-2);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pin-mails-count,
.pin-mails-group-count {
  min-inline-size: 24px;
  padding: 2px 7px;
  border-radius: var(--mp-radius-round);
  background: color-mix(in srgb, var(--pin-mails-accent) 12%, transparent);
  font-variant-numeric: tabular-nums;
}

.pin-mails-collapse-button,
.pin-mails-header-action {
  inline-size: 30px;
  block-size: 30px;
  min-inline-size: 30px;
  min-block-size: 30px;
  border-radius: var(--mp-radius-organic-sm);
}

.pin-mails-header-select,
.pin-mails-smart-view-select {
  min-block-size: 30px;
  border-color: color-mix(in srgb, currentColor 14%, transparent);
  border-radius: var(--mp-radius-round);
  background: color-mix(in srgb, var(--pin-mails-panel-bg) 88%, var(--pin-mails-header-bg));
  box-shadow: none;
}

.pin-mails-panel-tools {
  display: grid;
  grid-template-columns: minmax(150px, 1fr) minmax(120px, auto) auto;
  gap: 7px;
  padding: 8px 9px;
  border-block-end: 1px solid color-mix(in srgb, var(--pin-mails-border) 60%, transparent);
  background: var(--pin-mails-panel-bg);
}

.pin-mails-search-wrap {
  min-inline-size: 0;
}

.pin-mails-search {
  inline-size: 100%;
  min-block-size: 34px;
  padding-inline: 11px;
  border: 1px solid color-mix(in srgb, currentColor 14%, transparent);
  border-radius: var(--mp-radius-organic-sm);
  background: color-mix(in srgb, var(--pin-mails-header-bg) 64%, var(--pin-mails-panel-bg));
  box-shadow: none;
}

.pin-mails-search:focus {
  border-color: var(--pin-mails-accent);
  outline: 3px solid color-mix(in srgb, var(--pin-mails-accent) 18%, transparent);
  outline-offset: 0;
}

.pin-mails-panel-list {
  padding: 4px 6px 7px;
}

.pin-mails-account-group {
  margin: 0 0 8px;
  border: 0;
  border-radius: 0;
  overflow: visible;
}

.pin-mails-account-header {
  min-block-size: 30px;
  padding: 6px 7px 5px;
  border: 0;
  background: transparent;
  color: var(--layout-color-2);
  font-size: 12px;
  font-weight: 650;
  letter-spacing: .035em;
}

.pin-mails-account-dot {
  inline-size: 7px;
  block-size: 7px;
  box-shadow: none;
}

.pin-mails-card {
  gap: 4px;
  min-block-size: var(--pin-mails-card-min-height);
  margin: 1px 0;
  padding: 9px 10px 9px 15px;
  border: 1px solid transparent;
  border-radius: var(--mp-radius-organic-sm);
  background: transparent;
  transition:
    transform var(--mp-duration-normal) var(--mp-ease-organic),
    background-color var(--mp-duration-fast) linear,
    border-color var(--mp-duration-fast) linear,
    box-shadow var(--mp-duration-normal) var(--mp-ease-organic);
}

.pin-mails-card::before {
  inset-block: 10px;
  inset-inline-start: 4px;
  inline-size: 3px;
  border-radius: var(--mp-radius-round);
  opacity: .72;
}

.pin-mails-card:hover,
.pin-mails-card:focus-within {
  border-color: color-mix(in srgb, var(--pin-account-color) 22%, transparent);
  background: color-mix(in srgb, var(--pin-account-color) 7%, var(--pin-mails-card-bg));
  box-shadow: var(--mp-shadow-organic-low);
  transform: translateY(-1px);
}

.pin-mails-card[data-active] {
  background: color-mix(in srgb, var(--pin-account-color) 6%, transparent);
}

.pin-mails-card[data-selected] {
  border-color: color-mix(in srgb, var(--pin-account-color) 48%, transparent);
  background: color-mix(in srgb, var(--pin-account-color) 10%, var(--pin-mails-card-bg));
}

.pin-mails-card-pin {
  inline-size: 30px;
  block-size: 30px;
  min-inline-size: 30px;
  min-block-size: 30px;
  border-color: transparent;
  border-radius: var(--mp-radius-organic-sm);
  background: color-mix(in srgb, var(--pin-account-color) 10%, transparent);
  box-shadow: none;
}

.pin-mails-card-pin::before {
  inline-size: 20px;
  block-size: 20px;
  -webkit-mask-size: 20px 20px;
  mask-size: 20px 20px;
  filter: none;
}

.pin-mails-note,
.pin-mails-checklist {
  border-radius: var(--mp-radius-organic-sm);
  background: color-mix(in srgb, var(--pin-mails-header-bg) 62%, transparent);
}

.pin-mails-badge,
.pin-mails-tag,
.pin-mails-chip {
  border-radius: var(--mp-radius-round);
}

.pin-mails-empty {
  min-block-size: 84px;
  margin: 4px 2px;
  border: 0;
  border-radius: var(--mp-radius-organic-md);
  background: color-mix(in srgb, var(--pin-mails-header-bg) 68%, transparent);
}

.pin-mails-reminder-center {
  gap: 5px;
  padding: 7px 8px;
  background: color-mix(in srgb, var(--mp-color-warning-background) 42%, var(--pin-mails-panel-bg));
}

.pin-mails-reminder-row {
  border-color: color-mix(in srgb, var(--mp-color-warning-foreground) 16%, var(--pin-mails-border));
  border-radius: var(--mp-radius-organic-sm);
}

@container threadPane (max-width: 560px) {
  #pin-mails-panel {
    margin-inline: 5px;
    max-inline-size: calc(100% - 10px);
  }

  .pin-mails-panel-header {
    flex-wrap: wrap;
  }

  .pin-mails-title-wrap {
    flex: 1 1 calc(100% - 76px);
  }

  .pin-mails-header-select {
    flex: 1 1 120px;
    max-inline-size: none;
  }

  .pin-mails-panel-tools {
    grid-template-columns: 1fr;
  }
}

@container threadPane (max-width: 360px) {
  .pin-mails-header-icon,
  .pin-mails-summary,
  .pin-mails-header-select[data-secondary] {
    display: none;
  }

  .pin-mails-card {
    padding-inline-end: 7px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pin-mails-card {
    transition: none;
    transform: none !important;
  }
}

@media (forced-colors: active) {
  #pin-mails-panel,
  .pin-mails-card,
  .pin-mails-search,
  .pin-mails-header-select,
  .pin-mails-smart-view-select {
    border-color: CanvasText;
    background: Canvas;
    color: CanvasText;
    box-shadow: none;
  }
}
'''
append_once("extension/styles/pin.css", "Organic Workspace companion panel", panel_override)

# --- Canonical UI spec: replace Fluent-specific design guidance. ---
ui_spec = r'''# Spécification d’interface — MailPin Organic Workspace

## Direction canonique

MailPin n’utilise plus Fluent comme direction artistique. Le produit adopte **Organic Workspace** : une interface de travail locale, calme mais vivante, qui privilégie le contenu, le contexte et les transitions plutôt que l’empilement de cartes administratives.

Références de conception : espaces de travail créatifs, interfaces command-first et outils de productivité modernes. Elles servent de principes, jamais de composants copiés. MailPin conserve sa propre identité et n’ajoute aucune dépendance UI externe.

Principes :

- **workspace avant dashboard** : navigation persistante, canvas central et contexte secondaire ;
- **contenu avant chrome** : hiérarchie par typographie, espace, proximité et mouvement plutôt que bordures systématiques ;
- **progressive disclosure** : les outils avancés apparaissent au bon moment sans masquer les capacités existantes ;
- **command-first sans command-only** : la palette accélère le clavier, toutes les actions importantes restent aussi accessibles visuellement ;
- **mouvement fonctionnel** : une transition explique un changement d’état ou de contexte ; elle ne décore jamais gratuitement ;
- **zéro effet générique** : pas de dégradé, glow, glassmorphism, blob décoratif ou animation spectaculaire de landing page ;
- **local par construction** : aucune police, icône, texture, script ou ressource distante.

## Architecture du workspace

### Dashboard

Le Dashboard est un espace de travail à trois zones lorsque la largeur le permet :

1. **rail de navigation** : recherche, vues principales, vues intelligentes et vues enregistrées ;
2. **canvas** : contexte courant, métriques utiles, focus et contenu actionnable ;
3. **inspector** : diagnostic, activité et informations secondaires qui ne doivent pas concurrencer la tâche principale.

Sous 1260 px, l’inspector sort de la colonne et rejoint le flux. Sous 920 px, le rail devient une barre de workspace compacte. Aucun contenu essentiel ne doit devenir inaccessible.

Les vues Aujourd’hui, Liste, Kanban, Affaires, Revue, Historique et Santé conservent leur contrat métier et leurs raccourcis. La vue active doit être identifiable sans dépendre de la couleur seule.

### Panneau Thunderbird

Le panneau est un **compagnon compact** : voir → agir → repartir. Il ne doit pas reproduire le Dashboard en miniature.

- panneau au-dessus de la liste native, repliable et à défilement interne ;
- en-tête court avec portée, tri et actions réellement utiles ;
- recherche et vue intelligente immédiatement disponibles lorsque activées ;
- cartes traitées comme des lignes éditoriales, avec un repère de compte et peu de chrome ;
- détails secondaires révélés sans augmenter inutilement la hauteur de toutes les cartes ;
- container queries obligatoires pour les largeurs réellement imposées par le splitter Thunderbird ;
- aucune modification de la hauteur virtuelle ou de la géométrie de la liste native.

### Options

Options est un **éditeur de réglages**, pas un tableau de bord.

- rail persistant avec recherche et navigation ;
- scène de contenu centrale avec sections éditoriales ;
- familles fonctionnelles stables tant qu’aucun besoin produit ne justifie leur migration ;
- contrôles existants et registre `SETTINGS_CONTROL_DEFINITIONS` préservés ;
- mode Recommandé = réduction de charge cognitive, jamais sauvegarde implicite ;
- un seul dock Enregistrer/Annuler, visible uniquement lorsqu’un brouillon diffère de l’état persisté ;
- résultat d’une action affiché à proximité et via toast non bloquant.

## Typographie

Aucune police distante. MailPin utilise des familles locales privilégiant les variantes système à métriques modernes :

- display : `Segoe UI Variable Display`, `Aptos Display`, puis système ;
- texte : `Segoe UI Variable Text`, `Aptos`, puis système ;
- mono : `Cascadia Code`, `SFMono-Regular`, `Consolas`, puis mono système.

La hiérarchie utilise davantage l’échelle, la graisse et l’espace que les encadrements. Aucun texte explicite ne descend sous 12 px.

## Couleur

La base reste chaude et naturelle : Ink, Paper, Sage, Slate et Brass. Les valeurs runtime vivent dans `extension/styles/tokens.css`.

- Sage = progression/action ;
- Slate = information structurelle ;
- Brass = attention contextuelle ;
- états succès/alerte/danger restent sémantiques et ne sont jamais remplacés uniquement par la marque ;
- les thèmes clair, sombre et couleurs forcées doivent garder la même hiérarchie d’information.

Les dégradés et halos sont exclus du système produit.

## Géométrie et profondeur

- rayons plus organiques sur les surfaces interactives, pas sur chaque séparation ;
- bordures faibles et rares ;
- ombres uniquement pour une surface réellement détachée : dialog, dock, élément temporairement élevé ;
- une liste de mails ne devient pas une grille de cartes sans raison fonctionnelle ;
- l’alignement peut être asymétrique si la lecture et l’ordre clavier restent évidents.

## Motion

Durées de référence :

- hover/feedback : 100–140 ms ;
- changement d’état : 180–240 ms ;
- déplacement ou changement de contexte : 240–320 ms.

Utiliser une courbe organique de décélération. `prefers-reduced-motion` et le réglage MailPin de réduction du mouvement désactivent les déplacements non indispensables.

Une animation ne doit jamais retarder une action, bloquer le clavier ou masquer l’état final.

## Accessibilité et ergonomie

- clavier complet sur Dashboard, Options et panneau ;
- focus visible, ordre de tabulation cohérent et `aria-current` / `aria-pressed` selon le rôle ;
- zoom 200 % sans perte de fonctionnalité ;
- thèmes clair/sombre, contraste élevé et `forced-colors` ;
- cibles d’action suffisamment grandes sans gonfler toute l’interface ;
- aucun état uniquement communiqué par couleur ;
- scroll interne seulement lorsqu’il préserve le contexte ; éviter les scrolls imbriqués inutiles ;
- erreurs réessayables et états de chargement explicites.

## Invariants Thunderbird

- ne jamais modifier un compteur natif ou l’état lu/non-lu lors d’un simple épinglage ;
- clic carte = afficher le message sans faire défiler artificiellement la liste native ; double-clic = comportement natif prévu ;
- menu contextuel Thunderbird natif et focus restauré après fermeture ;
- étoile native intacte en mode indépendant ; transformation réversible en mode `nativeStar` ;
- aucune modification de l’intégration `PinCompatibility` pour un besoin uniquement visuel.

## Sécurité de l’interface

- aucune autorisation ou rôle simulé dans le DOM ;
- aucune entrée de formulaire considérée fiable avant validation privilégiée ;
- aucun `innerHTML` ou HTML construit avec des métadonnées mail ;
- import en aperçu sûr et automatismes neutralisés ;
- sélecteur natif obligatoire pour tout chemin local ;
- les confirmations UX complètent les contrôles privilégiés mais ne sont jamais la barrière unique.

## Critère de validation visuelle

Une refonte n’est pas considérée validée parce que ses tests statiques passent. Toute affirmation concernant géométrie, responsive, focus, thème ou mouvement dans Thunderbird exige une observation sur le vrai runtime lorsque la surface concernée y est rendue.
'''
write("docs/UI_SPEC.md", ui_spec)

# --- Brand doc: align visual language and repository slug. ---
branding = read("BRANDING.md")
branding = branding.replace(
    "- **Dépôt :** `ussmarines/mailperch-thunderbird` (slug GitHub historique conservé tant qu’il n’est pas renommé dans les paramètres du dépôt)",
    "- **Dépôt :** `ussmarines/mailpin-thunderbird`"
)
branding = branding.replace(
    "La direction artistique est volontairement éditoriale et sobre : pas de dégradés, pas d’effets de verre, pas de glow, pas de texture générative. L’interface conserve la géométrie Thunderbird et utilise la marque comme système de hiérarchie, pas comme décoration.",
    "La direction produit **Organic Workspace** est éditoriale, spatiale et command-first : rail de navigation, canvas de travail, contexte secondaire et micro-interactions fonctionnelles. Elle ne reprend plus Fluent comme langage visuel. Pas de dégradés, verre, glow ou texture générative ; la marque sert la hiérarchie plutôt que la décoration."
)
branding = branding.replace(
    "- **Ink Charcoal** `#1A1D21` — texte et structure.\n- **Slate Blue** `#3D536B` — information secondaire et intégration Thunderbird.\n- **Sage Teal** `#4F7F75` — action principale ; contraste AA avec texte blanc.\n- **Sage Teal Dark** `#426F67` — hover/pressed et surfaces sombres.\n- **Brass** `#C79A3A` — accent ponctuel pour rappel/attention, jamais texte blanc.\n- **Warm Off-White** `#F7F5F0` — canvas clair.",
    "- **Ink** `#171A18` — texte, commandes structurantes et contraste.\n- **Slate** `#46575D` — information secondaire et structure.\n- **Sage** `#4E7569` — progression et action.\n- **Sage Deep** `#2D5148` — action forte / état pressé.\n- **Brass** `#9B7040` — accent ponctuel de contexte.\n- **Warm Paper** `#F4F1E9` — canvas clair."
)
branding = branding.replace(
    "Pile locale uniquement : `system-ui`, `Segoe UI Variable`, `Aptos`, `Segoe UI`, sans-serif. Aucune police distante, CDN ou dépendance ajoutée.",
    "Pile locale uniquement : `Segoe UI Variable Display` / `Aptos Display` pour les titres, `Segoe UI Variable Text` / `Aptos` pour le texte et repli système ; `Cascadia Code` / `Consolas` pour le mono. Aucune police distante, CDN ou dépendance ajoutée."
)
write("BRANDING.md", branding)

# --- Options-local rule file: retire Fluent-era assumptions without weakening form invariants. ---
options_agents_path = "extension/options/AGENTS.md"
options_agents = read(options_agents_path)
options_agents = options_agents.replace(
    "La page Options contient beaucoup de réglages historiques. L’objectif actuel n’est pas d’en supprimer, mais de réduire la charge cognitive sans casser les profils existants.",
    "La page Options contient beaucoup de réglages historiques. Organic Workspace la traite comme un éditeur : réduire la charge cognitive, révéler progressivement le contexte et conserver tous les contrôles/persistences utiles sans reproduire un dashboard administratif."
)
options_agents = options_agents.replace(
    "Ne pas créer une nouvelle famille sans besoin produit explicite. Les réglages techniques peuvent rester dans le DOM pour le mode Avancé, mais doivent être retirés de la navigation/recherche et masqués lorsqu’ils sont marqués avancés en mode Recommandé.",
    "Les quatre familles restent une taxonomie fonctionnelle, pas une contrainte de composition visuelle. Le rail, la scène, la recherche et les transitions peuvent être refondus librement tant que chaque contrôle reste atteignable. Les réglages techniques peuvent rester dans le DOM pour le mode Avancé, mais doivent être retirés de la navigation/recherche et masqués lorsqu’ils sont marqués avancés en mode Recommandé."
)
write(options_agents_path, options_agents)

# --- Differential guard for the new design contract. ---
organic_test = r'''from pathlib import Path

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
'''
write("tests/test_organic_workspace_ui.py", organic_test)

print("Organic Workspace transformation applied.")
