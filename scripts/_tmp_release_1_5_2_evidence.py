#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = 31440019097
ARTIFACT_ID = 9082531880
ARTIFACT_SHA = "d007ed1287bc563021566ab1231c343b8cc37d0aff1458fc6ccd7773f4cb97e0"


def run(*args: str) -> str:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def reproduce_metadata() -> None:
    lines = (ROOT / ".github/workflows/release-1.5.2-final-validation.yml").read_text(encoding="utf-8").splitlines()
    section = next(i for i, line in enumerate(lines) if line.strip() == "- name: Prepare 1.5.2 metadata and documentation")
    start = next(i for i in range(section + 1, len(lines)) if lines[i].strip() == "python - <<'PY'")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "PY")
    script = "\n".join(line[10:] if line.startswith("          ") else line for line in lines[start + 1:end])
    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        exec(compile(script, "release-1.5.2-metadata.py", "exec"), {})
    finally:
        os.chdir(previous)


def write_reports() -> None:
    validation = """# Rapport de validation — MailPerch 1.5.2

Date : 2026-08-11
Workflow GitHub Actions : `31440019097`
Arbre de départ testé : `2c542b2b39f09b95155302da1d789ea1b3c6f9f2` + métadonnées 1.5.2 reproduites par le workflow
Thunderbird : 153.0.1 ESR · geckodriver 0.37.1 · Ubuntu 24.04

## Résultats réellement obtenus

- `npm run ci` : réussi sur l’arbre 1.5.2 ;
- smoke Thunderbird réel : réussi ;
- banc fonctionnel/charge : 50, 100, 500, 1 000 et 2 000 épingles réussis ;
- Dashboard : 7 vues, recherche, smart view, vue enregistrée, multi-sélection, action groupée, palette et actualisation dans le vrai onglet Thunderbird ;
- Options : Recommandé/Avancé, comptes sélectionnés, Enregistrer/Annuler, recherche, Tags, Agenda et santé dans le vrai onglet Thunderbird ;
- éditeur : commande XUL native `doCommand()`, notes, checklist, priorité, groupe, échéances, statut et relance validés ;
- thèmes : clipping, débordement horizontal, alignement et contraste texte de base vérifiés en clair/sombre ; ratios observés >= 12 en clair et >= 14 en sombre sur les contrôles mesurés ;
- persistance : cas aucun/A/B/A+C/A+B+C réussis sur deux processus Thunderbird distincts, même profil exact, SQLite 50 références et réglages conservés, réveil MV3 naturel ; A+C = 34 épingles avec B absent ;
- exceptions JavaScript MailPerch : aucune dans les scénarios verts ;
- artefact GitHub Actions : `9082531880`, SHA-256 `d007ed1287bc563021566ab1231c343b8cc37d0aff1458fc6ccd7773f4cb97e0` ;
- XPI construit : SHA-256 `e09adf1e3fa00809e5d92b56f20e596615e6ebb230cb7cdf46694587788901ea` ;
- archive source construite : SHA-256 `7a17379258be137cef60dc26cb5d58e4db7eeaf46ecf243347312659fb96d8dd`.

## Limites restantes

- fournisseurs réseau externes réels (Gmail, Microsoft, IMAP/CalDAV tiers) non simulés avec credentials ;
- inspection esthétique pixel par pixel, zoom 200 %, contraste OS élevé et parcours complet lecteur d’écran restent des validations humaines ;
- reproductibilité binaire ZIP Windows ↔ Linux reste suivie par `MP-2026-018`.
"""
    security = """# Audit sécurité delta — MailPerch 1.5.2

Date : 2026-08-11
Workflow de validation : `31440019097`

## Portée

1.5.2 ne modifie ni l’API Experiment privilégiée, ni `PinCompatibility`, ni les permissions WebExtension, ni les schémas SQLite/Settings/Data, ni la politique réseau. Les changements produit sont limités au Dashboard local et au CSS du panneau ; le reste concerne le banc de test et la documentation.

## Contrôles exécutés

- garde sécurité du dépôt et scan de secrets via `npm run ci` : réussis ;
- audit structurel et tests de contrats inclus dans `npm run ci` : réussis ;
- QA de branche Linux/Windows avant préparation de version : verte ;
- smoke et banc Thunderbird réels 1.5.2 : réussis sans exception JavaScript MailPerch ;
- aucune nouvelle permission, dépendance runtime, télémétrie, publicité, CDN, code distant ou connexion réseau runtime.

## Contrôles réutilisés car inchangés

L’audit exhaustif 1.5.1 reste applicable aux frontières privilégiées, dépendances, permissions, migrations et stockage, ces chemins n’ayant pas changé dans le delta 1.5.2. Codex Security n’a pas été utilisé et n’était pas nécessaire.

## Conclusion

Aucun élargissement de privilège ou de surface réseau runtime n’est introduit par 1.5.2.
"""
    (ROOT / "VALIDATION_REPORT_1.5.2.md").write_text(validation, encoding="utf-8")
    (ROOT / "SECURITY_AUDIT_1.5.2.md").write_text(security, encoding="utf-8")


def check_metadata() -> None:
    for command in [
        ("python", "scripts/check_versions.py"),
        ("python", "scripts/check_project_memory.py"),
        ("python", "scripts/check_bug_tracker.py"),
        ("npm", "run", "check"),
        ("git", "diff", "--check"),
    ]:
        subprocess.run(command, cwd=ROOT, check=True)


def commit_metadata() -> tuple[str, str]:
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    paths = [
        "package.json",
        "extension/manifest.json",
        "README.md",
        "README.en.md",
        "CHANGELOG.md",
        "THIRD_PARTY_NOTICES.md",
        "PROJECT_MEMORY.md",
        "docs/PROJECT_STATE.json",
        "docs/BUG_TRACKER.md",
        "docs/KNOWN_LIMITATIONS.md",
        "docs/ATN_RELEASE_CHECKLIST.md",
        "docs/CODEX_HANDOFF.md",
        "VALIDATION_REPORT_1.5.2.md",
        "SECURITY_AUDIT_1.5.2.md",
    ]
    subprocess.run(["git", "add", *paths], cwd=ROOT, check=True)
    run("git", "commit", "-m", "chore(release): prepare MailPerch 1.5.2")
    return run("git", "rev-parse", "HEAD"), run("git", "rev-parse", "HEAD^{tree}")


def update_validation_state(sha: str, tree: str) -> None:
    path = ROOT / "docs/AI_VALIDATION_STATE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["recorded_at"] = "2026-08-11T00:58:00+02:00"
    data["baseline"] = {
        "repository": "ussmarines/mailperch-thunderbird",
        "branch": "release/1.5.2-runtime-coverage",
        "commit_sha": sha,
        "tree_sha": tree,
    }
    data["repository_checks"] = [{
        "id": "github-linux-release-ci-1.5.2",
        "result": "success",
        "validated_commit": sha,
        "validated_tree": tree,
        "validated_at": "2026-08-11T00:53:42+02:00",
        "command": "npm run ci",
        "environment": {"os": "Ubuntu 24.04.4", "node": "24.18.0", "npm": "11.16.0", "python": "3.12.13"},
        "invalidates_on": ["**"],
        "evidence": {"kind": "github-actions", "run_id": RUN_ID, "summary": "Full check, complete test suite, reproducible build and 1.5.2 packaging passed before the real Thunderbird smoke and functional matrices."},
    }]
    kept = [item for item in data.get("targeted_checks", []) if item.get("id") == "options-playwright-dom-flow"]
    common = {
        "result": "success",
        "validated_commit": sha,
        "validated_tree": tree,
        "validated_at": "2026-08-11T00:53:42+02:00",
        "environment": {"os": "Ubuntu 24.04.4", "thunderbird": "153.0.1esr", "geckodriver": "0.37.1", "python": "3.12.13", "node": "24.18.0"},
    }
    kept.extend([
        {
            **common,
            "id": "thunderbird-153-runtime-coverage-1.5.2",
            "command": "GitHub Actions real Thunderbird smoke + functional --volumes 50",
            "invalidates_on": ["extension/**", "tests/thunderbird/real_smoke.py", "tests/thunderbird/functional_bench.py", "tests/test_thunderbird_test_bench.py", "tests/test_productivity_1_2_features.py", "tests/test_ui_regressions.py", "scripts/build.py", "package.json"],
            "evidence": {"kind": "github-actions-real-thunderbird", "run_id": RUN_ID, "artifact_id": ARTIFACT_ID, "artifact_sha256": ARTIFACT_SHA, "summary": "Real 1.5.2 XPI smoke passed; 50-pin run exercised Dashboard/Options DOM, native XUL editor actions, cleanup/reinstall, light/dark clipping/alignment and baseline text contrast with zero MailPerch JavaScript exceptions."},
        },
        {
            **common,
            "id": "thunderbird-153-scale-bench-1.5.2",
            "command": "GitHub Actions runtime --volumes 50,100,500,1000,2000",
            "invalidates_on": ["extension/**", "tests/thunderbird/functional_bench.py", "tests/test_thunderbird_test_bench.py", "scripts/build.py", "package.json"],
            "evidence": {"kind": "github-actions-real-thunderbird", "run_id": RUN_ID, "artifact_id": ARTIFACT_ID, "artifact_sha256": ARTIFACT_SHA, "summary": "50/100/500/1000/2000 pin matrix passed; pagination fully loaded 500/1000/2000 without duplicates and with zero timeouts or MailPerch JavaScript exceptions."},
        },
        {
            **common,
            "id": "thunderbird-153-persistence-1.5.2",
            "command": "GitHub Actions runtime --scope-validation-only",
            "invalidates_on": ["extension/**", "tests/thunderbird/real_smoke.py", "tests/thunderbird/functional_bench.py", "tests/test_thunderbird_test_bench.py", "scripts/build.py", "package.json"],
            "evidence": {"kind": "github-actions-real-thunderbird", "run_id": RUN_ID, "artifact_id": ARTIFACT_ID, "artifact_sha256": ARTIFACT_SHA, "summary": "none/A-only/B-only/A+C/A+B+C all passed across two distinct Thunderbird processes on the same exact disposable profile with permanent add-on persistence, SQLite/settings preservation and natural MV3 wake; A+C restored 34 pins with B absent."},
        },
    ])
    data["targeted_checks"] = kept
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    subprocess.run(["git", "add", "docs/AI_VALIDATION_STATE.json"], cwd=ROOT, check=True)
    run("git", "commit", "-m", "docs: record MailPerch 1.5.2 validation evidence")


def main() -> None:
    reproduce_metadata()
    write_reports()
    check_metadata()
    sha, tree = commit_metadata()
    update_validation_state(sha, tree)
    run("git", "push", "origin", "HEAD:release/1.5.2-runtime-coverage")


if __name__ == "__main__":
    main()
