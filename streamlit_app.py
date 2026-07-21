import pathlib
import sys

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from app import i18n, navigation  # noqa: E402

st.set_page_config(
    page_title="Polybot, post-mortem",
    page_icon="🌡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

i18n.language_selector()

lang = i18n.current()
pages = [
    st.Page(navigation.path(key), title=navigation.label(key, lang), default=(index == 0))
    for index, key in enumerate(navigation.KEYS)
]

st.navigation({i18n.t("chapters"): pages}).run()
