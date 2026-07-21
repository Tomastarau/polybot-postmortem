## L'argent réel, puis le crash

Le 19 mai, le bot passe en production réelle. Deux commits accompagnent le
basculement : la migration vers la version 2 du client Polymarket, puis
`fix: Polymarket order placement bugs (min_order_size + tick_size)` — les ordres
étaient rejetés parce qu'ils ne respectaient ni la taille minimale ni le pas de
cotation du carnet.

Suivent onze jours de trading réel, puis l'arrêt. Le 6 juin, le bot repasse en
mode simulation. Le portefeuille est tombé à 36 dollars.

Le diagnostic a d'abord été faux. En additionnant toutes les lignes du relevé
on-chain, j'obtenais une perte de 57 dollars. Le vrai chiffre était deux fois plus
petit : je comptais comme des dépenses les **ventes de stop-loss**, qui sont
précisément l'inverse — de l'argent qui rentre quand on coupe une position. Le
relevé contient trois types d'événements (achat, vente, remboursement) et j'en
traitais deux comme un seul.

Une fois le calcul correct, le vrai problème apparaît, et il n'est pas dans le
taux de réussite : **l'asymétrie**. Un pari gagné rapporte en moyenne 0,68 dollar.
Un pari perdu en coûte 4,27. Il faut donc gagner six fois pour absorber un échec.
Avec 88 % de réussite, on gagne environ sept fois pour un échec. La marge tient sur
un cheveu, et une mauvaise journée la consomme entièrement.

Augmenter le volume n'y change rien — c'est même exactement le piège. Multiplier
les paris multiplie proportionnellement les deux côtés de la balance. Quand la
structure des gains est asymétrique, seule la **sélection** peut aider : parier
moins souvent, mais mieux. C'est ce que le chapitre suivant essaie de faire, et
c'est là que ça devient intéressant.
