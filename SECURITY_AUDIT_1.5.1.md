# Audit de sécurité — MailPerch 1.5.1

> État pendant préparation : **EN COURS — ne pas utiliser comme preuve de publication avant la passe finale GitHub**.
> Base auditée : `main` 1.5.0 au commit `c87a46de4141e09f2e0b29c0ec6996b2693fc2b1`, puis corrections 1.5.1 sur branche dédiée.

## Périmètre

La passe couvre l’intégralité des fichiers suivis, l’historique Git disponible dans GitHub Actions, le runtime WebExtension/Experiment, les adaptateurs Thunderbird, le stockage, les imports/restaurations, la désinstallation, les workflows, les scripts de build, les tests, les documents et les fichiers de publication.

Codex Security n’a pas été utilisé. Les contrôles sont réalisés avec les outils standards du dépôt et des scanners de sécurité vérifiés.

## Contrôles réellement exécutés à ce stade

- inventaire exhaustif de tous les fichiers suivis, lecture binaire répétée et comparaison SHA-256 ;
- validation syntaxique/structurelle JSON, YAML, TOML, Python, JavaScript, SVG et PNG ;
- contrôle des liens Markdown locaux, ressources HTML/CSS/manifeste, modules Experiment et locales FR/EN ;
- recherche de primitives dangereuses, réseau runtime, secrets/fichiers sensibles et artefacts générés suivis ;
- garde d’identité sur tout l’historique Git ;
- Gitleaks 8.30.1 sur tout l’historique ;
- Opengrep 1.22.0 avec les règles projet ;
- Trivy 0.70.0 vulnérabilités/mauvaises configurations et SBOM CycloneDX ;
- zizmor 1.26.1 hors ligne sur les workflows GitHub Actions.

La première exécution complète des scanners standards a produit : **0 fuite Gitleaks, 0 finding Opengrep, 0 vulnérabilité/mauvaise configuration Trivy, 0 finding zizmor et 0 anomalie de garde d’identité**. Une nouvelle exécution sur l’arbre final est obligatoire avant publication et sera consignée dans la version finale de ce rapport.

## Défauts détectés et corrigés pendant l’audit

1. Éditeur de carte : état `checklistItems` et fonction `renderChecklist` hors portée de `openEditor()`, provoquant un `ReferenceError` strict-mode.
2. Frontière Messages : plusieurs énumérations, accès `msgDatabase` et mutations de messages restaient dans `implementation.js` malgré le contrat `PinCompatibility`.
3. Diagnostic fournisseur : l’état TLS réel du serveur n’était pas transmis à la matrice expurgée, ce qui pouvait produire `secure: false` par défaut.
4. Migration Settings : une affectation legacy restait figée à 7 alors que le schéma Settings courant est 8.
5. Workflow runtime : le déclenchement push du smoke ciblait encore une ancienne branche fusionnée.
6. Documentation/release : plusieurs sources actives décrivaient encore des versions, branches, schémas ou rapports devenus obsolètes.

## Invariants préservés

- identifiant `pin-mails@MailPerch.local` inchangé ;
- permission WebExtension `menus` uniquement ;
- CSP avec `connect-src 'none'` ;
- aucune dépendance runtime ajoutée ;
- aucun code distant, télémétrie, publicité ou CDN ;
- aucun stockage de corps complet de message ou contenu de pièce jointe ;
- SQLite physique 5, Settings 8, Data 7 ;
- mutations Messages ramenées derrière l’adaptateur privilégié ;
- balayages nouvellement extraits bornés à 100 000 en-têtes maximum par appel d’adaptateur.

## Preuve finale requise

Avant le tag 1.5.1 : relancer l’audit de sécurité standard complet sur le SHA final de la branche, vérifier les artefacts JSON expurgés, puis exécuter la CI et les tests Thunderbird réels. Le statut ci-dessus doit alors être remplacé par le résultat final observé.
