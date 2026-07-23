"""The two-audiences component: a plain sentence, the chart, then the details.

Enforces the project rule that no chart is ever shown bare. If a chart has no
takeaway sentence, it has no reason to exist.
"""
import streamlit as st

from app import i18n, navigation


def figure(takeaway, fig, table=None, method=None, title=None):
    if title:
        st.subheader(title)
    st.markdown(f"**{takeaway}**")
    st.plotly_chart(fig)
    if table is not None or method:
        with st.expander(i18n.t("details")):
            if method:
                st.markdown(method)
            if table is not None:
                st.dataframe(table, hide_index=True, width="stretch")


def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value, help=help_text)


def pager(key):
    previous, following = navigation.neighbours(key)
    lang = i18n.current()
    st.divider()
    left, right = st.columns(2)
    if previous:
        left.page_link(navigation.path(previous),
                       label=f"← {navigation.label(previous, lang)}",
                       help=i18n.t("previous"))
    if following:
        right.page_link(navigation.path(following),
                        label=f"{navigation.label(following, lang)} →",
                        help=i18n.t("next"))
