# Passage de relais — MailPin Organic Workspace

## Référence

- dépôt : `ussmarines/mailpin-thunderbird` ;
- branche active : `design/organic-workspace-ui` ;
- base `main` : `497d71e9660c068a166201a4da13fdddc3e65628` ;
- HEAD produit validé : `d763c359894f1726d6d96f85f8f8f72c2e0e9304` ;
- PR : **#39 — design: rebuild MailPin as Organic Workspace** ;
- version distribuée inchangée : **1.6.1** ;
- identifiant canonique inchangé : `ussmarines.mailpin@addons.thunderbird.net`.

## Objectif et état

La branche remplace l’ancienne direction Fluent par **Organic Workspace**. Il ne s’agit pas d’un skin swap : le Dashboard est réorganisé en rail de navigation / canvas / inspector, Options devient un éditeur de réglages persistant, et le panneau Thunderbird devient un compagnon compact. La typographie, la palette, les rayons, la profondeur et la motion ont été redéfinis, sans dépendance distante ni modification de la logique métier.

Le contrat canonique est désormais `docs/UI_SPEC.md`. La direction interdit gradients, glow, glassmorphism, blobs décoratifs et ressources distantes. Les thèmes clair/sombre, `forced-colors`, `prefers-reduced-motion`, le clavier et le zoom 200 % restent des exigences.

## Surfaces modifiées

- design system : `extension/styles/tokens.css`, `extension/styles/workspace.css` ;
- Dashboard : `extension/dashboard/dashboard.html`, `extension/dashboard/dashboard.js` ;
- Options : `extension/options/options.html`, `extension/options/options.js`, `extension/options/AGENTS.md` ;
- panneau Thunderbird : `extension/styles/pin.css` ;
- contrat / marque : `docs/UI_SPEC.md`, `BRANDING.md`, README FR/EN ;
- gardes : `tests/test_organic_workspace_ui.py`, gardes UI/statics/métadonnées associées ;
- métadonnées de dépôt : URLs canoniques synchronisées vers `ussmarines/mailpin-thunderbird`.

Aucun changement de permission, API Experiment, schéma de données, stockage, workflow métier, réseau, télémétrie, dépendance runtime ou ID d’extension.

## Preuves fraîches

Sur le HEAD produit exact `d763c359894f1726d6d96f85f8f8f72c2e0e9304` :

- PR #39 QA run **31692030322** : succès ;
  - Full verification Linux + `npm run ci` + structure XPI : succès ;
  - Source and model checks Windows : succès ;
  - Security guard regression + full-history identity guard : succès ;
  - artefact `development-build` : **9177778752** ;
- PR #39 Thunderbird runtime smoke run **31692030281** : succès ;
  - Thunderbird **153.0.1esr** + geckodriver **0.37.1** ;
  - installation temporaire, injection unique panneau/toggle, ouverture Dashboard, nettoyage désinstallation et réinstallation propre : succès ;
  - artefact `thunderbird-runtime-smoke` : **9177789095** ;
- XPI de développement produit par ces gates : SHA-256 `91276448c21361d32709aefb933924dd5d067c83c1eb60a0fc49a50563fe80d7`.

Avant la PR, le tree produit et la passe de cohérence ont également chacun passé `npm run ci` complet sur la branche.

## Limites de preuve

Le smoke Thunderbird confirme le chargement, l’injection et le cycle de vie réel ; il ne constitue pas à lui seul une validation humaine de la qualité visuelle. Restent à observer manuellement avant toute décision de merge :

- Dashboard aux largeurs desktop / intermédiaire / étroite ;
- Options, recherche, navigation et dock Enregistrer/Annuler ;
- panneau avec resize splitter continu ;
- clair / sombre / contraste élevé ;
- zoom 200 % et réduction du mouvement ;
- ressenti de motion, densité, lisibilité et ergonomie avec données réalistes.

## Git

**Ne pas merger #39 dans `main` sans nouvelle autorisation explicite de l’utilisateur.** La demande courante autorise le travail et les pushs sur la branche dédiée, mais exclut le push/merge sur `main`.

Codex Security n’a pas été utilisé et n’est pas requis par cette refonte.
