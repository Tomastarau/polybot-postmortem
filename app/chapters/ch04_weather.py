import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("04-meteo"))

labels = {"raw": i18n.t("ch4_raw"), "fixed": i18n.t("ch4_fixed")}
ui.figure(
    takeaway=i18n.t("ch4_takeaway"),
    fig=charts.error_histogram(data.forecast_error(), labels),
    table=pd.DataFrame(data.error_by_unit()),
    method=i18n.t("ch4_method"),
    title=i18n.t("ch4_title"),
)
