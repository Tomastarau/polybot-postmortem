import pandas as pd
import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("07-overfitting"))

result = data.overfitting()
labels = {k: i18n.t(f"ch7_{k}") for k in ["train", "test", "baseline", "filtered"]}
table = pd.DataFrame([
    {"periode": labels["train"], "filtre": labels["baseline"], **result["train_baseline"]},
    {"periode": labels["train"], "filtre": labels["filtered"], **result["train"]},
    {"periode": labels["test"], "filtre": labels["baseline"], **result["test_baseline"]},
    {"periode": labels["test"], "filtre": labels["filtered"], **result["test"]},
])
ui.figure(
    takeaway=i18n.t("ch7_takeaway"),
    fig=charts.train_test_bars(result, labels),
    table=table,
    method=i18n.t("ch7_method"),
    title=i18n.t("ch7_title"),
)
st.caption(", ".join(result["blacklist"]))

ui.pager("ch07_overfitting")
