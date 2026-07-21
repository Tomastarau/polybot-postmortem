"""Cached access to the gold tables. Pages never read Parquet directly."""
import streamlit as st

from app import analysis


@st.cache_data(show_spinner=False)
def table(name):
    return analysis.load(name)


@st.cache_data(show_spinner=False)
def paper_trades():
    return analysis.paper_trades()


@st.cache_data(show_spinner=False)
def headline():
    return analysis.summarise(paper_trades())


@st.cache_data(show_spinner=False)
def monthly():
    trades = paper_trades()
    rows = []
    for month, group in trades.groupby("month"):
        stats = analysis.summarise(group)
        stats["month"] = month
        rows.append(stats)
    return rows


@st.cache_data(show_spinner=False)
def equity_curve():
    trades = paper_trades().sort_values("ts").copy()
    trades["cumulative_pnl"] = trades["pnl_usd"].cumsum()
    return trades[["ts", "cumulative_pnl", "city", "pnl_usd", "entry_price", "mode"]]


@st.cache_data(show_spinner=False)
def overfitting():
    return analysis.out_of_sample_city_filter(paper_trades())


@st.cache_data(show_spinner=False)
def commits():
    df = table("commits")
    weekly = (df.assign(week=df["date"].dt.to_period("W").dt.start_time)
                .groupby(["week", "kind"]).size().reset_index(name="commits"))
    weekly["week"] = weekly["week"].dt.strftime("%d %b")
    return weekly


@st.cache_data(show_spinner=False)
def commit_log():
    return table("commits")[["date", "subject", "kind"]]


@st.cache_data(show_spinner=False)
def forecast_error():
    return analysis.forecast_error()


@st.cache_data(show_spinner=False)
def error_by_unit():
    return analysis.error_by_unit(analysis.forecast_error())


@st.cache_data(show_spinner=False)
def skip_reasons():
    return analysis.skip_reasons()


@st.cache_data(show_spinner=False)
def roi_by_entry_price():
    return analysis.roi_by_entry_price(paper_trades())


@st.cache_data(show_spinner=False)
def hourly_activity():
    return analysis.hourly_activity()


@st.cache_data(show_spinner=False)
def real_money():
    return analysis.real_money()


@st.cache_data(show_spinner=False)
def surviving_filter():
    return analysis.surviving_filter(paper_trades())
