## Trois mois, un bot, et un résultat nul

Entre le 20 avril et le 20 juillet 2026, un programme a parié tout seul sur la
température maximale de 48 villes. Il lisait sept sources météo, comparait leurs
prévisions au prix des paris sur Polymarket, et achetait quand il estimait le
marché trop cher. Il tournait sur un petit serveur à Francfort, réveillé toutes
les cinq minutes par des timers systemd, et il a produit 1,27 million de lignes
de journal.

Ce site raconte ce qu'il a fait, et pourquoi je l'ai éteint.

La réponse courte est ci-dessous : sur 752 paris, il a gagné **1,12 dollar**.
Pas 1 120 — un dollar et douze cents, pour 1 504 dollars engagés. Un rendement
de 0,07 %, soit à peu près exactement zéro.

Le plus intéressant n'est pas ce chiffre, c'est le taux de réussite qui
l'accompagne : **88 % des paris ont été gagnants**. Un chiffre qu'on afficherait
volontiers sur une plaquette commerciale, et qui ne vaut pourtant rien ici — parce
que le bot achetait à 88 cents ce qui rapporte un dollar. Gagner 88 fois sur 100
était précisément le seuil de rentabilité. Toute la suite de cette histoire
consiste à comprendre ça, à essayer de le dépasser, et à échouer honnêtement.
