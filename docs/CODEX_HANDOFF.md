# Passage de relais Codex — audit pré-store MailPerch 1.5.3

## Référence

- source de vérité : `main` au commit `afff4b6338f19c45e6c949d1d4628fcd58373ebc` ;
- branche de travail : `audit/pre-store-release-1.5.3` ;
- version auditée : **1.5.3** ;
- identifiant canonique : `pin-mails@MailPerch.local` ;
- publication GitHub `v1.5.3` déjà disponible ; soumission ATN non effectuée.

## Objet de la passe

- auditer le produit livré, l’Experiment privilégié, le stockage, le cycle de vie, les interfaces et le dossier store ;
- synchroniser les documents actifs de soumission avec 1.5.3 ;
- produire uniquement des preuves réellement exécutées ou vérifiées ;
- conserver comme limites explicites les fournisseurs externes, la matrice multi-OS et les aides techniques humaines non disponibles.

Aucune fonction métier, permission WebExtension, dépendance runtime, migration, connexion réseau ou donnée produit n’est ajoutée par cette passe.

## Sources de preuve

- `VALIDATION_REPORT_1.5.3.md` et `SECURITY_AUDIT_1.5.3.md` pour le delta publié ;
- `docs/AI_VALIDATION_STATE.json` pour les dernières preuves réutilisables ;
- `docs/ATN_RELEASE_CHECKLIST.md` et `docs/MANUAL_TEST_PLAN.md` pour les limites et actions humaines restantes ;
- `STORE_RELEASE.md` et `release/` pour le dossier reviewer.
