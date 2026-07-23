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

Sur les données d'entraînement, le rendement passe de +0,14 % à **+7,24 %**. Neuf
villes écartées, presque toutes les pertes supprimées.

Sur juillet, le même filtre donne **−0,40 %**.

L'explication est simple : les villes qui perdaient en juin avaient eu une météo
difficile **en juin**. Le filtre avait mémorisé la météo de juin. C'est la
définition même du surapprentissage, et il est d'autant plus insidieux ici qu'il
confirmait une intuition que j'avais depuis deux mois.

Un test qui ne peut pas échouer ne prouve rien : il faut évaluer une stratégie
sur des données qui n'ont pas servi à la construire.
