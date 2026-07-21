import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("05-infra"))

hours = data.hourly_activity()
ui.figure(
    takeaway=i18n.t("ch5_takeaway"),
    fig=charts.hourly_bars(hours, i18n.t("decisions")),
    table=pd.DataFrame(hours),
    method=i18n.t("ch5_method"),
    title=i18n.t("ch5_title"),
)
