# Rapport de validation — MailPerch 1.5.1

> État pendant préparation : **EN COURS — ne pas utiliser comme preuve de publication avant les contrôles finaux**.

## Changements validés localement à ce stade

- correction de la portée checklist de l’éditeur ;
- extraction des opérations Messages restantes vers `PinCompatibility.messages` ;
- propagation de `server.isSecure` et `offlineSupportLevel` dans les métadonnées de diagnostic ;
- migration Settings basée sur `PinSettings.SCHEMA_VERSION` ;
- smoke GitHub rattaché à `main` ;
- déclarations 1.5.1 et documents actifs resynchronisés.

## Tests réellement exécutés

### Base 1.5.0 avant correction

`npm run ci` a été exécuté sur le snapshot source de 1.5.0 et était vert. Cette preuve a démontré que la suite précédente ne détectait pas le crash `checklistItems` observé dans Thunderbird.

### Après corrections runtime ciblées

Ont été exécutés avec succès :

- `python tests/test_calendar_and_card_actions.py` ;
- `python tests/test_thunderbird_compatibility_boundary.py` ;
- `node tests/thunderbird_compatibility_contract.mjs` ;
- `node tests/productivity_1_2_model_tests.mjs` ;
- `python tests/test_productivity_1_2_features.py` ;
- `node tests/settings_defaults.mjs` ;
- inventaire exhaustif fichier-par-fichier : 0 erreur, 0 avertissement après les premières corrections.

Une exécution de `npm test` après passage en 1.5.1 a validé toutes les suites jusqu’au test de packaging, lequel s’est arrêté uniquement parce que les nouveaux rapports `SECURITY_AUDIT_1.5.1.md` et `VALIDATION_REPORT_1.5.1.md` n’existaient pas encore. Aucun test runtime/code antérieur dans cette séquence n’a échoué.

## Contrôles finaux encore obligatoires

- `npm run ci` complet avec les rapports présents et finalisés ;
- seconde passe exhaustive indépendante sur tous les fichiers ;
- audit sécurité standard complet sur l’arbre final ;
- smoke Thunderbird réel ;
- banc Thunderbird fonctionnel/charge réel 50/100/500/1000/2000 ;
- CI GitHub Linux/Windows et checks de PR ;
- build release et vérification des SHA-256 ;
- fusion, tag et workflow Release.

La version finale de ce rapport doit contenir uniquement les preuves réellement obtenues et les limites restantes.
