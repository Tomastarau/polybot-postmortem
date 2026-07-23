## La météo est un problème de données

Prévoir la température semble être un problème de météorologie. En pratique, c'est
un problème de plomberie.

Le bot a fini par lire sept sources : les modèles ECMWF et GFS pour les prévisions,
puis les observations réelles via les METAR d'aviation, le réseau AMEDAS japonais,
le NWS américain, et Wunderground pour l'historique officiel. Chacune a son format,
son fuseau, sa fréquence et ses trous.

Trois bugs valent d'être racontés, parce qu'ils se ressemblent tous.

**Tokyo ne correspondait pas.** La station météo utilisée pour prévoir n'était pas
celle utilisée pour résoudre le marché. Deux thermomètres distants de quelques
kilomètres, et des paris perdus sans que la prévision soit en cause.

**Le jour d'avant polluait le jour d'après.** Le code lisait `reportTime`, l'heure
à laquelle une observation est publiée, au lieu de `obsTime`, l'heure à laquelle
elle a été mesurée. Une mesure de 23 h 50 publiée à 00 h 10 était comptée dans la
mauvaise journée, et venait fausser le maximum.

**Et surtout, les degrés.** Onze villes américaines résolvent leurs marchés en
Fahrenheit ; les prévisions arrivaient en Celsius. Comparées sans conversion,
elles donnaient une erreur de prévision de 54 degrés, un chiffre si absurde
qu'il aurait dû sauter aux yeux, et qui est resté invisible tant que personne ne
regardait la distribution.

C'est ce que montre le graphique ci-dessous. Une métrique absente, on sait qu'on ne
l'a pas. Une métrique cassée, on la lit, on lui fait confiance, et on prend des
décisions avec.
