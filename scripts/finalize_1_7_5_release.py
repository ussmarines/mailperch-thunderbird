#!/usr/bin/env python3
from pathlib import Path
import json

XPI_SHA = "247e314911ce1006f40b78c6050f3697b7f6b1beb3f0489214e84410c668dc12"
SOURCE_SHA = "af555557bc0d3b80d35e34a7ec1447b77ebe356c75a95ece9f28b8238fdfb1fd"
SUMS_SHA = "db052f49548aa70e46208808084be3e5ef2ac8d454267e1babc53aeeb647ad26"
TAG_TARGET = "2384ee52df95a711424dfeb817ef114888634ed0"
CANDIDATE = "19cf23c21e983be924ffd9e6af8fdb1e8e612947"
QA = "32480175617"
SMOKE = "32480175435"
VERIFY_RUN = "32481646372"
NAME = "MailPin — Email Follow-up & Productivity"


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def replace(path, old, new):
    text = read(path)
    assert old in text, f"{path}: missing expected token {old!r}"
    write(path, text.replace(old, new))


# README FR/EN.
replace("README.md", "release-v1.7.4-4F7F75", "release-v1.7.5-4F7F75")
replace("README.md", "candidate-v1.7.5-3D536B", "source-v1.7.5-3D536B")
replace("README.md", "**Organic Workspace** reste inchangé dans la source 1.7.5 ; cette candidate modifie uniquement le nom public/localisé requis par ATN.", "**Organic Workspace** reste inchangé dans la release 1.7.5 ; cette maintenance modifie uniquement le nom public/localisé afin de respecter la limite ATN de 50 caractères.")
replace("README.md", "- **Version source :** `1.7.5` — candidate", "- **Version source :** `1.7.5` — publiée")
replace("README.md", "- **Dernière release publique :** `1.7.4`", "- **Dernière release publique :** `1.7.5`")
replace("README.md", "1. Téléchargez `MailPin_v1.7.4.xpi` depuis la release `v1.7.4`.", "1. Téléchargez `MailPin_v1.7.5.xpi` depuis la release `v1.7.5`.")

replace("README.en.md", "release-v1.7.4-4F7F75", "release-v1.7.5-4F7F75")
replace("README.en.md", "candidate-v1.7.5-3D536B", "source-v1.7.5-3D536B")
replace("README.en.md", "**Organic Workspace** is unchanged in source 1.7.5; this candidate only changes the public/localized add-on name required by ATN.", "**Organic Workspace** is unchanged in release 1.7.5; this maintenance only shortens the public/localized add-on name to comply with ATN's 50-character limit.")
replace("README.en.md", "- **Source version:** `1.7.5` — candidate", "- **Source version:** `1.7.5` — published")
replace("README.en.md", "- **Latest public release:** `1.7.4`", "- **Latest public release:** `1.7.5`")
replace("README.en.md", "1. Download `MailPin_v1.7.4.xpi` from release `v1.7.4`.", "1. Download `MailPin_v1.7.5.xpi` from release `v1.7.5`.")

# Operational memory.
replace("PROJECT_MEMORY.md", "> Dernière release publique : **1.7.4**", "> Dernière release publique : **1.7.5**")
replace("PROJECT_MEMORY.md", "> Branche courante : `release/atn-name-1.7.5` ; candidate de conformité ATN", "> Branche courante : `release/finalize-1.7.5` ; finalisation documentaire post-publication")
old_summary = "MailPin est une extension Thunderbird Manifest V3 locale. La source 1.7.5 raccourcit uniquement le nom public/localisé à **MailPin — Email Follow-up & Productivity** afin de respecter la limite ATN de 50 caractères. La logique métier, l’API Experiment, `PinCompatibility`, les schémas, le stockage, les permissions et la plage Thunderbird 153.0–154.* restent inchangés. La release 1.7.4 a passé la QA `32300356172` et le smoke réel Thunderbird 154.0 `32300356085`; la candidate 1.7.5 doit repasser les gates applicables sur son head exact avant publication."
new_summary = f"MailPin est une extension Thunderbird Manifest V3 locale. La release 1.7.5 raccourcit uniquement le nom public/localisé à **{NAME}** (40 caractères) afin de respecter la limite ATN de 50 caractères. La logique métier, l’API Experiment, `PinCompatibility`, les schémas, le stockage, les permissions et la plage Thunderbird 153.0–154.* restent inchangés. La candidate exacte `{CANDIDATE}` a passé la QA `{QA}` et le smoke réel Thunderbird 154.0 `{SMOKE}`. Le tag `v1.7.5` cible exactement `{TAG_TARGET}` et les artefacts publics ont été vérifiés dans le run `{VERIFY_RUN}`."
replace("PROJECT_MEMORY.md", old_summary, new_summary)
replace("PROJECT_MEMORY.md", "- source : 1.7.5 candidate ; dernière release publique : 1.7.4 ;", "- source : 1.7.5 publiée ; dernière release publique : 1.7.5 ;")
replace("PROJECT_MEMORY.md", "- release 1.7.4 : QA `32300356172` — PASS ; smoke Thunderbird 154.0 `32300356085` — PASS ;\n- candidate 1.7.5 : contrôle du nom, QA/build et smoke Thunderbird 154.0 frais requis avant merge/publication.", f"- candidate exacte 1.7.5 `{CANDIDATE}` : QA `{QA}` — PASS ; smoke Thunderbird 154.0 `{SMOKE}` — PASS ;\n- release `v1.7.5` : tag `{TAG_TARGET}`, build reviewer hors `.git` PASS, artefacts publics vérifiés `{VERIFY_RUN}` — PASS.")

# Machine-readable project state.
state_path = Path("docs/PROJECT_STATE.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
state["baseGitHub"] = {
    "branch": "main",
    "commit": TAG_TARGET,
    "role": "published v1.7.5 tag target after ATN name-compliance gates",
}
state["developmentBranch"] = "release/finalize-1.7.5"
state["testing"]["browserStatus"] = "No UI/runtime behavior change in 1.7.5; only the localized/public add-on name was shortened to 40 characters for ATN."
state["testing"]["runtimeStatus"] = f"Exact 1.7.5 candidate {CANDIDATE} passed QA {QA} and real Thunderbird 154.0 smoke {SMOKE}. The release publisher rebuilt from the reviewer archive without .git before publishing v1.7.5 at {TAG_TARGET}; public assets were independently verified in run {VERIFY_RUN}."
state["latestPublicVersion"] = "1.7.5"
state["releaseStatus"] = "published"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

write("STORE_RELEASE.md", f"""# Publication MailPin 1.7.5

## État

- **Version source :** 1.7.5 — publiée
- **Dernière release publique :** 1.7.5
- **Dernière publication :** `v1.7.5`, commit `{TAG_TARGET}`
- **Nom public/localisé :** `{NAME}` — 40 caractères
- **ID permanent :** `ussmarines.mailpin@addons.thunderbird.net`
- **Compatibilité publiée :** Thunderbird 153.0 à 154.*

## Portée 1.7.5

La 1.7.5 corrige uniquement la conformité du nom Add-ons for Thunderbird : le nom 1.7.4 embarqué faisait 56 caractères, au-delà de la limite ATN de 50. Le nom publié fait désormais 40 caractères.

Aucune logique métier, API Experiment, frontière `PinCompatibility`, permission, migration, schéma, stockage, dépendance runtime, connexion réseau, télémétrie, publicité, CDN ou code distant n’est modifié.

## Preuves

- candidate exacte `{CANDIDATE}` : QA Linux/Windows + garde sécurité/identité `{QA}` — PASS ;
- même candidate : smoke réel Thunderbird 154.0 `{SMOKE}` — PASS ;
- tag `v1.7.5` : `{TAG_TARGET}` ;
- publisher : `npm run ci` depuis le checkout puis depuis l’archive reviewer fraîche sans `.git`, XPI reconstruit SHA-identique — PASS ;
- vérification indépendante des artefacts publics : run `{VERIFY_RUN}` — PASS ;
- `MailPin_v1.7.5.xpi` — 254 557 octets — SHA-256 `{XPI_SHA}` ;
- `MailPin_GitHub_Repository_v1.7.5.zip` — 689 068 octets — SHA-256 `{SOURCE_SHA}` ;
- `SHA256SUMS.txt` — SHA-256 `{SUMS_SHA}`.

## Gates GitHub

- [x] nom localisé FR/EN = 40 caractères et garde anti-régression ≤ 50 ;
- [x] QA Linux/Windows sur la candidate exacte ;
- [x] garde sécurité/identité ;
- [x] build reproductible et structure XPI ;
- [x] smoke Thunderbird 154.0 réel ;
- [x] merge sur `main` ;
- [x] archive reviewer reconstruite sans `.git` ;
- [x] tag/release `v1.7.5` publié ;
- [x] artefacts publics et empreintes vérifiés ;
- [ ] soumission/revue ATN.

La recette humaine 1.7.5 et les fournisseurs/calendriers réseau réels restent des validations distinctes lorsqu’ils sont revendiqués. Codex Security n’a pas été utilisé.
""")

write("docs/ATN_RELEASE_CHECKLIST.md", f"""# Checklist Add-ons for Thunderbird — MailPin 1.7.5

Dernière release GitHub publique : **1.7.5**. La **version source 1.7.5** est publiée et prête pour une nouvelle soumission Add-ons for Thunderbird.

## Identité et build

- [x] ID `ussmarines.mailpin@addons.thunderbird.net` inchangé ;
- [x] nom public/localisé `{NAME}` (40 caractères, limite ATN 50) ;
- [x] version source 1.7.5 synchronisée ;
- [x] aucune nouvelle dépendance runtime/build tierce ;
- [x] aucune nouvelle permission WebExtension ;
- [x] QA/build exacts et release `v1.7.5` publiés.

## Compatibilité Thunderbird

- [x] Manifest V3, permission `menus` uniquement, plage Thunderbird 153.0–154.* inchangée ;
- [x] candidate exacte `{CANDIDATE}` : QA `{QA}` PASS ;
- [x] même candidate : smoke réel Thunderbird 154.0 `{SMOKE}` PASS ;
- [ ] recette visuelle humaine sur le XPI 1.7.5 si souhaitée avant ATN ;
- [ ] Gmail/Microsoft/IMAP et calendriers réseau réels uniquement s’ils sont revendiqués dans la soumission.

## Sécurité / review

- [x] réseau runtime, télémétrie, publicité, CDN et code distant interdits ;
- [x] aucune modification de stockage, schéma, logique métier ou `PinCompatibility` ;
- [x] audit source `SECURITY_AUDIT_1.7.5.md` sans Codex Security ;
- [x] build reproductible et structure XPI validés ;
- [x] `npm run ci` depuis une extraction neuve de l’archive reviewer publiée sans `.git` ;
- [x] XPI reconstruit identique au XPI publié ;
- [ ] téléversement et revue humaine ATN.

Artefacts officiels :
- XPI SHA-256 `{XPI_SHA}` ;
- source reviewer SHA-256 `{SOURCE_SHA}`.

Aucun contrôle non exécuté n’est présenté comme PASS.
""")

write("release/BUILD_INSTRUCTIONS.md", f"""# Instructions de build pour les reviewers — MailPin 1.7.5

## État

La release GitHub **1.7.5** est publiée. La source **1.7.5** correspond à la version officielle destinée à ATN et conserve la compatibilité Thunderbird 153.0–154.*.

## Environnement

- Ubuntu 24.04 ou équivalent ;
- Python 3.11+ ;
- Node.js 20+ et npm 10+ ;
- Git uniquement pour un checkout ou les contrôles d’historique.

**Git n’est pas requis** pour reproduire le build depuis l’archive source extraite. Aucune dépendance npm/Python tierce n’est installée.

## Reproduction

Dans un checkout de la source MailPin 1.7.5 ou dans l’archive reviewer extraite sans `.git` :

```bash
npm run ci
```

Livrables :

```text
dist/MailPin_v1.7.5.xpi
dist/MailPin_GitHub_Repository_v1.7.5.zip
dist/SHA256SUMS.txt
```

Le contenu de `extension/` est placé directement à la racine du XPI. Aucun JavaScript/CSS n’est minifié, transpilé, concaténé, généré ou obfusqué.

## Portée 1.7.5

La 1.7.5 raccourcit uniquement le nom localisé à `{NAME}` pour respecter la limite ATN de 50 caractères. Elle n’ajoute aucune permission, dépendance runtime, migration, schéma, réseau, télémétrie, publicité ou code distant.

## Preuves

- candidate exacte `{CANDIDATE}` : QA `{QA}` — PASS ;
- smoke réel Thunderbird 154.0 `{SMOKE}` — PASS ;
- tag `v1.7.5` : `{TAG_TARGET}` ;
- le publisher a exécuté `npm run ci` depuis une extraction neuve de l’archive reviewer sans `.git` et a vérifié que le XPI reconstruit avait le même SHA-256 que le XPI initial ;
- artefacts publics revérifiés dans le run `{VERIFY_RUN}` — PASS.

XPI SHA-256 : `{XPI_SHA}`.
Archive source SHA-256 : `{SOURCE_SHA}`.
SHA256SUMS.txt SHA-256 : `{SUMS_SHA}`.
""")

write("release/ATN_REVIEW_NOTES_TEMPLATE.md", f"""# Notes pour les reviewers ATN — MailPin 1.7.5

## Statut

- **Dernière release GitHub publique :** 1.7.5
- **Source publiée :** 1.7.5
- **Version :** 1.7.5
- **Soumission ATN :** prête à effectuer

## Identité

- **Nom :** {NAME}
- **Longueur du nom :** 40 caractères
- **ID :** `ussmarines.mailpin@addons.thunderbird.net`
- **Compatibilité :** Thunderbird 153.0 à 154.*
- **Permission WebExtension :** `menus` uniquement

## Correctif 1.7.5

Le nom localisé précédent contenait 56 caractères et dépassait la limite ATN de 50 caractères. La 1.7.5 utilise `{NAME}` (40 caractères). Aucun comportement runtime n’est modifié.

Aucune permission, migration, dépendance runtime, télémétrie, publicité, connexion réseau ou code distant n’est ajouté.

## Build

Voir `release/BUILD_INSTRUCTIONS.md`. La commande reviewer est `npm run ci` depuis l’archive source extraite. Le build hors `.git` a été exécuté avant publication et le XPI reconstruit est SHA-identique au XPI publié.

XPI SHA-256 : `{XPI_SHA}`.
Archive source SHA-256 : `{SOURCE_SHA}`.

## Test rapide

1. Installer le XPI dans Thunderbird 154.0 et confirmer le nom `{NAME}`.
2. Confirmer l’injection unique du panneau et du bouton Quick Filter.
3. Ouvrir le Dashboard depuis le panneau et confirmer un seul onglet.
4. Épingler/désépingler et confirmer l’absence de modification lu/non-lu ou compteurs natifs.
5. Désinstaller/réinstaller et confirmer le nettoyage puis l’injection unique.

Voir `PRIVACY.md`, `SECURITY.md`, `SECURITY_AUDIT_1.7.5.md` et `release/BUILD_INSTRUCTIONS.md`.
""")

write("SECURITY_AUDIT_1.7.5.md", f"""# Audit de sécurité — MailPin 1.7.5

## Portée

MailPin 1.7.5 est une maintenance de métadonnées pour conformité ATN. Le changement installable est limité au nom localisé/store et au numéro de version.

## Invariants vérifiés

- ID `ussmarines.mailpin@addons.thunderbird.net` inchangé ;
- Thunderbird 153.0–154.* inchangé ;
- permission `menus` inchangée ;
- aucune logique métier, API Experiment, `PinCompatibility`, stockage, schéma ou migration modifié ;
- aucun réseau runtime, télémétrie, publicité, CDN ou code distant ajouté.

## Gates exécutés

- QA Linux/Windows et garde sécurité/identité `{QA}` — PASS ;
- smoke réel Thunderbird 154.0 `{SMOKE}` — PASS ;
- build reviewer sans `.git` + XPI SHA-identique avant publication — PASS ;
- vérification indépendante des artefacts publics `{VERIFY_RUN}` — PASS ;
- tag publié `v1.7.5` → `{TAG_TARGET}`.

Codex Security n’a pas été utilisé.
""")

write("VALIDATION_REPORT_1.7.5.md", f"""# Rapport de validation — MailPin 1.7.5

## Objectif

Valider la correction de conformité ATN : le nom localisé de la 1.7.4 faisait 56 caractères alors que le formulaire ATN impose un maximum de 50.

## Critères PASS/FAIL

PASS exige :
- `extensionName` FR et EN exactement `{NAME}` ;
- longueur du nom = 40 caractères et ≤ 50 ;
- version 1.7.5 synchronisée ;
- ID et plage Thunderbird inchangés ;
- QA Linux/Windows et build reproductible PASS ;
- smoke Thunderbird 154.0 PASS sur le head exact ;
- artefacts publiés et archive reviewer reproductible hors `.git`.

## Résultat

**PASS.**

- candidate exacte : `{CANDIDATE}` ;
- QA Linux/Windows + garde sécurité/identité : `{QA}` — PASS ;
- smoke réel Thunderbird 154.0 : `{SMOKE}` — PASS ;
- release/tag `v1.7.5` : `{TAG_TARGET}` ;
- nom FR/EN : 40 caractères — PASS ;
- archive reviewer fraîche sans `.git` : `npm run ci` — PASS ;
- XPI reconstruit identique au XPI publié — PASS ;
- vérification indépendante des artefacts publics : `{VERIFY_RUN}` — PASS ;
- XPI SHA-256 : `{XPI_SHA}` ;
- source reviewer SHA-256 : `{SOURCE_SHA}`.
""")

# Bug tracker.
replace("docs/BUG_TRACKER.md", "Dernière release publique : **1.7.4**", "Dernière release publique : **1.7.5**")
old_bug = "| MP-2026-060 | 1.7.4 | ATN refuse la soumission car le nom embarqué de l’extension dépasse 50 caractères. | `extensionName` vaut `MailPin — Email Follow-up & Productivity for Thunderbird` (56 caractères) dans les locales FR/EN. | `extension/_locales/*/messages.json`, métadonnées et gardes de nom | `scripts/check_repo.py`, `tests/static_checks.py`, QA/build/smoke | À VALIDER | 1.7.5 | Nouveau nom `MailPin — Email Follow-up & Productivity` mesuré à 40 caractères ; candidate 1.7.5 à valider puis publier avant nouvelle soumission ATN. |"
new_bug = f"| MP-2026-060 | 1.7.4 | ATN refuse la soumission car le nom embarqué de l’extension dépasse 50 caractères. | `extensionName` vaut `MailPin — Email Follow-up & Productivity for Thunderbird` (56 caractères) dans les locales FR/EN. | `extension/_locales/*/messages.json`, métadonnées et gardes de nom | `scripts/check_repo.py`, `tests/static_checks.py`, QA/build/smoke | CORRIGÉ | 1.7.5 | Nom `{NAME}` = 40 caractères ; candidate `{CANDIDATE}` : QA `{QA}` PASS et smoke Thunderbird 154 `{SMOKE}` PASS ; tag `v1.7.5` `{TAG_TARGET}` ; artefacts publics `{VERIFY_RUN}` PASS. |"
replace("docs/BUG_TRACKER.md", old_bug, new_bug)

write("docs/KNOWN_LIMITATIONS.md", """# Limites connues — MailPin

## Source 1.7.5 / release publique 1.7.5

La source **1.7.5** et la release publique **1.7.5** sont alignées. Cette maintenance porte uniquement sur le nom public/localisé pour conformité ATN.

- compatibilité revendiquée : Thunderbird 153.0 à 154.* ;
- le changement 1.7.5 porte uniquement sur le nom public/localisé, pas sur le comportement runtime ;
- Agenda reste facultatif et dépend des capacités réelles du calendrier ;
- fournisseurs réseau et calendriers distants restent des validations distinctes ;
- aucune nouvelle permission, migration, dépendance runtime ou connexion réseau n’est introduite.
""")

replace("docs/MANUAL_TEST_PLAN.md", "la dernière release publique est 1.7.4", "la dernière release publique est 1.7.5")
replace("docs/MANUAL_TEST_PLAN.md", "Le XPI testé doit correspondre exactement à la candidate/release 1.7.5 concernée.", "Le XPI testé doit correspondre exactement à la release publique 1.7.5.")

write("docs/CODEX_HANDOFF.md", f"""# Passage de relais — MailPin 1.7.5 publiée

## État

- branche : `release/finalize-1.7.5` ;
- version source : **1.7.5** ;
- dernière release publique : **1.7.5** ;
- Thunderbird : 153.0 à 154.* ;
- ID : `ussmarines.mailpin@addons.thunderbird.net` ;
- nom ATN : `{NAME}` — 40 caractères.

## Résultat

La maintenance 1.7.5 est publiée. Elle raccourcit uniquement le nom localisé/store pour respecter la limite ATN de 50 caractères.

Candidate exacte `{CANDIDATE}` : QA `{QA}` PASS, smoke réel Thunderbird 154.0 `{SMOKE}` PASS. Tag `v1.7.5` : `{TAG_TARGET}`. Le build reviewer sans `.git` a reproduit un XPI SHA-identique et les artefacts publics ont été vérifiés dans `{VERIFY_RUN}`.

## Suite

La prochaine action produit est la nouvelle soumission ATN avec le XPI et l’archive source 1.7.5 publiés. Aucun changement runtime supplémentaire n’est requis pour cette soumission.

Codex Security n’est pas requis.
""")

template_path = Path("release/manifest-store-template.json")
template = json.loads(template_path.read_text(encoding="utf-8"))
template["note"] = "Référence de métadonnées pour MailPin 1.7.5 publié, dernière release publique. Le nom public/localisé fait 40 caractères et respecte la limite ATN de 50 caractères."
template_path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Latest useful validation evidence.
validation_path = Path("docs/AI_VALIDATION_STATE.json")
validation = json.loads(validation_path.read_text(encoding="utf-8"))
validation["recorded_at"] = "2026-08-21T14:25:00+02:00"
validation["baseline"] = {
    "repository": "ussmarines/mailpin-thunderbird",
    "branch": "main",
    "commit_sha": TAG_TARGET,
    "tree_sha": "",
    "working_tree_patch_id": "",
    "untracked_candidate_files": [],
}
validation["repository_checks"] = [{
    "id": "github-release-1-7-5-gate",
    "result": "success",
    "validated_commit": TAG_TARGET,
    "working_tree_patch_id": "",
    "validated_at": "2026-08-21T14:25:00+02:00",
    "command": f"PR #55 QA {QA} + Thunderbird runtime smoke {SMOKE} + published-asset verification {VERIFY_RUN}",
    "environment": {
        "ci": "GitHub Actions",
        "linux": "ubuntu-24.04",
        "windows": "windows-latest",
        "thunderbird": "154.0",
    },
    "invalidates_on": [
        "extension/**", "package.json", "scripts/**", "tests/**",
        ".github/workflows/ci.yml", ".github/workflows/thunderbird-smoke.yml",
        "docs/PROJECT_STATE.json"
    ],
    "evidence": {
        "kind": "github-release-gate",
        "summary": "MailPin 1.7.5: localized ATN name 40 chars; QA Linux/Windows, identity/security guard, reproducible build, real Thunderbird 154 smoke, reviewer-source build without .git, and public release asset verification all passed.",
        "qa_run": int(QA),
        "thunderbird_smoke_run": int(SMOKE),
        "public_asset_verification_run": int(VERIFY_RUN),
        "xpi_sha256": XPI_SHA,
        "source_sha256": SOURCE_SHA,
    },
}]
validation["targeted_checks"] = []
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

write("release/ATN_SUBMISSION_1.7.5.md", f"""# Soumission Add-ons for Thunderbird — MailPin 1.7.5

## Artefacts officiels

- XPI : `MailPin_v1.7.5.xpi` — SHA-256 `{XPI_SHA}`
- Source reviewer : `MailPin_GitHub_Repository_v1.7.5.zip` — SHA-256 `{SOURCE_SHA}`
- Checksums : `SHA256SUMS.txt` — SHA-256 `{SUMS_SHA}`

## Métadonnées

- Nom : `{NAME}`
- Version : `1.7.5`
- ID : `ussmarines.mailpin@addons.thunderbird.net`
- Compatibilité : Thunderbird 153.0–154.*
- Support : `https://github.com/ussmarines/mailpin-thunderbird`
- Licence : `MailPin Source-Available License 1.1`

## Résumé EN

Pin, organize and follow up on important emails in Thunderbird with notes, subtasks, reminders, saved views, Calendar integration and a local dashboard.

## Catégories recommandées

- Message and News Reading
- Calendar and Date/Time

## Cases

- Experimental add-on : **non**
- Requires payment/non-free services/software/additional hardware : **non**
- Privacy Policy : **oui**, utiliser le texte complet de `PRIVACY.md`

## Reviewer

Utiliser le contenu de `release/ATN_REVIEW_NOTES_TEMPLATE.md` et les instructions `release/BUILD_INSTRUCTIONS.md`.
""")

print("MailPin 1.7.5 final published state prepared")
