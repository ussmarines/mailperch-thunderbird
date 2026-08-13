# Audit de sécurité — MailPin 1.7.0 (source)

## État

Audit global de la ligne source 1.7.0. Dernière release publique : 1.6.1. Ce document décrit la source en cours de validation et ne constitue pas une publication.

## Périmètre contrôlé

- manifeste MV3, permission `menus` et CSP `connect-src none` ;
- absence de réseau runtime, télémétrie, publicité, CDN et code distant ;
- API Experiment, validation/normalisation des entrées et frontières `PinCompatibility` ;
- SQLite, imports/restauration, règles, Agenda, Tags et cycle de désinstallation ;
- secrets/identité, actions GitHub épinglées, build sans dépendance tierce ;
- revue statique des helpers morts, surfaces DOM dangereuses et identifiants persistants legacy.

## Résultat de l’audit local standard

- `security_guard.py` : vert ;
- `scan_secrets.py` : vert ;
- `deep_audit.py` : vert après nettoyage ;
- aucun `eval`, `new Function`, `innerHTML`, `outerHTML` ou appel réseau runtime détecté dans `extension/` ;
- les clés historiques `mailperch.installation`, `mailperch-*`, préférences legacy et noms de base sont conservés lorsqu’ils assurent compatibilité/migration ;
- deux helpers privilégiés devenus sans appel ont été supprimés.

## Validation finale

Les résultats GitHub Actions/scan standard du commit final seront enregistrés dans ce document avant toute décision de publication. Codex Security n’est pas utilisé par défaut.
