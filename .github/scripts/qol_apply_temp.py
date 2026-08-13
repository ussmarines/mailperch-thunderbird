from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PALETTE = [
    "#4e7569",  # sage
    "#a14f68",  # berry
    "#718547",  # moss
    "#59558f",  # indigo
    "#9b7040",  # brass
    "#47758e",  # ocean
    "#a95d4e",  # clay
    "#875476",  # plum
]

LEGACY = [
    "#0f6cbd", "#5c2d91", "#107c10", "#c239b3", "#d83b01",
    "#038387", "#8e562e", "#8764b8", "#0078d4", "#ca5010",
]


def replace(path, old, new, count=1):
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual < count:
        raise SystemExit(f"anchor missing in {path}: expected >= {count}, got {actual}: {old[:120]!r}")
    text = text.replace(old, new, count)
    file.write_text(text, encoding="utf-8", newline="\n")


def append_once(path, marker, block):
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    if marker in text:
        return
    file.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8", newline="\n")


# --- Runtime / Thunderbird panel palette -----------------------------------
impl_palette_old = '''const DEFAULT_COLORS = [
  "#0f6cbd",
  "#5c2d91",
  "#107c10",
  "#c239b3",
  "#d83b01",
  "#038387",
  "#8e562e",
  "#8764b8",
  "#0078d4",
  "#ca5010"
];'''
impl_palette_new = '''const DEFAULT_COLORS = Object.freeze([
  "#4e7569", // sage
  "#a14f68", // berry
  "#718547", // moss
  "#59558f", // indigo
  "#9b7040", // brass
  "#47758e", // ocean
  "#a95d4e", // clay
  "#875476"  // plum
]);

// Pre-Organic Workspace defaults were generated automatically from the
// account key and were then persisted by the Options form. Treat only that
// exact generated value as a legacy default; arbitrary/custom colours stay
// untouched.
const LEGACY_DEFAULT_COLORS = Object.freeze([
  "#0f6cbd", "#5c2d91", "#107c10", "#c239b3", "#d83b01",
  "#038387", "#8e562e", "#8764b8", "#0078d4", "#ca5010"
]);

function nextDefaultColor(items = [], startIndex = 0) {
  const usage = new Map(DEFAULT_COLORS.map(color => [color, 0]));
  for (const item of Array.isArray(items) ? items : []) {
    const color = String(item?.color || "").toLowerCase();
    if (usage.has(color)) usage.set(color, usage.get(color) + 1);
  }
  const minimum = Math.min(...usage.values());
  const start = Math.max(0, Number(startIndex) || 0) % DEFAULT_COLORS.length;
  for (let offset = 0; offset < DEFAULT_COLORS.length; offset += 1) {
    const color = DEFAULT_COLORS[(start + offset) % DEFAULT_COLORS.length];
    if (usage.get(color) === minimum) return color;
  }
  return DEFAULT_COLORS[start];
}'''
replace("extension/api/pinInbox/implementation.js", impl_palette_old, impl_palette_new)

replace(
    "extension/api/pinInbox/implementation.js",
    'function getDefaultColor(accountKey) {\n  return DEFAULT_COLORS[hashString(accountKey) % DEFAULT_COLORS.length];\n}',
    '''function getDefaultColor(accountKey) {
  return DEFAULT_COLORS[hashString(accountKey) % DEFAULT_COLORS.length];
}

function getLegacyDefaultColor(accountKey) {
  return LEGACY_DEFAULT_COLORS[hashString(accountKey) % LEGACY_DEFAULT_COLORS.length];
}'''
)

replace(
    "extension/api/pinInbox/implementation.js",
    '  _getAccountColor(accountKey) {\n    return this._settings.accountColors[accountKey] || getDefaultColor(accountKey);\n  }',
    '''  _getAccountColor(accountKey) {
    const stored = String(this._settings.accountColors[accountKey] || "").toLowerCase();
    if (!stored || stored === getLegacyDefaultColor(accountKey)) return getDefaultColor(accountKey);
    return stored;
  }'''
)

replace(
    "extension/api/pinInbox/implementation.js",
    '  const color = COLOR_RE.test(String(value.color || "")) ? String(value.color).toLowerCase() : "#6264a7";',
    '  const color = COLOR_RE.test(String(value.color || "")) ? String(value.color).toLowerCase() : DEFAULT_COLORS[fallbackIndex % DEFAULT_COLORS.length];'
)
replace(
    "extension/api/pinInbox/implementation.js",
    '    color: COLOR_RE.test(String(value.color || "")) ? String(value.color).toLowerCase() : "#0f6cbd",',
    '    color: COLOR_RE.test(String(value.color || "")) ? String(value.color).toLowerCase() : DEFAULT_COLORS[fallbackIndex % DEFAULT_COLORS.length],'
)

replace(
    "extension/api/pinInbox/implementation.js",
    '    const item = normalizeCase({...details, id: details.id || uniqueEntityId("case", values)}, values.length);',
    '''    const requestedColor = COLOR_RE.test(String(details.color || ""))
      ? String(details.color).toLowerCase()
      : nextDefaultColor([...(this._data.groups || []), ...values]);
    const item = normalizeCase({...details, color: requestedColor, id: details.id || uniqueEntityId("case", values)}, values.length);'''
)

replace(
    "extension/api/pinInbox/implementation.js",
    '        this._data.groups.push({id, name: label.slice(0, 80), color: COLOR_RE.test(color.value) ? color.value : "#6264a7"});',
    '        this._data.groups.push({id, name: label.slice(0, 80), color: COLOR_RE.test(color.value) ? color.value : nextDefaultColor(this._data.groups)});'
)
replace(
    "extension/api/pinInbox/implementation.js",
    '      color.value = DEFAULT_COLORS[this._data.groups.length % DEFAULT_COLORS.length];',
    '      color.value = nextDefaultColor(this._data.groups);'
)

# Replace only the neutral account-colour fallback sites, not semantic smart
# section colours or tag-sync definitions.
replace(
    "extension/api/pinInbox/implementation.js",
    '      const color = this._settings.showAccountColor\n        ? this._getAccountColor(ref.accountKey)\n        : "#0f6cbd";',
    '      const color = this._settings.showAccountColor\n        ? this._getAccountColor(ref.accountKey)\n        : DEFAULT_COLORS[0];'
)
replace(
    "extension/api/pinInbox/implementation.js",
    '          this._settings.showAccountColor ? this._getAccountColor(key) : "#0f6cbd",',
    '          this._settings.showAccountColor ? this._getAccountColor(key) : DEFAULT_COLORS[0],'
)

# --- Options QoL ------------------------------------------------------------
options_anchor = '''const INITIALIZATION_TIMEOUTS = Object.freeze({
  apiNamespace: 2_000,
  configuration: 10_000,
  shortcut: 5_000,
  calendar: 7_000,
  auxiliary: 7_000
});'''
options_insert = options_anchor + '''
const ENTITY_DEFAULT_COLORS = Object.freeze([
  "#4e7569", "#a14f68", "#718547", "#59558f",
  "#9b7040", "#47758e", "#a95d4e", "#875476"
]);

function nextEntityColor(items = [], startIndex = 0) {
  const usage = new Map(ENTITY_DEFAULT_COLORS.map(color => [color, 0]));
  for (const item of Array.isArray(items) ? items : []) {
    const color = String(item?.color || "").toLowerCase();
    if (usage.has(color)) usage.set(color, usage.get(color) + 1);
  }
  const minimum = Math.min(...usage.values());
  const start = Math.max(0, Number(startIndex) || 0) % ENTITY_DEFAULT_COLORS.length;
  for (let offset = 0; offset < ENTITY_DEFAULT_COLORS.length; offset += 1) {
    const color = ENTITY_DEFAULT_COLORS[(start + offset) % ENTITY_DEFAULT_COLORS.length];
    if (usage.get(color) === minimum) return color;
  }
  return ENTITY_DEFAULT_COLORS[start];
}

function focusCreatedEntity(hostId, selector = "input:not([type='color'])") {
  requestAnimationFrame(() => {
    const host = $(hostId);
    const card = host?.lastElementChild;
    if (!card) return;
    card.scrollIntoView({block: "nearest", behavior: "smooth"});
    const control = card.querySelector(selector);
    control?.focus({preventScroll: true});
    if (control instanceof HTMLInputElement && ["text", "search", "url", "email", "tel"].includes(control.type)) {
      control.select();
    }
  });
}'''
replace("extension/options/options.js", options_anchor, options_insert)

replace(
    "extension/options/options.js",
    '  control.required = true;\n  return {control, compatible};',
    '  return {control, compatible};'
)
replace(
    "extension/options/options.js",
    '    const due=document.createElement("input");due.type="datetime-local";due.required=true;due.value=item.dueAt?new Date(item.dueAt-new Date().getTimezoneOffset()*60000).toISOString().slice(0,16):"";',
    '    const due=document.createElement("input");due.type="datetime-local";due.value=item.dueAt?new Date(item.dueAt-new Date().getTimezoneOffset()*60000).toISOString().slice(0,16):"";'
)

replace(
    "extension/options/options.js",
    '    color.dataset.settingMigration = PinSettings.MIGRATION_STRATEGY;\n    color.addEventListener("input", () => card.style.setProperty("--account-color", color.value));',
    '''    color.dataset.settingMigration = PinSettings.MIGRATION_STRATEGY;
    color.setAttribute("aria-label", `${msg("dynamicColor")} · ${primaryLabel}`);
    color.title = `${msg("dynamicColor")} · ${primaryLabel}`;
    color.addEventListener("input", () => card.style.setProperty("--account-color", color.value));'''
)
replace(
    "extension/options/options.js",
    '    reset.type = "button";\n    reset.addEventListener("click", () => {',
    '''    reset.type = "button";
    reset.setAttribute("aria-label", `${msg("defaultButton")} · ${primaryLabel}`);
    reset.title = `${msg("defaultButton")} · ${primaryLabel}`;
    reset.addEventListener("click", () => {'''
)

replace(
    "extension/options/options.js",
    '''      name: msg("dynamicNewGroup"),
      color: "#6264a7"
    });
    renderGroups();
    renderRules();
    renderTemplates();
    syncDirtyState();''',
    '''      name: msg("dynamicNewGroup"),
      color: nextEntityColor([...groups, ...cases])
    });
    renderGroups();
    renderRules();
    renderTemplates();
    syncDirtyState();
    focusCreatedEntity("groups-list");'''
)
replace(
    "extension/options/options.js",
    '''      name: msg("dynamicNewCase"),
      color: "#0f6cbd",
      status: "active",
      createdAt: Date.now(),
      updatedAt: Date.now()
    });
    renderCases();
    renderRules();
    renderTemplates();
    syncDirtyState();''',
    '''      name: msg("dynamicNewCase"),
      color: nextEntityColor([...groups, ...cases]),
      status: "active",
      createdAt: Date.now(),
      updatedAt: Date.now()
    });
    renderCases();
    renderRules();
    renderTemplates();
    syncDirtyState();
    focusCreatedEntity("cases-list");'''
)
replace(
    "extension/options/options.js",
    '''    renderTemplates();
    renderRules();
    syncDirtyState();
  });

  $("add-rule")''',
    '''    renderTemplates();
    renderRules();
    syncDirtyState();
    focusCreatedEntity("templates-list");
  });

  $("add-rule")'''
)
replace(
    "extension/options/options.js",
    '''    renderRules();
    syncDirtyState();
  });

  $("simulate-rules")''',
    '''    renderRules();
    syncDirtyState();
    focusCreatedEntity("rules-list");
  });

  $("simulate-rules")'''
)

# --- Permanent UX specification --------------------------------------------
spec_marker = "## 11. Quality of Life et valeurs par défaut"
spec_block = '''
## 11. Quality of Life et valeurs par défaut

- Les couleurs générées automatiquement utilisent la palette d’accents MailPin : Sage, Berry, Moss, Indigo, Brass, Ocean, Clay et Plum. Elles doivent être nettement différenciables tout en restant cohérentes avec Organic Workspace.
- Les couleurs personnalisées choisies par l’utilisateur sont conservées. Seules les anciennes couleurs générées automatiquement par MailPin peuvent être remappées vers la palette courante.
- Lorsqu’un groupe, une affaire ou toute autre entité colorable est créée, MailPin propose la couleur la moins utilisée de la palette avant de recommencer un cycle.
- Une création place immédiatement le focus sur son champ de nom et sélectionne le libellé par défaut pour permettre la saisie sans clic supplémentaire.
- Un champ optionnel ne devient obligatoire qu’au moment de l’action qui en dépend. En particulier, une affaire peut exister sans échéance ni calendrier ; Agenda valide ces données uniquement lors de la création/synchronisation d’un élément.
- Les contrôles de couleur et de remise à la valeur par défaut doivent exposer un nom accessible contextualisé par l’entité concernée.
- Les états `dirty`, le raccourci Ctrl/Cmd+S, l’avertissement de fermeture avec modifications non enregistrées, les états busy et les confirmations destructives existantes restent les mécanismes de référence et ne doivent pas être dupliqués par des dialogues supplémentaires sans besoin prouvé.
'''
append_once("docs/UI_SPEC.md", spec_marker, spec_block)

# --- Regression contract ----------------------------------------------------
test_block = r'''
def test_qol_palette_defaults_and_low_friction_creation_contract():
    import re

    implementation = text("extension/api/pinInbox/implementation.js")
    options_js = text("extension/options/options.js")
    spec = text("docs/UI_SPEC.md")

    def palette(source, name):
        match = re.search(rf"const {name} = Object\.freeze\(\[(.*?)\]\);", source, re.S)
        assert match, name
        return re.findall(r"#[0-9a-fA-F]{6}", match.group(1))

    runtime_palette = [value.lower() for value in palette(implementation, "DEFAULT_COLORS")]
    options_palette = [value.lower() for value in palette(options_js, "ENTITY_DEFAULT_COLORS")]
    assert runtime_palette == options_palette
    assert len(runtime_palette) == 8
    assert len(set(runtime_palette)) == len(runtime_palette)
    assert runtime_palette[0] == "#4e7569"
    assert "#0f6cbd" not in runtime_palette
    assert "#6264a7" not in runtime_palette

    assert "function nextDefaultColor(items = [], startIndex = 0)" in implementation
    assert "stored === getLegacyDefaultColor(accountKey)" in implementation
    assert "nextDefaultColor(this._data.groups)" in implementation
    assert "nextDefaultColor([...(this._data.groups || []), ...values])" in implementation
    assert "function nextEntityColor(items = [], startIndex = 0)" in options_js
    assert 'color: nextEntityColor([...groups, ...cases])' in options_js
    assert 'focusCreatedEntity("groups-list")' in options_js
    assert 'focusCreatedEntity("cases-list")' in options_js
    assert 'focusCreatedEntity("templates-list")' in options_js
    assert 'focusCreatedEntity("rules-list")' in options_js

    # Deadline and calendar are optional until the Agenda action itself
    # validates the values it needs.
    assert 'control.required = true' not in options_js
    assert 'due.type="datetime-local";due.required=true' not in options_js
    assert 'if (!item.dueAt) throw new Error(msg("dynamicCalendarDueRequired"));' in options_js
    assert 'if (!calendar.value) {' in options_js

    assert 'color.setAttribute("aria-label", `${msg("dynamicColor")} · ${primaryLabel}`)' in options_js
    assert "Quality of Life et valeurs par défaut" in spec
'''
append_once("tests/test_organic_workspace_ui.py", "test_qol_palette_defaults_and_low_friction_creation_contract", test_block)

print("QoL patch applied")
