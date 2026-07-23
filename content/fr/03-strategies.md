## La chasse à la stratégie

Le mois de mai est une succession d'idées essayées puis abandonnées.

La première s'appelle le **scanner de rendement**. Elle part d'un constat : sur ces
marchés, certains paris sont pratiquement joués d'avance. Quand il est 20 h et que
la température maximale du jour est déjà connue, parier « non, il ne fera pas
9 °C » est une constatation. Le pari se paie 0,97 et
rapporte 1,00 : 3 % en quelques heures, presque sans risque. Les toutes premières
traces du bot, le 3 mai, sont 1 322 marchés scannés selon cette logique.

Le problème de l'argent gratuit, c'est que tout le monde le voit. Les 3 % étaient
déjà pris quand le bot arrivait, et la stratégie « observée » a fini par ne plus
jamais trader : sur ses derniers jours d'activité, elle a refusé 1 510 paris
d'affilée pour cause de *prix trop élevé*.

D'où le pivot du 12 mai, résumé par un commit sans ambiguïté : `rm: everything but
D0 yield`. Tout le reste est supprimé. Le bot ne garde qu'une stratégie : parier
**avant** que la température soit connue, sur la base des prévisions, contre les
tranches de température que les modèles jugent improbables. On passe de la
constatation au pari, et donc du risque nul au vrai risque.

Ce que le graphique ci-dessous montre, c'est la conséquence directe de ce choix :
un bot qui passe l'écrasante majorité de son temps à refuser de jouer.
