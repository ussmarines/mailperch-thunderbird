# Passage de relais Codex — consolidation Thunderbird / Options

Ce fichier décrit uniquement la branche de travail actuelle pour éviter de recharger tout l’historique. Lire dans cet ordre :

1. `docs/IDENTITY_MIGRATION_REQUIRED.md` — identité immuable ;
2. `PROJECT_MEMORY.md` — invariants et carte des fichiers ;
3. ce fichier ;
4. `docs/THUNDERBIRD_COMPATIBILITY.md` si la frontière Thunderbird est inspectée ;
5. `docs/THUNDERBIRD_TEST_BENCH.md` si le banc runtime est inspecté ;
6. uniquement les fichiers modifiés pertinents dans le diff contre `main`.

## Référence Git

- version publique : **1.2.1** ;
- base : `main` = `385815f546968acf721c8cd8486ff48f55f78a32` ;
- branche : `refactor/thunderbird-integration-and-ux` ;
- ne pas fusionner `main` ;
- ne pas créer de tag/release ;
- ne pas modifier le numéro public avant décision de release.

## Objectifs de la branche

1. isoler les API internes Thunderbird derrière une couche Messages / Tags / Agenda ;
2. conserver le comportement produit 1.2.1 ;
3. rendre les Options plus simples avec **Essentiel / Organisation / Automatisation / Avancé** ;
4. présenter `guided` comme mode **Recommandé** sans migration ;
5. ajouter un smoke test qui lance un vrai Thunderbird officiel ;
6. documenter les limites et la reprise.

## Hors périmètre

Ne pas implémenter ici : **Prochaine action**, **Timeline conversation**, **Follow-up récurrent**, **Résultat du suivi**, IA, cloud, comptes MailPerch ou nouvelle synchronisation distante.

## Architecture à préserver

```text
business modules
      │
      ▼
PinCompatibility
 ├─ thunderbird-messages.js
 ├─ thunderbird-tags.js
 └─ thunderbird-calendar.js
      │
      ▼
Thunderbird internal APIs
```

`implementation.js` conserve l’orchestration, le cycle de vie et le DOM `about:3pane`. Ne pas lancer un grand refactoring du DOM dans cette passe.

### Invariants de compatibilité

- pas d’appels métier directs à `MailServices`, `MailUtils`, `MessageArchiver`, `cal`, `CalEvent`, `CalTodo` hors adaptateurs ;
- Tags : vérifier toutes les collisions avant toute création ; ne jamais adopter/supprimer un tag personnel ;
- Agenda/Tags facultatifs : indisponibilité locale, pas panne globale ;
- résolution de messages bornée ;
- listeners/observers enregistrés avec cleanup idempotent ;
- aucune nouvelle permission WebExtension, dépendance runtime, connexion réseau ou migration de stockage.

## Options

Le stockage garde `uxMode = guided|advanced`. L’interface affiche **Recommandé** pour `guided`.

Le mode Recommandé masque les sections marquées avancées mais ne supprime aucun contrôle. L’action d’application des recommandations :

- charge la configuration réelle ;
- applique un brouillon sûr ;
- conserve calendrier préféré, groupe d’attente, dossier de sauvegarde, couleurs de comptes et activation des boîtes ;
- marque le formulaire modifié ;
- **ne sauvegarde pas** ;
- laisse Enregistrer/Annuler décider du résultat.

## Banc Thunderbird

- workflow : `.github/workflows/thunderbird-smoke.yml` ;
- runner : `tests/thunderbird/real_smoke.py` ;
- garde statique : `tests/test_thunderbird_test_bench.py` ;
- binaire ciblé actuellement : Thunderbird `153.0.1esr` ;
- geckodriver : `0.37.1` ;
- téléchargements test uniquement, SHA-256 vérifiés ;
- le smoke installe/désinstalle/réinstalle l’XPI et contrôle l’injection/cleanup du panneau.

Ne jamais déduire qu’il est compatible avec toutes les versions/fournisseurs à partir d’un seul smoke Linux.

## Tests ciblés déjà prévus

```bash
python tests/test_thunderbird_compatibility_boundary.py
node tests/thunderbird_compatibility_contract.mjs
python tests/test_recommended_options_ux.py
python tests/test_thunderbird_test_bench.py
```

La validation complète de branche reste :

```bash
npm run ci
```

Ne relancer une suite coûteuse en boucle que si ses fichiers/dépendances ont changé ou si une correction peut l’affecter. Après une correction finale, une seule passe complète est attendue.

## Surface à examiner en priorité lors de la revue Codex

1. diff `main...refactor/thunderbird-integration-and-ux` ;
2. contrats des trois adaptateurs et appels de `implementation.js` ;
3. cleanup des listeners/observers et comportement de capacité manquante ;
4. atomicité/propriété des tags ;
5. Options : masquage, recherche/navigation, brouillon Recommandé, save/cancel ;
6. workflow runtime : chaîne de confiance, absence de secret, checksums, timeouts, logs ;
7. documentation et cohérence des assertions.

## Ce qu’une revue ne doit pas faire

- refaire un audit historique exhaustif des anciennes builds 3.2.x sans indice lié au diff ;
- remplacer les adaptateurs par un abstrait générique sans besoin concret ;
- assouplir un test simplement pour obtenir du vert ;
- ajouter Selenium/npm packages pour le smoke si la bibliothèque standard suffit ;
- modifier `main`, taguer ou publier ;
- supprimer les tests historiques de zones inchangées uniquement pour raccourcir la CI.

## Rapport attendu de Codex

À la fin, fournir :

- constat du diff revu ;
- bugs/régressions trouvés et corrections exactes ;
- tests réellement exécutés et résultats ;
- limites qui nécessitent encore Thunderbird réel ;
- `git status --short --branch` ;
- dernier commit ;
- confirmation explicite : aucun push `main`, aucun tag, aucune release.

Le prompt précis sera fourni séparément après choix des outils/skills Codex disponibles.
