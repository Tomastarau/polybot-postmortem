import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("08-verdict"))

rows = data.roi_by_entry_price()
labels = {"win_rate": i18n.t("ch8_win_rate"), "break_even": i18n.t("ch8_break_even")}
ui.figure(
    takeaway=i18n.t("ch8_takeaway"),
    fig=charts.win_rate_vs_break_even(rows, labels),
    table=pd.DataFrame(rows)[["band", "trades", "win_rate", "break_even", "roi", "pnl_usd"]],
    method=i18n.t("ch8_method"),
    title=i18n.t("ch8_title"),
)

null = data.null_model()
ui.figure(
    takeaway=i18n.t("ch8_null_takeaway"),
    fig=charts.null_distribution(null, {"observed": i18n.t("ch8_observed")}),
    table=pd.DataFrame([{
        "observed": null["observed"],
        "median": null["median"],
        "std": null["std"],
        "percentile": null["percentile"],
    }]),
    method=i18n.t("ch8_null_method"),
    title=i18n.t("ch8_null_title"),
)

ui.pager("ch08_verdict")
