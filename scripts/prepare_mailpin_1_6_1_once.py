#!/usr/bin/env python3
"""Prepare MailPin 1.6.1 as the truthful ATN/reviewer metadata candidate.

No business/runtime logic is changed. The only XPI runtime delta is manifest version 1.6.1.
This file removes itself after applying the one-shot transformation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "1.6.0"
VERSION = "1.6.1"
RUNTIME_SHA = "4fdb978e1828325001f95951c115059a931b8b6e"
BASELINE_SHA = "6d582da0cf729b1a93df348e4845430fbfb7fad2"
XPI_160_SHA = "6860e0177795b163cb672edd1a93897260785c4b8eeeeac71d1b3d32dca281ae"
ID = "ussmarines.mailpin@addons.thunderbird.net"


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


# Canonical package/manifest version. No other manifest field is changed.
package_path = ROOT / "package.json"
package = json.loads(package_path.read_text(encoding="utf-8"))
assert package["version"] == OLD
package["version"] = VERSION
write(package_path, json.dumps(package, ensure_ascii=False, indent=2))

manifest_path = ROOT / "extension/manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
assert manifest["version"] == OLD
assert manifest["browser_specific_settings"]["gecko"]["id"] == ID
assert manifest["permissions"] == ["menus"]
manifest["version"] = VERSION
write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2))

# README current-version markers only. Keep the historical statement that 1.6.0 introduced the brand/ID.
for rel in ("README.md", "README.en.md"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace("release-v1.6.0", "release-v1.6.1")
    text = text.replace("MailPin_v1.6.0.xpi", "MailPin_v1.6.1.xpi")
    text = text.replace("MailPin_GitHub_Repository_v1.6.0.zip", "MailPin_GitHub_Repository_v1.6.1.zip")
    text = text.replace("release `v1.6.0`", "release `v1.6.1`")
    text = text.replace("**MailPin :** `1.6.0`", "**MailPin :** `1.6.1`")
    text = text.replace("**MailPin:** `1.6.0`", "**MailPin:** `1.6.1`")
    write(path, text)

# Changelog: 1.6.1 is deliberately documentation/store truth + version bump only.
changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
if not re.search(r"^## 1\.6\.1\b", changelog, flags=re.M):
    entry = """## 1.6.1 — métadonnées de publication et dossier ATN fiabilisés

- corrige les documents actifs de publication/review qui avaient conservé des preuves 1.5.4 sous des libellés 1.6.0 après le rebranding ;
- distingue explicitement la recette manuelle pré-rebranding 1.5.4 des validations fraîches MailPin 1.6.0/1.6.1 ;
- synchronise `PROJECT_MEMORY.md`, `docs/PROJECT_STATE.json`, `STORE_RELEASE.md`, la checklist ATN, le handoff et les instructions reviewers sur les vrais commits/runs MailPin ;
- conserve l’identité publique définitive `ussmarines.mailpin@addons.thunderbird.net` et documente que la migration d’ID a été introduite volontairement en 1.6.0 ;
- passe la version distribuée à 1.6.1 afin que l’archive source remise aux reviewers contienne des métadonnées exactes ;
- aucune modification de logique métier, permission, schéma, dépendance runtime, réseau, télémétrie ou code distant ; seul le champ `version` du manifeste change dans le XPI.

"""
    changelog = changelog.replace("# Journal des modifications\n\n", "# Journal des modifications\n\n" + entry, 1)
write(changelog_path, changelog)

# Simple current-release markers whose content remains otherwise valid.
replacements = {
    "THIRD_PARTY_NOTICES.md": [("MailPin 1.6.0", "MailPin 1.6.1")],
    "PRIVACY.md": [("MailPin 1.6.0 ne contient", "MailPin 1.6.1 ne contient"), ("MailPin 1.6.0 contains", "MailPin 1.6.1 contains")],
    "SECURITY.md": [("SECURITY_AUDIT_1.6.0.md", "SECURITY_AUDIT_1.6.1.md")],
    "docs/BUG_TRACKER.md": [("Version publique : **1.6.0**", "Version publique : **1.6.1**")],
    "release/ATN_REVIEW_NOTES_TEMPLATE.md": [("— MailPin 1.6.0", "— MailPin 1.6.1"), ("Version :** 1.6.0", "Version :** 1.6.1")],
    "release/BUILD_INSTRUCTIONS.md": [("build 1.6.0", "build 1.6.1"), ("MailPin_v1.6.0.xpi", "MailPin_v1.6.1.xpi"), ("MailPin_GitHub_Repository_v1.6.0.zip", "MailPin_GitHub_Repository_v1.6.1.zip")],
    "release/manifest-store-template.json": [("publication 1.6.0", "publication 1.6.1")],
}
for rel, pairs in replacements.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = text.replace(old, new)
    write(path, text)

# Known limitations: correct the mechanically overstated 1.6.0 wording.
known_path = ROOT / "docs/KNOWN_LIMITATIONS.md"
known = known_path.read_text(encoding="utf-8")
known = re.sub(
    r"## Version 1\.6\.0 et portée de validation\n\n.*?\n\nUne matrice exhaustive",
    "## Version 1.6.1 et portée de validation\n\n"
    "MailPin **1.6.1** ne change pas la logique métier de 1.6.0 : le delta distribué est le champ `version` du manifeste et les métadonnées/documentations de publication. "
    "Le rebranding MailPin, la nouvelle identité ATN, l’icône SVG et la palette ont été introduits en 1.6.0 et ont passé QA Linux/Windows, garde sécurité et smoke Thunderbird 153 réel sur le runtime intégré. "
    "La recette manuelle utilisateur reste une preuve héritée de la dernière build pré-rebranding 1.5.4 pour les comportements métier inchangés ; elle n’est pas présentée comme une recette manuelle fraîche du XPI 1.6.1. "
    "Les validations automatisées fraîches de 1.6.1 sont consignées dans `VALIDATION_REPORT_1.6.1.md`.\n\nUne matrice exhaustive",
    known,
    flags=re.S,
)
known = known.replace("Le manifeste 1.6.0 déclare", "Le manifeste 1.6.1 déclare")
write(known_path, known)

# Manual plan: exact 1.6.1 XPI remains a manual acceptance item, without pretending prior manual work was fresh.
manual_path = ROOT / "docs/MANUAL_TEST_PLAN.md"
manual = manual_path.read_text(encoding="utf-8")
manual = manual.replace("# Plan de test manuel MailPin — 1.6.0", "# Plan de test manuel MailPin — 1.6.1")
manual = manual.replace(
    "Le présent plan complète les validations automatisées du candidat local 1.6.0. Les preuves historiques restent utiles uniquement pour les surfaces inchangées ; toute zone runtime modifiée doit disposer d’une preuve fraîche avant publication.",
    "Le présent plan complète les validations automatisées du candidat 1.6.1. La logique métier est inchangée depuis le runtime MailPin 1.6.0 ; la recette utilisateur pré-rebranding 1.5.4 reste une preuve héritée uniquement pour ces comportements inchangés. Le XPI 1.6.1 doit néanmoins recevoir son propre smoke automatisé avant publication et peut recevoir une recette humaine ciblée avant soumission ATN."
)
manual = manual.replace("## Priorité 1.6.0 — recette des constats utilisateurs", "## Priorité 1.6.1 — recette ciblée avant ATN")
manual = manual.replace(
    "La readiness reste **NO-GO** tant que ces scénarios n’ont pas été observés sur le XPI 1.6.0 exact fourni pour retest.",
    "Pour GitHub, le GO 1.6.1 dépend des QA Linux/Windows, de la garde sécurité, du build reproductible et du smoke Thunderbird réel. Pour ATN, une recette humaine ciblée du XPI 1.6.1 reste recommandée et doit être consignée sans réattribuer les tests 1.5.4 à cette version."
)
write(manual_path, manual)

# Store/reviewer truth. Wording stays valid after the release is published.
store = f"""# Publication MailPin 1.6.1

## Identité

- **Nom :** MailPin
- **Nom complet :** MailPin — Email Follow-up & Productivity for Thunderbird
- **Version publique :** 1.6.1
- **Sous-titre FR :** Suivi d’e-mails & productivité pour Thunderbird.
- **Subtitle EN:** Email Follow-up & Productivity for Thunderbird
- **Auteur public :** ussmarines
- **Identifiant permanent :** `{ID}`
- **Compatibilité déclarée :** Thunderbird 153.0 à 153.*
- **Licence :** MailPin Source-Available License 1.1

L’identifiant a été adopté volontairement en 1.6.0 avant la première publication ATN. Il doit conserver exactement la même casse et ne plus être modifié après publication ATN.

## Pourquoi 1.6.1

La 1.6.0 a réalisé le rebranding **MailPerch → MailPin**, l’adoption de l’ID public définitif et la nouvelle direction artistique. Son runtime intégré par la PR #35 (`{RUNTIME_SHA}`) a passé QA Linux/Windows, garde sécurité et smoke Thunderbird 153 réel. La release GitHub v1.6.0 a ensuite été publiée depuis `main`.

Un contrôle reviewer post-publication a détecté que certains documents actifs de l’archive source 1.6.0 contenaient encore des preuves textuelles héritées de la préparation 1.5.4 (ancien numéro de PR/SHA, ancien hash XPI et une phrase niant à tort le changement d’identité). **Aucun défaut runtime n’a été trouvé.**

La 1.6.1 corrige uniquement cette cohérence de publication et le numéro de version. Aucun comportement métier, permission, schéma, stockage, dépendance runtime, réseau, télémétrie, publicité ou code distant n’est modifié.

## Preuves correctement attribuées

- recette manuelle utilisateur : dernière preuve fraîche sur le candidat pré-rebranding 1.5.4 ; réutilisable uniquement pour les comportements métier inchangés ;
- rebranding/runtime MailPin 1.6.0 : PR #35 puis commit `{RUNTIME_SHA}`, QA Linux/Windows + garde sécurité + smoke Thunderbird réel verts ;
- release 1.6.0 : XPI publié SHA-256 `{XPI_160_SHA}` ;
- 1.6.1 : la PR et la release doivent refaire la QA complète et le smoke Thunderbird car le manifeste/version est modifié ; les résultats publiés par GitHub Actions et `SHA256SUMS.txt` constituent la preuve fraîche de cette version.

Aucune recette manuelle fraîche du XPI 1.6.1 n’est revendiquée tant qu’elle n’a pas été réellement effectuée.

## Livrables GitHub / ATN

Le workflow Release publie, après `npm run ci` :

- `dist/MailPin_v1.6.1.xpi` — extension ;
- `dist/MailPin_GitHub_Repository_v1.6.1.zip` — sources complètes pour review ;
- `dist/SHA256SUMS.txt` — empreintes définitives ;
- `release/ATN_REVIEW_NOTES_TEMPLATE.md` — informations reviewers ;
- `release/BUILD_INSTRUCTIONS.md` — reproduction du build.

Pour une soumission ATN, **les sommes du `SHA256SUMS.txt` attaché à la release v1.6.1 sont la référence définitive** ; aucun ancien hash 1.5.x/1.6.0 ne doit être recopié dans le dossier reviewer.

## Informations de fiche ATN

### Description courte FR

Épinglez, organisez et suivez vos e-mails importants dans Thunderbird avec portée par comptes, notes, sous-tâches, rappels, vues, Agenda et tableau de bord local.

### Short description EN

Pin, organize, and follow up on important email in Thunderbird with account scoping, notes, subtasks, reminders, saved views, Calendar integration, and a local dashboard.

### Confidentialité

MailPin ne transmet aucune donnée. Aucun corps complet de message ni contenu de pièce jointe n’est copié dans sa base. Voir `PRIVACY.md`.

### Permission privilégiée

L’API Experiment `pinInbox` est nécessaire pour intégrer le panneau dans `about:3pane`, résoudre les messages déplacés, utiliser SQLite, écouter les changements de dossiers, gérer les tags MailPin et créer/synchroniser les tâches ou événements Agenda compatibles. Cette API explique l’avertissement d’accès complet affiché par Thunderbird.

## Limites restant externes à GitHub

- recette humaine ciblée du XPI 1.6.1 avant ATN ;
- matrice Windows/Linux/macOS Thunderbird réelle exhaustive ;
- Gmail/Microsoft/IMAP et calendriers réseau réels hors banc ;
- validation humaine complète zoom 200 %, contraste OS élevé et lecteurs d’écran ;
- accès au compte développeur et décision finale des reviewers ATN.
"""
write(ROOT / "STORE_RELEASE.md", store)

# ATN checklist: distinguish inherited manual acceptance from fresh automated evidence.
checklist = """# Checklist de publication Add-ons for Thunderbird — 1.6.1

Les cases cochées correspondent à des éléments présents dans l’artefact/repo ou à des validations automatisées exigées par le processus de release. Les cases non cochées nécessitent encore une action humaine, un fournisseur externe ou l’accès au portail ATN.

## Identité et fiche

- [x] nom MailPin, slogan, sous-titres FR/EN, auteur et assets synchronisés ;
- [x] identifiant permanent `ussmarines.mailpin@addons.thunderbird.net` défini avant première publication ATN ;
- [x] version 1.6.1 synchronisée dans manifeste, package, README, build et dossier reviewer ;
- [x] licence et politique de confidentialité présentes ;
- [ ] recherche juridique finale de disponibilité de la marque ;
- [ ] support et politique de confidentialité vérifiés dans le portail ATN au moment de la soumission.

## Compatibilité

- [x] Manifest V3 et clés de manifeste contrôlés ;
- [x] plage déclarée Thunderbird 153.0 à 153.* ;
- [x] thèmes clair/sombre, clipping, overflow et contraste de base couverts par les gardes automatisées existantes ;
- [x] comportements métier inchangés depuis la dernière recette utilisateur pré-rebranding 1.5.4 ; cette preuve est explicitement héritée et non renommée « recette 1.6.1 » ;
- [x] release 1.6.1 soumise à QA Linux/Windows, garde sécurité, build reproductible et smoke Thunderbird réel avant publication GitHub ;
- [ ] recette humaine ciblée du XPI 1.6.1 exact ;
- [ ] matrice fonctionnelle/charge 50/100/500/1000/2000 fraîche sur 1.6.1 — non relancée car logique métier inchangée ;
- [ ] matrice Windows/Linux/macOS Thunderbird réelle exhaustive ;
- [ ] Gmail/Microsoft/IMAP et calendriers réseau réels.

## Review et build

- [x] code lisible, non minifié, non transpilé et non obfusqué ;
- [x] instructions de build reproductible ;
- [x] archive source complète sans profil ni secret ;
- [x] aucune bibliothèque tierce runtime/build ajoutée ;
- [x] actions GitHub épinglées par SHA ;
- [x] release GitHub v1.6.1 destinée à être produite par le gate final avant utilisation de ce dossier pour ATN ;
- [ ] téléversement du XPI et de l’archive source sur ATN.

## Confidentialité et sécurité

- [x] permissions minimales (`menus`), CSP sans réseau et scans standards contrôlés ;
- [x] aucune nouvelle permission, dépendance runtime, télémétrie, publicité ou code distant en 1.6.1 ;
- [x] changement d’identité documenté comme ayant eu lieu en 1.6.0 — il n’est plus nié dans les documents actifs ;
- [x] Codex Security non utilisé ;
- [ ] validation avec fournisseurs mail/calendrier externes réels ;
- [ ] validation humaine complète zoom 200 %, contraste OS élevé et lecteurs d’écran.

## Traçabilité

- [x] rebranding MailPin intégré par PR #35 ;
- [x] runtime rebrand exact `4fdb978e1828325001f95951c115059a931b8b6e` : QA Linux/Windows, garde sécurité et smoke Thunderbird réel verts ;
- [x] XPI public v1.6.0 de référence : SHA-256 `6860e0177795b163cb672edd1a93897260785c4b8eeeeac71d1b3d32dca281ae` ;
- [x] métadonnées 1.6.1 débarrassées des anciens PR/SHA/hashes 1.5.4 ;
- [ ] soumission et validation finales par les reviewers ATN.
"""
write(ROOT / "docs/ATN_RELEASE_CHECKLIST.md", checklist)

# Handoff current state, without stale 1.5.4 attribution.
handoff = f"""# Passage de relais Codex — MailPin 1.6.1

## Référence

- runtime MailPin intégré par la PR #35 : `{RUNTIME_SHA}` ;
- baseline `main` avant préparation 1.6.1 : `{BASELINE_SHA}` ;
- version cible publique : **1.6.1** ;
- identifiant canonique : `{ID}` ;
- branche de préparation : `release/mailpin-1.6.1-store-metadata`.

## État produit

MailPin 1.6.0 a introduit le nouveau nom, l’ID ATN définitif, l’icône SVG et la palette professionnelle sans modifier la logique métier validée avant rebranding. Le runtime rebrand intégré par #35 a ensuite repassé QA Linux/Windows, garde sécurité et smoke Thunderbird 153 réel sur le commit exact `{RUNTIME_SHA}`.

La 1.6.1 ne corrige pas un bug runtime. Elle retire des métadonnées de publication 1.5.4 restées actives dans l’archive source 1.6.0 et évite d’attribuer à tort une recette manuelle fraîche à un XPI qui ne l’avait pas reçue. Le seul delta XPI prévu est `manifest.version = 1.6.1`.

## Preuves

- recette manuelle : dernière preuve fraîche sur le candidat 1.5.4 avant rebranding, réutilisée uniquement pour le métier inchangé ;
- QA/sécurité/smoke réel MailPin 1.6.0 : verts sur `{RUNTIME_SHA}` ;
- XPI v1.6.0 public : `{XPI_160_SHA}` ;
- 1.6.1 : exiger QA Linux/Windows + sécurité + `npm run ci` + smoke Thunderbird réel sur la PR et le `main` final avant release.

## Readiness

- **GitHub 1.6.1 : GO uniquement après les gates ci-dessus** ;
- **ATN : candidat officiel après release GitHub**, avec recette humaine ciblée, fournisseurs réseau/matrice multi-OS et contrôles accessibilité humains restant explicitement hors preuve.

Aucune nouvelle permission, dépendance runtime, connexion réseau, télémétrie, publicité ou migration de stockage n’est introduite en 1.6.1. Le changement d’identité a eu lieu volontairement en 1.6.0 et reste immuable pour la publication ATN. Codex Security n’a pas été utilisé.
"""
write(ROOT / "docs/CODEX_HANDOFF.md", handoff)

# Project memory: preserve detailed history, fix the current header and stale current-state claims.
memory_path = ROOT / "PROJECT_MEMORY.md"
memory = memory_path.read_text(encoding="utf-8")
memory = memory.replace(
    "> Version publique : **1.6.0**\n> Branche de référence : `main` ; runtime 1.6.0 intégré par la PR #33\n> Base GitHub de validation : `main` au commit `ca7206329045b58aff3384e7bd4c3b99eeecd2b3`",
    f"> Version publique : **1.6.1**\n> Branche de référence : `main` ; runtime MailPin intégré par la PR #35\n> Base runtime validée : `{RUNTIME_SHA}` ; préparation 1.6.1 dérivée de `{BASELINE_SHA}`"
)
memory = memory.replace(
    "La version 1.6.0 corrige les constats manuels de 1.5.3 :",
    "Le métier actuellement distribué reprend les corrections fonctionnelles consolidées avant le rebranding. La 1.6.0 a introduit l’identité MailPin et la 1.6.1 fiabilise uniquement le dossier de publication/review. Les corrections métier héritées couvrent :"
)
memory = memory.replace(
    "Elle n’ajoute aucune permission, dépendance runtime, migration ni connexion réseau.",
    "La 1.6.1 n’ajoute aucune permission, dépendance runtime, migration de stockage ni connexion réseau. Le changement d’ID a été introduit volontairement en 1.6.0 avant la première publication ATN."
)
memory = memory.replace(
    "La PR #33 puis le commit squash intégré à `main` ont ensuite repassé les workflows QA Linux/Windows et le smoke Thunderbird réel avec succès.",
    f"Le rebranding a été intégré par la PR #35. Le commit runtime `{RUNTIME_SHA}` a repassé les workflows QA Linux/Windows, la garde sécurité et le smoke Thunderbird réel avec succès."
)
memory = memory.replace(
    "Pour la 1.6.0, le banc ciblé 50 références sous Thunderbird 153.0.3 a revalidé les chemins modifiés :",
    "Avant rebranding, le banc ciblé 50 références sous Thunderbird 153.0.3 a revalidé les chemins métier ensuite conservés :"
)
memory = memory.replace(
    "- recette utilisateur finale verte ; QA Linux/Windows et smoke Thunderbird 153 réel verts sur la PR #33 puis sur `main`.",
    f"- recette utilisateur pré-rebranding 1.5.4 verte pour le métier inchangé ; cette preuve n’est pas renommée recette 1.6.1 ;\n- runtime MailPin `{RUNTIME_SHA}` : QA Linux/Windows, garde sécurité et smoke Thunderbird 153 réel verts ;\n- 1.6.1 ne modifie que la version du manifeste et les métadonnées de publication, et exige ses propres gates automatisés avant release."
)
write(memory_path, memory)

# Project state: machine-readable current scope, explicitly separating runtime baseline and release metadata.
state_path = ROOT / "docs/PROJECT_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["extensionVersion"] = VERSION
state["baseGitHub"] = {
    "branch": "main",
    "commit": BASELINE_SHA,
    "role": "pre-1.6.1 release-metadata baseline"
}
state["extensionId"] = ID
state.setdefault("testing", {})["browserStatus"] = (
    "Chromium DOM-flow and geometry evidence predates the branding-only release delta and remains applicable to unchanged business/layout behavior; "
    "MailPin identity/palette are covered by current static/UI guards."
)
state["testing"]["runtimeStatus"] = (
    f"MailPin 1.6.0 rebrand runtime commit {RUNTIME_SHA} passed Linux/Windows QA, security guard and real Thunderbird 153 smoke. "
    "MailPin 1.6.1 changes only manifest version plus publication/reviewer metadata; its release process must rerun full QA and real Thunderbird smoke. "
    "No fresh manual 1.6.1 XPI acceptance is claimed."
)
write(state_path, json.dumps(state, ensure_ascii=False, indent=2))

# New release-specific audit/validation docs. Historical 1.6.0 reports remain immutable.
security = f"""# Audit de sécurité — MailPin 1.6.1

## Périmètre du delta

La 1.6.1 est une correction de version et de métadonnées de publication. Par rapport au runtime 1.6.0, aucune logique métier ni frontière privilégiée n’est modifiée. Dans le XPI, seul `manifest.version` passe de 1.6.0 à 1.6.1 ; les autres changements sont des documents/build metadata hors runtime.

## Invariants contrôlés

- ID inchangé : `{ID}` ;
- permission WebExtension : `menus` uniquement ;
- CSP : `connect-src 'none'` ;
- aucun réseau runtime, télémétrie, publicité, CDN ou code distant ;
- aucun nouveau stockage de corps de message ou pièce jointe ;
- aucune nouvelle dépendance runtime/build ;
- API Experiment `pinInbox`, adaptateurs `PinCompatibility`, schémas SQLite/settings/data et préfixes persistants inchangés.

## Validation

La PR 1.6.1 doit passer les gardes standards du dépôt, `npm run ci`, Linux/Windows, scan d’identité/secrets et smoke Thunderbird réel. Codex Security n’est pas utilisé. La matrice de charge 50–2000 et les fournisseurs réseau ne sont pas relancés car aucune surface métier correspondante ne change.
"""
write(ROOT / "SECURITY_AUDIT_1.6.1.md", security)

validation = f"""# Rapport de validation — MailPin 1.6.1

## Objectif

Produire un candidat reviewer/ATN dont les métadonnées décrivent exactement les preuves disponibles, sans modifier le comportement de MailPin.

## Delta

- `package.json` / `extension/manifest.json` : version 1.6.1 ;
- documents actifs de publication, mémoire projet, état machine et templates reviewers corrigés ;
- nouveaux rapports 1.6.1 ;
- aucune modification des modules métier, de `background.js`, du schéma Experiment, des adaptateurs Thunderbird, du stockage ou des styles runtime.

## Preuves réutilisées

- recette utilisateur : build pré-rebranding 1.5.4, uniquement pour les comportements métier inchangés ;
- rebranding/runtime MailPin : PR #35, commit `{RUNTIME_SHA}`, QA Linux/Windows + garde sécurité + smoke Thunderbird 153 réel verts ;
- release 1.6.0 : XPI SHA-256 `{XPI_160_SHA}`.

## Preuves requises pour 1.6.1

Avant publication : contrôles de version/métadonnées, `npm run ci`, `git diff --check`, QA Linux/Windows, garde sécurité et smoke Thunderbird réel sur le candidat 1.6.1. Une recette humaine exacte du XPI 1.6.1 n’est pas revendiquée tant qu’elle n’est pas réellement effectuée.
"""
write(ROOT / "VALIDATION_REPORT_1.6.1.md", validation)

# Verify release-template JSON remains valid and canonical.
store_template = ROOT / "release/manifest-store-template.json"
json.loads(store_template.read_text(encoding="utf-8"))

# Remove one-shot script from the final diff.
Path(__file__).unlink()
print("MailPin 1.6.1 store-metadata preparation complete")
