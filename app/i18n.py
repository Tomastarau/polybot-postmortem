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
        "ch1_equity_takeaway": "Le bot monte pendant six semaines, puis redescend. "
                               "Il finit à +1,12 $.",
        "ch1_equity_method": "Chaque point est une décision résolue, mise fixe de 2 $. "
                             "Un pari réussi rapporte `2 / prix − 2`, une perte coûte 2 $.",
        "ch1_monthly_title": "P&L par mois",
        "ch1_monthly_takeaway": "Un mois positif sur trois. Aucun ne couvre les 12 $ "
                                "mensuels du serveur.",

        "ch2_title": "Rythme de développement, avril à juin",
        "ch2_takeaway": "52 commits en six semaines. La moitié sont des corrections.",
        "ch2_method": "Chaque commit est classé par son préfixe (`feat`, `fix`, `rm`, `log`). "
                      "Historique figé dans `data/commits.parquet`.",
        "ch2_feature": "fonctionnalité",
        "ch2_fix": "correction",
        "ch2_removal": "suppression",
        "ch2_logging": "journalisation",
        "ch2_other": "autre",

        "ch3_title": "Pourquoi le bot renonçait à parier",
        "ch3_takeaway": "Le bot a examiné 48 826 occasions et en a écarté 98 %.",
        "ch3_method": "Chaque ligne de `decisions.parquet` est une occasion évaluée. "
                      "`would_trade` signifie qu'aucun motif de refus ne s'est déclenché. "
                      "Les motifs sont exclusifs, le premier qui se déclenche arrête "
                      "l'évaluation.",

        "ch4_title": "Erreur de prévision, avant et après correction d'unité",
        "ch4_takeaway": "Sur les villes américaines, l'erreur de prévision atteignait "
                        "54 degrés. On comparait des Celsius à des Fahrenheit.",
        "ch4_method": "Erreur = prévision (°C) − température officielle. Sur les marchés en "
                      "Fahrenheit, la valeur officielle est en °F. La série corrigée applique "
                      "`(°F − 32) × 5/9` avant de comparer.",
        "ch4_raw": "erreur brute",
        "ch4_fixed": "après conversion",

        "ch5_title": "Quand le bot travaillait",
        "ch5_takeaway": "Le bot se réveillait quatre fois par jour, toutes les six heures, "
                        "au rythme des publications des modèles météo.",
        "ch5_method": "Heures UTC des décisions journalisées. Les runs de 00, 06, 12 et 18 h "
                      "correspondent aux publications des modèles GFS et ECMWF.",

        "ch6_title": "L'argent réel, du 29 mai au 6 juin",
        "ch6_takeaway": "279 $ engagés et 251 $ récupérés sur la seule semaine où de "
                        "l'argent réel a circulé, soit 28 $ de perte.",
        "ch6_method": "Relevé on-chain. Les achats sortent de la trésorerie, les ventes "
                      "(stop-loss) et les remboursements y rentrent. Compter les ventes "
                      "comme des coûts avait produit un premier diagnostic à −57 $. "
                      "Le relevé s'arrête au retour en mode papier, quelques remboursements "
                      "tardifs manquent donc et la perte réelle est un peu moindre.",
        "ch6_spent": "Achats",
        "ch6_sold": "Stop-loss",
        "ch6_redeemed": "Remboursements",
        "ch6_net": "Solde",

        "ch7_title": "Le filtre par ville : entraînement contre test",
        "ch7_takeaway": "Le filtre donne +7,24 % sur mai-juin, les données qui ont servi "
                        "à le construire, et −0,40 % sur juillet.",
        "ch7_method": "Les villes perdantes de mai-juin (au moins 5 paris) sont blacklistées, "
                      "puis le filtre est appliqué tel quel à juillet, sans réajustement. "
                      "Verrouillé par `test_city_blacklist_is_overfitting`.",
        "ch7_train": "Entraînement (mai-juin)",
        "ch7_test": "Test (juillet)",
        "ch7_baseline": "Sans filtre",
        "ch7_filtered": "Avec le filtre",

        "ch8_title": "Le taux de réussite face au seuil de rentabilité",
        "ch8_takeaway": "Dans chaque tranche de prix, la barre bleue rejoint le point rouge. "
                        "Le bot gagnait juste assez souvent pour rentrer dans ses frais.",
        "ch8_method": "Le seuil de rentabilité est le prix d'entrée moyen de la tranche. "
                      "Acheter à 0,88 impose de gagner 88 fois sur 100 pour rentrer dans "
                      "ses frais. Seule la tranche bon marché dégage un écart positif.",
        "ch8_win_rate": "Taux de réussite",
        "ch8_break_even": "Seuil de rentabilité",
        "ch8_null_title": "Le résultat réel face au hasard du marché",
        "ch8_null_takeaway": "On rejoue les 752 paris 10 000 fois en supposant que le prix "
                             "du marché avait raison. Le résultat réel tombe au centre de "
                             "la distribution obtenue.",
        "ch8_null_method": "Chaque pari gagne avec la probabilité que le marché lui donnait, "
                           "soit son prix d'entrée. 10 000 tirages à graine fixe. Le "
                           "percentile du résultat réel est verrouillé par "
                           "`test_pnl_is_indistinguishable_from_the_null_model`.",
        "ch8_observed": "Résultat réel",

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
        "ch1_equity_takeaway": "The bot climbs for six weeks, then falls back. "
                               "It ends at +1.12 $.",
        "ch1_equity_method": "Each point is a settled decision, fixed 2 $ stake. A winning "
                             "bet pays `2 / price − 2`, a loss costs 2 $.",
        "ch1_monthly_title": "P&L by month",
        "ch1_monthly_takeaway": "One positive month out of three. None covers the 12 $ "
                                "monthly server bill.",

        "ch2_title": "Development rhythm, April to June",
        "ch2_takeaway": "52 commits in six weeks. Half of them are fixes.",
        "ch2_method": "Commits are classified by prefix (`feat`, `fix`, `rm`, `log`). History "
                      "frozen into `data/commits.parquet`.",
        "ch2_feature": "feature",
        "ch2_fix": "fix",
        "ch2_removal": "removal",
        "ch2_logging": "logging",
        "ch2_other": "other",

        "ch3_title": "Why the bot declined to bet",
        "ch3_takeaway": "The bot examined 48,826 opportunities and turned down 98 %.",
        "ch3_method": "Each row of `decisions.parquet` is an evaluated opportunity. "
                      "`would_trade` means no rejection reason fired. Reasons are exclusive, "
                      "the first one to trigger ends the evaluation.",

        "ch4_title": "Forecast error, before and after the unit fix",
        "ch4_takeaway": "On US cities the forecast error reached 54 degrees. Celsius was "
                        "being compared against Fahrenheit.",
        "ch4_method": "Error = forecast (°C) − official temperature. On Fahrenheit markets the "
                      "official value is in °F. The corrected series applies `(°F − 32) × 5/9` "
                      "before comparing.",
        "ch4_raw": "raw error",
        "ch4_fixed": "after conversion",

        "ch5_title": "When the bot worked",
        "ch5_takeaway": "The bot woke up four times a day, every six hours, following the "
                        "weather models' publication schedule.",
        "ch5_method": "UTC hours of logged decisions. The 00, 06, 12 and 18 h runs match the "
                      "GFS and ECMWF model releases.",

        "ch6_title": "Real money, 29 May to 6 June",
        "ch6_takeaway": "279 $ committed and 251 $ recovered over the only week real money "
                        "moved, so 28 $ lost.",
        "ch6_method": "On-chain ledger. Buys leave the treasury, sells (stop-losses) and "
                      "redemptions return to it. Counting sells as costs had produced a first "
                      "diagnosis of −57 $. The ledger stops when paper mode resumed, so a few "
                      "late redemptions are missing and the real loss is slightly smaller.",
        "ch6_spent": "Buys",
        "ch6_sold": "Stop-losses",
        "ch6_redeemed": "Redemptions",
        "ch6_net": "Net",

        "ch7_title": "The city filter: training versus test",
        "ch7_takeaway": "The filter returns +7.24 % on May-June, the data used to build it, "
                        "and −0.40 % on July.",
        "ch7_method": "Cities that lost money in May-June (at least 5 bets) are blacklisted, "
                      "then the filter is applied untouched to July. Locked by "
                      "`test_city_blacklist_is_overfitting`.",
        "ch7_train": "Training (May-June)",
        "ch7_test": "Test (July)",
        "ch7_baseline": "No filter",
        "ch7_filtered": "With the filter",

        "ch8_title": "Win rate against the break-even line",
        "ch8_takeaway": "In every price band the blue bar meets the red dot. The bot won just "
                        "often enough to break even.",
        "ch8_method": "Break-even is the band's average entry price. Paying 0.88 requires "
                      "winning 88 times out of 100 just to break even. Only the cheap band "
                      "opens a positive gap.",
        "ch8_win_rate": "Win rate",
        "ch8_break_even": "Break-even",
        "ch8_null_title": "The real result against market chance",
        "ch8_null_takeaway": "The 752 bets are replayed 10,000 times assuming the market "
                             "price was right. The real result lands in the middle of the "
                             "resulting distribution.",
        "ch8_null_method": "Each bet wins with the probability the market gave it, which is "
                           "its entry price. 10,000 draws at a fixed seed. The percentile of "
                           "the real result is locked by "
                           "`test_pnl_is_indistinguishable_from_the_null_model`.",
        "ch8_observed": "Real result",

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
