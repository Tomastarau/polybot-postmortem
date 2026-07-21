## Le piège de l'overfitting

Le 8 mai, un commit du bot s'appelle `fix: blacklisting cities that lose
regularly`. L'intuition semble imparable : certaines villes ont un climat
instable, les prévisions y sont mauvaises, le bot y perd de l'argent. Il suffit de
ne plus y jouer.

En juin, après les pertes réelles, j'ai voulu formaliser cette idée : un score de
fiabilité glissant par ville, recalculé sur quatorze jours, qui refuserait
automatiquement les villes récemment perdantes. Le design était prêt à être
implémenté.

Deux mois de données ont tranché avant que j'écrive la moindre ligne.

La méthode est celle qui aurait dû être appliquée dès le départ. On coupe
l'historique en deux : mai-juin pour **construire** le filtre, juillet pour le
**tester**. Le filtre est calibré uniquement sur la première moitié, puis appliqué
tel quel à la seconde, sans le moindre réajustement.

Sur les données d'entraînement, le résultat est spectaculaire : le rendement passe
de +0,14 % à **+7,24 %**. Neuf villes écartées, presque toutes les pertes
supprimées, une courbe magnifique.

Sur juillet, le même filtre donne **−0,40 %**. Rien. Moins que rien.

L'explication tient en une phrase : les villes qui perdaient en juin n'étaient pas
des villes structurellement mauvaises, c'étaient des villes qui avaient eu une
météo difficile **en juin**. Le filtre n'avait rien appris sur le monde ; il avait
mémorisé un échantillon. C'est la définition même du surapprentissage, et il est
d'autant plus insidieux ici qu'il confirmait une intuition que j'avais depuis deux
mois.

Un modèle qui vous donne raison sur les données qui l'ont produit ne vous apprend
rien. Il faut lui donner l'occasion d'avoir tort.
