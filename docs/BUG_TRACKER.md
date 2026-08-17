# Registre des bugs MailPin

Version source : **1.7.3**

Dernière release publique : **1.7.2**

Les détails historiques complets restent dans Git et les audits archivés. Ce registre courant conserve les éléments encore actionnables et les dernières corrections.

## Bugs ouverts

| ID | Introduit | Symptôme | Cause | Fichiers | Test | Statut | Correction | Validation |
|---|---|---|---|---|---|---|---|---|
| MP-2026-018 | 1.1.1 | L’empreinte binaire du ZIP peut différer entre Windows et Linux malgré des contenus extraits identiques. | Différences de conteneur ZIP entre plateformes. | `scripts/build.py`, tests de reproductibilité | `tests/test_build_reproducible.py` | À VALIDER | — | Comparer les artefacts inter-plateformes et leur contenu extrait. |

## Bugs corrigés ou en validation

| ID | Introduit | Symptôme | Cause | Fichiers | Test | Statut | Correction | Validation |
|---|---|---|---|---|---|---|---|---|
| MP-2026-058 | 1.7.2 | Plusieurs groupes de réglages restaient trop proches et le bouton Annuler était peu lisible en thème sombre ; les corrections 1.7.2 vivaient dans une feuille CSS ajoutée par-dessus le style canonique. | Le rythme vertical ne couvrait pas toutes les structures imbriquées et le save dock héritait d’un contraste inadapté ; `interaction-stability.css` était chargé dynamiquement. | `extension/styles/workspace.css`, `extension/styles/theme.js`, `tests/test_organic_workspace_ui.py` | contrats UI, QA, smoke Thunderbird réel | CORRIGÉ | 1.7.3 | PR #49 : overlay supprimé, règles intégrées en dur ; QA `32027919000` PASS et smoke `32027918991` PASS avant squash `ed54686f64626c37d5d38236ebcda8ec8e94a094`. |
| MP-2026-056 | 1.7.1 | Navigation Options, statistiques, save dock, notifications et cartes Agenda pouvaient sauter ou se chevaucher. | Composition et suivi de navigation insuffisamment stables. | Dashboard/Options/styles | `tests/test_organic_workspace_ui.py`, QA, smoke | CORRIGÉ | 1.7.2 | QA et smoke réels de la candidate 1.7.2 PASS avant publication. |
| MP-2026-055 | 1.7.1 | `npm run ci` échouait depuis l’archive reviewer sans `.git`. | `security_guard.py` dépendait inconditionnellement de `git ls-files`. | garde sécurité/build reviewer | tests reviewer hors Git | CORRIGÉ | 1.7.1 | Fallback borné `.mailpin-source-files.json` validé hors Git. |

## Procédure

1. Reproduire et documenter le symptôme.
2. Corriger la cause et ajouter une garde ciblée.
3. Relancer d’abord le contrôle en échec puis uniquement les validations invalidées.
4. Exécuter `npm run ci` au jalon final lorsque nécessaire.
5. Garder `À VALIDER` tant qu’une preuve réelle requise manque.
