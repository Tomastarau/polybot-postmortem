import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("01-resume"))

stats = data.headline()
ui.kpi_row([
    (i18n.t("trades"), f"{stats['trades']:,}".replace(",", " "), None),
    (i18n.t("pnl"), f"{stats['pnl_usd']:+.2f} $", None),
    (i18n.t("win_rate"), f"{stats['win_rate']:.1%}", None),
    (i18n.t("roi"), f"{stats['roi']:+.2%}", None),
])

ui.figure(
    takeaway=i18n.t("ch1_equity_takeaway"),
    fig=charts.equity_curve(data.equity_curve(), i18n.t("city")),
    method=i18n.t("ch1_equity_method"),
    title=i18n.t("ch1_equity_title"),
)

rows = data.monthly()
ui.figure(
    takeaway=i18n.t("ch1_monthly_takeaway"),
    fig=charts.monthly_bars(rows, i18n.t("trades")),
    table=pd.DataFrame(rows)[["month", "trades", "pnl_usd", "roi", "win_rate"]],
    title=i18n.t("ch1_monthly_title"),
)

st.info(f"**{i18n.t('source')}** — {i18n.t('source_body')}")
