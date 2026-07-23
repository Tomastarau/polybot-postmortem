import streamlit as st

from app import charts, data, i18n, ui

st.markdown(i18n.prose("02-naissance"))

labels = {k: i18n.t(f"ch2_{k}") for k in
          ["feature", "fix", "removal", "logging", "other"]}
ui.figure(
    takeaway=i18n.t("ch2_takeaway"),
    fig=charts.commit_timeline(data.commits(), labels),
    table=data.commit_log(),
    method=i18n.t("ch2_method"),
    title=i18n.t("ch2_title"),
)

ui.pager("ch02_birth")
