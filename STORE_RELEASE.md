# Publication de MailPerch 1.5.3

## Identité

- **Nom :** MailPerch
- **Nom complet :** MailPerch — Email Pins & Follow-up
- **Version publique :** 1.5.3
- **Sous-titre FR :** Épinglez, organisez et suivez vos e-mails dans Thunderbird.
- **Subtitle EN:** Pin, organize and follow up on your emails in Thunderbird.
- **Auteur public :** ussmarines
- **Identifiant permanent :** `pin-mails@MailPerch.local`
- **Compatibilité déclarée :** Thunderbird 153.0 à 153.*
- **Licence :** MailPerch Source-Available License 1.1

L’identifiant propre au produit doit conserver exactement la même casse et ne plus être modifié après signature ou publication.

## État de préparation

La version 1.5.3 conserve le fonctionnement local et les permissions de 1.5.2. Elle rend inertes les automatismes restaurés par import jusqu’à leur validation explicite, fait respecter `safeMode` avant la rétention et corrige un chevauchement dans les Options. Elle n’ajoute ni fonctionnalité métier, ni permission, ni dépendance runtime, ni connexion réseau. Les contrôles automatisés du dépôt couvrent la syntaxe, les ressources, les permissions, la CSP, l’absence de réseau, les contrats API, les migrations, les compteurs natifs, l’accessibilité, les modèles JavaScript/SQLite, le scan de secrets et le packaging.

Le banc fonctionnel réel a validé 50, 100, 500, 1 000 et 2 000 épingles. La portée multi-comptes a été validée avec vide=0, A=18, B=16, A+C=34 et A+B+C=50 ; la persistance sur le même profil entre deux processus, la sauvegarde Options → panneau et les thèmes clair/sombre sont couvertes par le banc Thunderbird.

La soumission Add-ons for Thunderbird reste une action manuelle : seul le portail ATN et ses reviewers peuvent valider ou refuser la publication. Avant l’envoi, le propriétaire doit terminer les cases manuelles de `docs/ATN_RELEASE_CHECKLIST.md`, confirmer que support et politique de confidentialité sont accessibles publiquement, puis tester le XPI dans les versions et systèmes annoncés.

## Fichiers à soumettre

Après `npm run ci` :

- `dist/MailPerch_v1.5.3.xpi` — extension à téléverser ;
- `dist/MailPerch_GitHub_Repository_v1.5.3.zip` — sources complètes pour review ;
- `dist/SHA256SUMS.txt` — empreintes des deux archives ;
- `release/ATN_REVIEW_NOTES_TEMPLATE.md` — informations de test et justification de l’Experiment ;
- `release/BUILD_INSTRUCTIONS.md` — reproduction exacte du build.

## Informations de fiche ATN

### Description courte FR

Épinglez, organisez et suivez vos e-mails importants dans Thunderbird avec portée par comptes, notes, sous-tâches, rappels, vues, Agenda et tableau de bord local.

### Short description EN

Pin, organize, and follow up on important email in Thunderbird with account scoping, notes, subtasks, reminders, saved views, Calendar integration, and a local dashboard.

### Confidentialité

MailPerch ne transmet aucune donnée. Aucun corps complet de message ni contenu de pièce jointe n’est copié dans sa base. Voir `PRIVACY.md`.

### Permission privilégiée

L’API Experiment `pinInbox` est nécessaire pour intégrer le panneau dans `about:3pane`, résoudre les messages déplacés, utiliser SQLite, écouter les changements de dossiers, gérer les tags MailPerch et créer/synchroniser des tâches ou événements Agenda. Cette API explique l’avertissement d’accès complet affiché par Thunderbird.

## Blocages externes restants

- validation manuelle complète Windows, Linux et macOS sur les versions Thunderbird réellement annoncées ;
- validation des fournisseurs/comptes réels restant au plan ATN ;
- création/accès au compte développeur et soumission dans le portail Add-ons for Thunderbird ;
- décision finale des reviewers ATN.
