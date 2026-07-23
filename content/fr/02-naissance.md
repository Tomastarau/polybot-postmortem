## Naissance, et le premier pivot

Le 20 avril 2026, le premier commit s'appelle `init: polybot live`. L'idée tient
en une phrase : Polymarket propose des paris sur la température maximale du jour
dans une cinquantaine de villes, les modèles météo publient des prévisions
gratuites, et si les deux divergent, il y a de l'argent à prendre.

Les cinq commits suivants, tous le même jour, disent le reste : `fix: slug date
format`, `fix: edge formulas, rounding, regex`, `fix: handle forecast weather api
NaN return`. Le concept était simple ; le contact avec le réel l'était moins.

La première décision structurante arrive une semaine plus tard. Plutôt que de
continuer à modifier un bot qui joue de l'argent en production pour voir si une
idée fonctionne, j'ai construit un **laboratoire de rejeu** séparé : neuf mois
d'historique de marchés, un moteur qui rejoue les décisions comme si elles étaient
prises à l'époque, et une règle inscrite noir sur blanc dans les notes du projet :

> La calibration doit être construite avec une date de coupure strictement
> antérieure à la période de rejeu.

Sans cette règle, un backtest utilise, pour prédire une journée, des informations
qui n'existaient pas encore ce jour-là. Les résultats sont faux, mais la courbe
de performance reste bonne : rien ne signale l'erreur. On appelle ça une fuite de
données, et c'est la première cause de stratégies qui réussissent en simulation
et échouent en production.

Le graphique ci-dessous montre ce à quoi ressemblent réellement six semaines de
développement.
