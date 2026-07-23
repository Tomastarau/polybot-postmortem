import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("06-argent-reel"))

money = data.real_money()
labels = {k: i18n.t(f"ch6_{k}") for k in ["spent", "sold", "redeemed", "net"]}
summary = pd.DataFrame([
    {"flux": labels["spent"], "usd": -money["spent"], "n": money["buys"]},
    {"flux": labels["sold"], "usd": money["sold"], "n": money["stop_losses"]},
    {"flux": labels["redeemed"], "usd": money["redeemed"], "n": money["redemptions"]},
    {"flux": labels["net"], "usd": money["net"], "n": None},
])
ui.figure(
    takeaway=i18n.t("ch6_takeaway"),
    fig=charts.money_waterfall(money, labels),
    table=summary,
    method=i18n.t("ch6_method"),
    title=i18n.t("ch6_title"),
)

ui.pager("ch06_real_money")
