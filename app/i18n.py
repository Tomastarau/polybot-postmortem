"""Bilingual text. Long-form prose lives in content/<lang>/, never in the Python.

Only short labels, chart takeaways and method notes live here.
"""
import pathlib

import streamlit as st

CONTENT = pathlib.Path(__file__).resolve().parent.parent / "content"
LANGUAGES = {"fr": "Français", "en": "English"}
DEFAULT = "fr"

UI = {
    "fr": {
        "nav_language": "Langue",
        "chapters": "Chapitres",
        "previous": "Précédent",
        "next": "Suivant",
        "details": "Voir les données et la méthode",
        "trades": "Trades papier",
        "pnl": "P&L total",
        "win_rate": "Taux de réussite",
        "roi": "ROI sur capital déployé",
        "city": "Ville",
        "decisions": "décisions",
        "commits": "commits",

        "ch1_equity_title": "P&L cumulé, mai à juillet 2026",
        "ch1_equity_takeaway": "Six semaines de hausse, puis un retour au point de départ : "
                               "au total, le bot n'a rien gagné ni rien perdu.",
        "ch1_equity_method": "Chaque point est une décision résolue, mise fixe de 2 $. "
                             "Le gain d'un pari réussi vaut `2 / prix − 2` ; une perte coûte 2 $.",
        "ch1_monthly_title": "P&L par mois",
        "ch1_monthly_takeaway": "Un seul mois positif sur trois, et jamais de quoi payer le serveur.",

        "ch2_title": "Rythme de développement, avril à juin",
        "ch2_takeaway": "52 commits en six semaines, dont la moitié sont des corrections : "
                        "le vrai travail n'était pas la stratégie, c'était de faire tenir la mécanique.",
        "ch2_method": "Chaque commit est classé par son préfixe (`feat`, `fix`, `rm`, `log`). "
                      "Historique figé dans `data/commits.parquet` par `scripts/export_commits.py`.",
        "ch2_feature": "fonctionnalité",
        "ch2_fix": "correction",
        "ch2_removal": "suppression",
        "ch2_logging": "journalisation",
        "ch2_other": "autre",

        "ch3_title": "Pourquoi le bot renonçait à parier",
        "ch3_takeaway": "Sur 48 826 occasions examinées, le bot en a écarté 98 % : "
                        "l'essentiel du travail d'un robot de trading consiste à ne pas trader.",
        "ch3_method": "Chaque ligne de `decisions.parquet` est une occasion évaluée. "
                      "`would_trade` signifie qu'aucun motif de refus ne s'est déclenché. "
                      "Les motifs sont exclusifs : le premier qui se déclenche arrête l'évaluation.",

        "ch4_title": "Erreur de prévision, avant et après correction d'unité",
        "ch4_takeaway": "Les prévisions semblaient absurdes sur les villes américaines — "
                        "54 degrés d'erreur. En réalité on comparait des Celsius à des Fahrenheit.",
        "ch4_method": "Erreur = prévision (°C) − température officielle. Sur les marchés "
                      "en Fahrenheit, la valeur officielle est en °F : la série corrigée "
                      "applique `(°F − 32) × 5/9` avant de comparer.",
        "ch4_raw": "erreur brute",
        "ch4_fixed": "après conversion",

        "ch5_title": "Quand le bot travaillait",
        "ch5_takeaway": "Quatre réveils par jour, toutes les six heures : le bot suivait "
                        "le rythme de publication des modèles météo, pas celui des marchés.",
        "ch5_method": "Heures UTC des décisions journalisées. Les runs de 00, 06, 12 et 18 h "
                      "correspondent aux publications des modèles GFS et ECMWF.",

        "ch6_title": "L'argent réel, du 29 mai au 6 juin",
        "ch6_takeaway": "279 $ engagés, 251 $ récupérés : la seule semaine où de l'argent "
                        "réel a circulé s'est soldée par une perte de 28 $.",
        "ch6_method": "Relevé on-chain. Les achats sortent de la trésorerie, les ventes "
                      "(stop-loss) et les remboursements y rentrent. Compter les ventes "
                      "comme des coûts est l'erreur qui avait produit un premier "
                      "diagnostic à −57 $. Le relevé s'arrête au retour en mode papier : "
                      "quelques remboursements tardifs manquent, la perte réelle est donc "
                      "un peu moindre.",
        "ch6_spent": "Achats",
        "ch6_sold": "Stop-loss",
        "ch6_redeemed": "Remboursements",
        "ch6_net": "Solde",

        "ch7_title": "Le filtre par ville : entraînement contre test",
        "ch7_takeaway": "Le filtre transforme +0,14 % en +7,24 % sur les données qui l'ont "
                        "conçu, et ne donne plus rien le mois suivant. Il n'avait rien "
                        "appris : il avait mémorisé la météo de juin.",
        "ch7_method": "Les villes perdantes de mai-juin (au moins 5 paris) sont blacklistées, "
                      "puis le filtre est appliqué tel quel à juillet, sans réajustement. "
                      "Verrouillé par `test_city_blacklist_is_overfitting`.",
        "ch7_train": "Entraînement (mai-juin)",
        "ch7_test": "Test (juillet)",
        "ch7_baseline": "Sans filtre",
        "ch7_filtered": "Avec le filtre",

        "ch8_title": "Le taux de réussite face au seuil de rentabilité",
        "ch8_takeaway": "Le bot gagnait presque toujours, et presque exactement autant "
                        "qu'il fallait pour ne rien gagner : la barre bleue colle au "
                        "point rouge dans chaque tranche de prix.",
        "ch8_method": "Le seuil de rentabilité est le prix d'entrée moyen de la tranche : "
                      "acheter à 0,88 impose de gagner 88 fois sur 100 pour rentrer dans "
                      "ses frais. Seule la tranche bon marché dégage un écart positif.",
        "ch8_win_rate": "Taux de réussite",
        "ch8_break_even": "Seuil de rentabilité",

        "source": "D'où viennent ces chiffres",
        "source_body": "Tous les nombres de ce site sont calculés à l'exécution depuis les "
                       "fichiers de `data/`, et verrouillés par les tests de `tests/`. "
                       "Aucun chiffre n'est écrit en dur dans le texte.",
    },
    "en": {
        "nav_language": "Language",
        "chapters": "Chapters",
        "previous": "Previous",
        "next": "Next",
        "details": "See the data and method",
        "trades": "Paper trades",
        "pnl": "Total P&L",
        "win_rate": "Win rate",
        "roi": "Return on deployed capital",
        "city": "City",
        "decisions": "decisions",
        "commits": "commits",

        "ch1_equity_title": "Cumulative P&L, May to July 2026",
        "ch1_equity_takeaway": "Six weeks of gains, then a return to the starting point: "
                               "overall the bot neither made nor lost anything.",
        "ch1_equity_method": "Each point is a settled decision, fixed 2 $ stake. A winning "
                             "bet pays `2 / price − 2`; a loss costs 2 $.",
        "ch1_monthly_title": "P&L by month",
        "ch1_monthly_takeaway": "One positive month out of three, and never enough to pay for the server.",

        "ch2_title": "Development rhythm, April to June",
        "ch2_takeaway": "52 commits in six weeks, half of them fixes: the real work was not "
                        "the strategy, it was keeping the machinery standing.",
        "ch2_method": "Commits are classified by prefix (`feat`, `fix`, `rm`, `log`). History "
                      "frozen into `data/commits.parquet` by `scripts/export_commits.py`.",
        "ch2_feature": "feature",
        "ch2_fix": "fix",
        "ch2_removal": "removal",
        "ch2_logging": "logging",
        "ch2_other": "other",

        "ch3_title": "Why the bot declined to bet",
        "ch3_takeaway": "Out of 48,826 opportunities examined, it turned down 98 %: most of a "
                        "trading bot's work is deciding not to trade.",
        "ch3_method": "Each row of `decisions.parquet` is an evaluated opportunity. "
                      "`would_trade` means no rejection reason fired. Reasons are exclusive: "
                      "the first one to trigger ends the evaluation.",

        "ch4_title": "Forecast error, before and after the unit fix",
        "ch4_takeaway": "Forecasts looked absurd on US cities — 54 degrees off. In truth we "
                        "were comparing Celsius against Fahrenheit.",
        "ch4_method": "Error = forecast (°C) − official temperature. On Fahrenheit markets the "
                      "official value is in °F: the corrected series applies `(°F − 32) × 5/9` "
                      "before comparing.",
        "ch4_raw": "raw error",
        "ch4_fixed": "after conversion",

        "ch5_title": "When the bot worked",
        "ch5_takeaway": "Four wake-ups a day, every six hours: the bot followed the weather "
                        "models' publication schedule, not the market's.",
        "ch5_method": "UTC hours of logged decisions. The 00, 06, 12 and 18 h runs match the "
                      "GFS and ECMWF model releases.",

        "ch6_title": "Real money, 29 May to 6 June",
        "ch6_takeaway": "279 $ committed, 251 $ recovered: the only week real money moved "
                        "ended 28 $ down.",
        "ch6_method": "On-chain ledger. Buys leave the treasury; sells (stop-losses) and "
                      "redemptions return to it. Counting sells as costs was the mistake that "
                      "produced a first diagnosis of −57 $. The ledger stops when paper mode "
                      "resumed, so a few late redemptions are missing and the real loss is "
                      "slightly smaller.",
        "ch6_spent": "Buys",
        "ch6_sold": "Stop-losses",
        "ch6_redeemed": "Redemptions",
        "ch6_net": "Net",

        "ch7_title": "The city filter: training versus test",
        "ch7_takeaway": "The filter turns +0.14 % into +7.24 % on the data that designed it, "
                        "and delivers nothing the following month. It had learned nothing: it "
                        "had memorised June's weather.",
        "ch7_method": "Cities that lost money in May-June (at least 5 bets) are blacklisted, "
                      "then the filter is applied untouched to July. Locked by "
                      "`test_city_blacklist_is_overfitting`.",
        "ch7_train": "Training (May-June)",
        "ch7_test": "Test (July)",
        "ch7_baseline": "No filter",
        "ch7_filtered": "With the filter",

        "ch8_title": "Win rate against the break-even line",
        "ch8_takeaway": "The bot won almost always, and almost exactly as often as it needed "
                        "to win nothing: the blue bar sits on the red dot in every price band.",
        "ch8_method": "Break-even is the band's average entry price: paying 0.88 requires "
                      "winning 88 times out of 100 just to break even. Only the cheap band "
                      "opens a positive gap.",
        "ch8_win_rate": "Win rate",
        "ch8_break_even": "Break-even",

        "source": "Where these numbers come from",
        "source_body": "Every figure on this site is computed at runtime from the files in "
                       "`data/`, and locked by the tests in `tests/`. No number is hard-coded "
                       "in the text.",
    },
}


def current():
    return st.session_state.get("lang", DEFAULT)


def t(key):
    return UI[current()][key]


def prose(slug):
    path = CONTENT / current() / f"{slug}.md"
    if not path.exists():
        path = CONTENT / DEFAULT / f"{slug}.md"
    return path.read_text(encoding="utf-8")


def language_selector():
    codes = list(LANGUAGES)
    stored = st.query_params.get("lang")
    if stored in LANGUAGES and "lang" not in st.session_state:
        st.session_state["lang"] = stored

    chosen = st.sidebar.radio(
        UI[current()]["nav_language"],
        codes,
        index=codes.index(current()),
        format_func=lambda code: LANGUAGES[code],
        horizontal=True,
        key="lang",
    )
    st.query_params["lang"] = chosen
    return chosen
