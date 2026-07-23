import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("03-strategies"))

reasons = data.skip_reasons()
ui.figure(
    takeaway=i18n.t("ch3_takeaway"),
    fig=charts.skip_reason_bars(reasons, i18n.t("decisions")),
    table=reasons,
    method=i18n.t("ch3_method"),
    title=i18n.t("ch3_title"),
)

ui.pager("ch03_strategies")
