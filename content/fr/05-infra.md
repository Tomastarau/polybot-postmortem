## Faire tourner un bot 24 h sur 24

Le bot vivait sur une petite machine louée à Francfort : deux processeurs, deux
gigaoctets de mémoire. Il n'a jamais redémarré tout seul en trois mois.

L'ordonnancement ne repose pas sur un programme qui tourne en boucle, mais sur
**seize minuteurs systemd** qui réveillent des tâches courtes : chercher les
marchés du jour, relever les carnets d'ordres, marquer les positions ouvertes,
réconcilier avec la blockchain, produire un résumé quotidien. Chaque tâche démarre,
fait son travail, et meurt.

Ce choix a une conséquence pratique très concrète : comme chaque exécution relit
sa configuration au démarrage, changer un paramètre ne demande aucun redémarrage
de service. Basculer le bot en mode simulation consiste à éditer une ligne dans un
fichier. La prochaine tâche qui se réveille en tient compte. Un programme en
boucle aurait exigé une gestion de signaux et un rechargement à chaud.

L'autre décision structurante est d'avoir journalisé beaucoup trop. Vingt
gigaoctets de traces pour un bot qui misait deux dollars : chaque décision, chaque
carnet d'ordres, chaque prévision, chaque résolution officielle. Sur le moment,
c'était disproportionné.

C'est pourtant la raison pour laquelle ce site existe. Les analyses qui ont conclu
le projet (l'overfitting du filtre par ville, la démonstration que le taux de
réussite ne valait rien) posent des questions que je ne me posais pas au moment
d'écrire ces journaux. **On ne peut analyser que ce qu'on a pensé à enregistrer.**
Le stockage coûte quelques centimes ; la donnée qu'on n'a pas capturée est perdue
pour toujours.
