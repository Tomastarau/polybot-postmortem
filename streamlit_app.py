import pathlib
import sys

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from app import i18n  # noqa: E402

st.set_page_config(
    page_title="Polybot — post-mortem",
    page_icon="🌡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

i18n.language_selector()

CHAPTERS = [
    ("app/chapters/ch01_summary.py",
     {"fr": "1 · Le résumé", "en": "1 · The summary"}),
    ("app/chapters/ch02_birth.py",
     {"fr": "2 · Naissance et pivot", "en": "2 · Birth and pivot"}),
    ("app/chapters/ch03_strategies.py",
     {"fr": "3 · La chasse à la stratégie", "en": "3 · Hunting for a strategy"}),
    ("app/chapters/ch04_weather.py",
     {"fr": "4 · La météo, un problème de données", "en": "4 · Weather is a data problem"}),
    ("app/chapters/ch05_infra.py",
     {"fr": "5 · Opérer 24 h sur 24", "en": "5 · Running around the clock"}),
    ("app/chapters/ch06_real_money.py",
     {"fr": "6 · L'argent réel", "en": "6 · Real money"}),
    ("app/chapters/ch07_overfitting.py",
     {"fr": "7 · Le piège de l'overfitting", "en": "7 · The overfitting trap"}),
    ("app/chapters/ch08_verdict.py",
     {"fr": "8 · Le verdict", "en": "8 · The verdict"}),
    ("app/chapters/ch09_method.py",
     {"fr": "Données et méthode", "en": "Data and method"}),
]

pages = [
    st.Page(path, title=titles[i18n.current()], default=(index == 0))
    for index, (path, titles) in enumerate(CHAPTERS)
]

st.navigation({i18n.t("chapters"): pages}).run()
