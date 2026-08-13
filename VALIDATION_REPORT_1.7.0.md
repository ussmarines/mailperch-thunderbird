# Rapport de validation — MailPin 1.7.0 (source)

## État

La source 1.7.0 est la ligne post-Organic Workspace et audit global. Dernière release publique : 1.6.1. Aucun tag/release 1.7.0 n’est créé par ce rapport.

## Contrôles déjà établis

- Organic Workspace intégré via PR #39 ;
- shell Dashboard/Options canonique dans le HTML source ;
- garde Organic Workspace réellement exécuté dans `npm test` ;
- permission, réseau, stockage et identifiant d’extension inchangés ;
- audit de code mort, documents actifs, workflows, tests et métadonnées effectué sur la branche d’audit globale.

## Validation finale attendue

Avant merge/publication : tests ciblés du delta, `npm run ci`, QA Linux/Windows, garde sécurité/full-history, smoke Thunderbird 153 réel et contrôle des artefacts. La recette visuelle humaine du XPI exact reste distincte des preuves automatisées.
