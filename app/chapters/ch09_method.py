import streamlit as st

from app import i18n

st.markdown(i18n.prose("09-methode"))
st.info(f"**{i18n.t('source')}** — {i18n.t('source_body')}")
