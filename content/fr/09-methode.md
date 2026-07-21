## Données et méthode

Ce site ne contient aucun chiffre écrit à la main. Tout est recalculé au
chargement depuis quatre fichiers Parquet publiés dans le dépôt, eux-mêmes
distillés depuis 1,27 million de lignes de journaux bruts.

### Les tables

| Fichier | Lignes | Contenu |
|---|---|---|
| `decisions.parquet` | 48 826 | Chaque occasion évaluée : prévision, désaccord entre modèles, probabilité estimée, prix, motif de refus |
| `market_snapshots.parquet` | 133 559 | L'état du carnet d'ordres au moment de décider |
| `resolutions.parquet` | 2 392 | La température officielle retenue, par ville et par jour |
| `real_trades.parquet` | 127 | Les mouvements on-chain, anonymisés |
| `commits.parquet` | 52 | L'historique git du bot |

### Comment le P&L est reconstruit

Le bot pariait **non** sur une tranche de température. Il gagne si la température
officielle tombe en dehors de la tranche. À mise fixe de 2 dollars, un pari gagné
rapporte `2 / prix − 2`, un pari perdu coûte 2 dollars. On joint chaque décision à
la résolution officielle de sa ville et de sa date, et on somme.

### Réduction et anonymisation

Les résolutions étaient enregistrées toutes les cinq minutes : 822 000 lignes pour
2 392 événements réels. Seul le dernier état de chaque `(ville, date)` est
conservé. Les relevés on-chain sont dépouillés de l'adresse du portefeuille, du
pseudonyme et des hachages de transaction — un test échoue si l'un d'eux
réapparaît.

### Ce qui verrouille les chiffres

Les nombres cités dans le récit sont couverts par des tests qui les recalculent
depuis les données publiées. Si une table change et qu'un chiffre bouge, la suite
de tests casse. C'est délibéré : le texte ne peut pas dériver des données sans que
quelque chose se plaigne.

Le code d'extraction, la conversion et les tests sont dans le dépôt. Tout est
vérifiable sans me faire confiance.
