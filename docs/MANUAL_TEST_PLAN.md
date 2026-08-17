# Plan de test manuel MailPin — 1.7.2

Utiliser de préférence un profil Thunderbird jetable avec des messages synthétiques pour les scénarios destructifs ou de migration. Pour une validation utilisateur finale, un profil réel peut être utilisé après sauvegarde, en évitant toute opération destructive non nécessaire.

Le présent plan complète les validations automatisées de la source 1.7.2. La dernière release publique est 1.7.1. La 1.7.2 modifie des surfaces UI Dashboard/Options : une recette humaine post-correction est donc recommandée en plus du smoke Thunderbird automatisé. Aucun contrôle non exécuté ne doit être présenté comme PASS.

## Priorité A — corrections UI/navigation 1.7.2

1. **Dashboard / Plus de statistiques** : ouvrir/fermer plusieurs fois le contrôle ; il doit être clairement identifiable, rester au même emplacement et afficher les statistiques supplémentaires dessous sans saut latéral.
2. **Navigation Options** : cliquer successivement sur Bien démarrer, Agenda, Raccourci clavier, Règles et actions automatiques, Groupes/affaires/modèles, Compatibilité, Centre de santé, Sauvegarde ; la rubrique active doit toujours correspondre à la section réellement affichée.
3. **Scroll long** : faire défiler manuellement plusieurs longues sections puis remonter ; le rail doit suivre la section visible sans conserver une ancienne rubrique active.
4. **Enregistrer/Annuler** : modifier un réglage au milieu puis en bas de page ; la barre doit rester visible dans le viewport, sans pousser ni redimensionner l’en-tête. Tester Enregistrer puis Annuler sur un nouveau brouillon.
5. **Notifications** : déclencher une confirmation et, si possible dans un profil jetable, une erreur contrôlée ; le feedback doit rester visible près de la position courante.
6. **Espacement** : contrôler Rappels, Règles, Centre de santé et Sauvegarde à 100/125/200 % ; aucun groupe de cartes/champs ne doit sembler collé au groupe voisin ni créer de scroll horizontal.
7. **Agenda** : avec des calendriers aux noms courts et longs, vérifier que les badges de capacité ne chevauchent jamais le nom et restent lisibles sur une fenêtre réduite.
8. **Raccourcis** : vérifier que l’action « Enregistrer le raccourci » est visuellement distincte de la dernière ligne de saisie et reste accessible au clavier.
9. Répéter les points principaux en thème clair/sombre, largeur réduite et `prefers-reduced-motion` si disponible.

## Priorité B — invariants métier autour des surfaces modifiées

1. Épingler/désépingler depuis ligne native, menu contextuel, message affiché et carte épinglée.
2. Vérifier qu’un simple épinglage ne change ni état lu/non lu ni compteurs natifs.
3. Ouvrir Modifier sur une carte, changer note/checklist/statut puis vérifier la persistance.
4. Créer un événement Agenda puis, si un calendrier compatible existe, une tâche ; vérifier le calendrier choisi et l’absence de doublon.
5. Fermer/réouvrir Thunderbird et confirmer le retour d’un seul panneau et la conservation des données.

## Priorité C — Options Recommandé/Avancé

1. En mode Recommandé, appliquer les réglages recommandés : le formulaire doit devenir modifié sans sauvegarde automatique.
2. Annuler : les valeurs persistées doivent revenir.
3. Réappliquer puis Enregistrer : fermer/réouvrir Options et vérifier la persistance.
4. Passer en mode Avancé et confirmer que les réglages techniques restent accessibles.
5. Vérifier recherche, navigation clavier, `Ctrl/Cmd+S`, focus visible et absence de section avancée révélée par erreur en mode Recommandé.

## Priorité D — Tags et Agenda

1. Créer un tag personnel avant le test ; activer/désactiver la synchronisation MailPin et confirmer que le tag personnel reste strictement inchangé.
2. Tester un calendrier local inscriptible et, si disponible, un calendrier lecture seule ; l’action incompatible doit être indisponible ou échouer proprement.
3. Refaire les scénarios avec les fournisseurs réels explicitement annoncés avant une soumission ATN générale.

## Priorité E — publication

1. Installer **l’XPI exact produit par la candidate 1.7.2**, pas une build intermédiaire.
2. Vérifier version `1.7.2`, ID `ussmarines.mailpin@addons.thunderbird.net` et compatibilité Thunderbird 153.x.
3. Comparer l’empreinte SHA-256 du XPI testé à celle de l’artefact destiné à la release.
4. Après publication, retélécharger l’asset GitHub et confirmer la même empreinte avant de considérer la release validée.

Les validations automatiques restent : `npm run ci`, QA Linux/Windows, garde sécurité/identité, build reproductible et smoke Thunderbird réel sur le candidat exact.
