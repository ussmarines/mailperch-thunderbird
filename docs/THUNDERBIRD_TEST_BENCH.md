# Banc de test Thunderbird

## But

MailPerch possède plusieurs niveaux de tests. Aucun niveau ne doit être présenté comme une preuve qu’un autre niveau a réussi.

```text
Tests statiques / modèles
          │
          ▼
Contrats de compatibilité avec faux services
          │
          ▼
Smoke runtime sur binaire Thunderbird officiel
          │
          ▼
Tests comm-central xpcshell / Mochitest
          │
          ▼
Validation manuelle avec profils et fournisseurs réels
```

Le smoke runtime ajouté dans cette branche vise un contrôle rapide de l’intégration réelle. Il ne remplace ni la matrice manuelle, ni les suites de tests internes de Thunderbird.

## 1. Tests locaux du dépôt

```bash
npm run check
npm test
npm run build
npm run ci
```

Les contrats spécifiques de la nouvelle frontière sont :

```bash
python tests/test_thunderbird_compatibility_boundary.py
node tests/thunderbird_compatibility_contract.mjs
python tests/test_thunderbird_test_bench.py
```

Ils ne nécessitent pas Thunderbird.

## 2. Smoke runtime GitHub Actions

Workflow : `.github/workflows/thunderbird-smoke.yml`

Script : `tests/thunderbird/real_smoke.py`

Le workflow est volontairement séparé de la QA obligatoire pendant sa phase d’épreuve. Il s’exécute sur la branche de consolidation et peut aussi être lancé manuellement.

Thunderbird documente officiellement `mach`/xpcshell/Mochitest pour ses propres tests. En revanche, la documentation geckodriver est centrée sur Gecko/Firefox et ne garantit pas explicitement ce scénario Thunderbird ; le smoke externe est donc traité comme un harnais expérimental jusqu’à preuve par exécution. En cas d’incompatibilité structurelle, on conserve les contrats et on utilise la voie officielle comm-central plutôt que de masquer l’échec.

### Chaîne de confiance

Le job :

1. construit l’XPI depuis le checkout ;
2. télécharge Thunderbird `153.0.1esr` depuis l’archive officielle Mozilla ;
3. vérifie l’archive avec le `SHA256SUMS` officiel Mozilla ;
4. télécharge geckodriver `0.37.1` depuis la release Mozilla officielle ;
5. vérifie le SHA-256 de l’asset fourni par GitHub ;
6. lance Thunderbird sous Xvfb ;
7. installe temporairement le XPI par l’extension WebDriver Mozilla ;
8. passe au contexte privilégié et contrôle l’état runtime ;
9. désinstalle puis contrôle le nettoyage ;
10. réinstalle et contrôle une nouvelle injection propre ;
11. conserve logs, résultat JSON et captures disponibles comme artefacts.

Aucun de ces téléchargements n’est une dépendance d’exécution de MailPerch. Ils existent uniquement dans l’environnement de test.

### Ce que le smoke valide

Lorsque le job réussit réellement, il démontre au minimum sur la version épinglée :

- lancement du binaire Thunderbird ;
- chargement du XPI et ID exact `pin-mails@MailPerch.local` ;
- extension active ;
- présence d’un `about:3pane` prêt ;
- une seule injection `#pin-mails-panel` ;
- une seule injection `#pin-mails-qfb-toggle` ;
- retrait des injections après désinstallation ;
- réinstallation propre sans duplication.

### Ce qu’il ne valide pas

Il ne prouve pas à lui seul :

- la totalité de la plage Thunderbird 128–153 ;
- Windows ou macOS ;
- IMAP/POP/Gmail/Microsoft réels ;
- les dossiers virtuels réels ;
- Agenda CalDAV/Google/etc. ;
- les réponses réellement reçues/envoyées ;
- le rendu au zoom 200 % ;
- les performances avec des milliers de messages ;
- l’accessibilité avec NVDA/Orca.

Ces points restent dans `docs/MANUAL_TEST_PLAN.md`.

## 3. Tests officiels dans un checkout Thunderbird

Thunderbird documente l’exécution de tests d’extensions dans un checkout `comm-central` construit. Deux familles sont particulièrement adaptées à MailPerch :

```bash
./mach xpcshell-test comm/mail/components/extensions/test/xpcshell
./mach mochitest mail/components/extensions/test/browser
```

Sur Windows, utiliser la forme `./mach` ou la commande recommandée par l’environnement Mozilla Developer Shell du checkout.

Cette voie est la plus adaptée pour tester des interfaces internes et des helpers Thunderbird au plus près du code source, mais elle exige un checkout/build Thunderbird complet ; ce n’est donc pas un prérequis pour développer MailPerch au quotidien.

Références officielles :

- Thunderbird Developer Docs — Running Tests : https://developer.thunderbird.net/thunderbird-development/testing/running-tests
- Thunderbird Developer Docs — Adding Tests : https://developer.thunderbird.net/thunderbird-development/testing/adding-tests
- Thunderbird Developer Docs — Experiments : https://developer.thunderbird.net/add-ons/mailextensions/experiments
- Mozilla geckodriver : https://github.com/mozilla/geckodriver

## 4. Exécution manuelle du smoke

Après avoir construit l’XPI et installé un binaire Thunderbird + geckodriver compatibles :

```bash
python tests/thunderbird/real_smoke.py \
  --thunderbird /chemin/vers/thunderbird \
  --geckodriver /chemin/vers/geckodriver \
  --xpi dist/MailPerch_v1.2.1.xpi \
  --artifacts-dir artifacts/thunderbird-smoke
```

Sur Linux sans écran, lancer la même commande sous `xvfb-run -a`.

Le script utilise uniquement la bibliothèque standard Python ; Selenium n’est pas requis.

## 5. Interprétation d’un échec

Un échec du smoke doit être classé avant correction :

- **download/checksum** : chaîne de test ou archive distante ;
- **session WebDriver** : compatibilité geckodriver/Thunderbird ;
- **installation XPI** : manifeste/Experiment ;
- **absence about:3pane** : démarrage/profil ou changement Thunderbird ;
- **panneau absent/dupliqué** : intégration MailPerch ;
- **cleanup** : cycle de vie/désinstallation ;
- **timeout** : conserver logs/captures avant toute hypothèse.

Ne jamais assouplir une assertion pour rendre le job vert sans expliquer la cause. Si geckodriver cesse de permettre ce type de contrôle, le banc doit échouer clairement et la voie `mach` doit devenir la preuve runtime principale.

## État de preuve de la branche

Le code du banc et ses gardes statiques sont validés localement. Le statut **runtime réel** doit être mis à jour uniquement après exécution du workflow GitHub sur le binaire officiel ; tant que cette exécution n’a pas réussi, ne pas présenter le smoke comme une validation Thunderbird acquise.
