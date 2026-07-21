## Le verdict

Sur 752 paris papier, le bot a gagné 1,12 dollar. Le taux de réussite est de
88,3 %, et il ne veut rien dire.

Voici pourquoi, et c'est le seul raisonnement à retenir de ce site. Sur ces
marchés, un pari coûte son prix et rapporte toujours 1,00 dollar s'il est gagné.
Payer 0,88 pour gagner 1,00, c'est risquer 0,88 pour empocher 0,12. Pour rentrer
dans ses frais, il faut donc gagner **88 fois sur 100**. Le taux de réussite n'est
pas une performance : c'est le prix affiché, retranscrit en pourcentage. Gagner
88 % du temps en payant 0,88, c'est faire exactement zéro.

Le graphique ci-dessous superpose les deux. Dans chaque tranche de prix, la barre
bleue (ce que le bot a réussi) se pose sur le point rouge (ce qu'il fallait
réussir). Un seul endroit dégage un écart : les paris achetés entre 0,70 et 0,85,
soit +4,4 % de rendement sur 175 paris. C'est la seule piste que ces trois mois
ont produite, et elle reste fragile — sur la moitié d'entraînement elle ne
rapporte que +1,45 %, ce qui est indistinguable du hasard.

Restait l'arithmétique finale, et elle n'a rien de sophistiqué. Le serveur coûtait
12 dollars par mois. La meilleure estimation de gain, en supposant que la piste
ci-dessus soit réelle, tournait autour de 9 dollars par mois. Le capital
disponible était de 36 dollars.

Un edge s'exprime en pourcentage ; un serveur se paie en euros. Tant que le
capital reste petit, tout coût fixe domine l'équation — et aucun raffinement de
stratégie ne rattrape un dénominateur de 36 dollars.

Alors j'ai arrêté le bot, supprimé l'infrastructure, et publié les données. Ce
site est ce qu'il reste : 1,27 million de décisions, réduites à 5,3 mégaoctets, et
une conclusion négative mais solide. C'était, de loin, le meilleur rendement du
projet.
