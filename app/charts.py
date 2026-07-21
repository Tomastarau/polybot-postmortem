"""Plotly figures. One function per figure, no data access and no prose."""
import plotly.graph_objects as go

from app import theme


def equity_curve(df, hover_label):
    c = theme.palette()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["ts"],
        y=df["cumulative_pnl"],
        mode="lines",
        line={"color": c["series_1"], "width": 2},
        fill="tozeroy",
        fillcolor=theme.fade(c["series_1"]),
        hovertemplate=f"%{{x|%d %b}} · %{{y:+.2f}} $ · {hover_label}: %{{customdata}}<extra></extra>",
        customdata=df["city"],
    ))
    fig.add_hline(y=0, line={"color": c["baseline"], "width": 1})
    fig.update_layout(**theme.layout(height=320))
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(ticksuffix=" $")
    return fig


def monthly_bars(rows, label):
    c = theme.palette()
    values = [r["pnl_usd"] for r in rows]
    fig = go.Figure(go.Bar(
        x=[r["month"] for r in rows],
        y=values,
        marker={"color": [c["good"] if v >= 0 else c["critical"] for v in values],
                "cornerradius": 4},
        text=[f"{v:+.2f} $" for v in values],
        textposition="outside",
        textfont={"color": c["text_secondary"]},
        hovertemplate=f"%{{x}} · %{{y:+.2f}} $ · {label}: %{{customdata}}<extra></extra>",
        customdata=[r["trades"] for r in rows],
    ))
    fig.add_hline(y=0, line={"color": c["baseline"], "width": 1})
    fig.update_layout(**theme.layout(height=260))
    fig.update_layout(bargap=0.45)
    fig.update_yaxes(ticksuffix=" $")
    return fig


def commit_timeline(df, labels):
    c = theme.palette()
    colors = {"feature": c["series_1"], "fix": c["critical"],
              "removal": c["series_2"], "logging": c["muted"], "other": c["muted"]}
    fig = go.Figure()
    for kind in ["feature", "fix", "removal", "logging", "other"]:
        subset = df[df["kind"] == kind]
        if subset.empty:
            continue
        fig.add_trace(go.Bar(
            x=subset["week"], y=subset["commits"], name=labels.get(kind, kind),
            marker={"color": colors[kind], "cornerradius": 3, "line": {"width": 2,
                    "color": c["surface"]}},
            hovertemplate="%{x} · %{y} · " + labels.get(kind, kind) + "<extra></extra>",
        ))
    fig.update_layout(**theme.layout(height=280, showlegend=True))
    fig.update_layout(barmode="stack", bargap=0.4)
    return fig


def skip_reason_bars(df, label):
    c = theme.palette()
    df = df.iloc[::-1]
    fig = go.Figure(go.Bar(
        x=df["decisions"], y=df["skip_reason"], orientation="h",
        marker={"color": [c["good"] if r == "would_trade" else c["series_1"]
                          for r in df["skip_reason"]], "cornerradius": 4},
        hovertemplate=f"%{{y}} · %{{x:,}} {label}<extra></extra>",
    ))
    fig.update_layout(**theme.layout(height=320))
    fig.update_layout(margin={"l": 8, "r": 8, "t": 8, "b": 8})
    return fig


def error_histogram(df, labels):
    c = theme.palette()
    fig = go.Figure()
    for column, color, name in [
        ("error_raw", c["critical"], labels["raw"]),
        ("error_fixed", c["series_1"], labels["fixed"]),
    ]:
        fig.add_trace(go.Histogram(
            x=df[column].clip(-70, 70), name=name, nbinsx=70,
            marker={"color": color, "line": {"width": 1, "color": c["surface"]}},
            opacity=0.75,
            hovertemplate="%{x:.0f} · %{y}<extra>" + name + "</extra>",
        ))
    fig.update_layout(**theme.layout(height=300, showlegend=True))
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(ticksuffix=" °")
    return fig


def hourly_bars(rows, label):
    c = theme.palette()
    fig = go.Figure(go.Bar(
        x=[f"{r['hour']:02d}h" for r in rows],
        y=[r["decisions"] for r in rows],
        marker={"color": c["series_1"], "cornerradius": 4},
        hovertemplate=f"%{{x}} UTC · %{{y:,}} {label}<extra></extra>",
    ))
    fig.update_layout(**theme.layout(height=240))
    fig.update_layout(bargap=0.5)
    return fig


def money_waterfall(money, labels):
    c = theme.palette()
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=[labels["spent"], labels["sold"], labels["redeemed"], labels["net"]],
        y=[-money["spent"], money["sold"], money["redeemed"], None],
        connector={"line": {"color": c["baseline"], "width": 1}},
        decreasing={"marker": {"color": c["critical"]}},
        increasing={"marker": {"color": c["good"]}},
        totals={"marker": {"color": c["series_1"]}},
        text=[f"{-money['spent']:+.2f} $", f"{money['sold']:+.2f} $",
              f"{money['redeemed']:+.2f} $", f"{money['net']:+.2f} $"],
        textposition="outside",
        textfont={"color": c["text_secondary"]},
        hovertemplate="%{x} · %{y:+.2f} $<extra></extra>",
    ))
    fig.update_layout(**theme.layout(height=300))
    fig.update_yaxes(ticksuffix=" $")
    return fig


def train_test_bars(result, labels):
    c = theme.palette()
    fig = go.Figure()
    for key, color, name in [("train", c["series_1"], labels["train"]),
                             ("test", c["series_2"], labels["test"])]:
        fig.add_trace(go.Bar(
            x=[labels["baseline"], labels["filtered"]],
            y=[result[f"{key}_baseline"]["roi"] * 100, result[key]["roi"] * 100],
            name=name,
            marker={"color": color, "cornerradius": 4,
                    "line": {"width": 2, "color": c["surface"]}},
            text=[f"{result[f'{key}_baseline']['roi'] * 100:+.2f} %",
                  f"{result[key]['roi'] * 100:+.2f} %"],
            textposition="outside",
            textfont={"color": c["text_secondary"]},
            hovertemplate="%{x} · %{y:+.2f} %<extra>" + name + "</extra>",
        ))
    fig.add_hline(y=0, line={"color": c["baseline"], "width": 1})
    fig.update_layout(**theme.layout(height=320, showlegend=True))
    fig.update_layout(barmode="group", bargap=0.45, bargroupgap=0.08)
    fig.update_yaxes(ticksuffix=" %")
    return fig


def win_rate_vs_break_even(rows, labels):
    c = theme.palette()
    bands = [r["band"] for r in rows]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bands, y=[r["win_rate"] * 100 for r in rows], name=labels["win_rate"],
        marker={"color": c["series_1"], "cornerradius": 4,
                "line": {"width": 2, "color": c["surface"]}},
        text=[f"{r['win_rate'] * 100:.1f} %" for r in rows],
        textposition="inside",
        textfont={"color": "#ffffff"},
        hovertemplate="%{x} · %{y:.1f} %<extra>" + labels["win_rate"] + "</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=bands, y=[r["break_even"] * 100 for r in rows], name=labels["break_even"],
        mode="markers+lines",
        line={"color": c["critical"], "width": 2, "dash": "dot"},
        marker={"size": 10, "color": c["critical"],
                "line": {"width": 2, "color": c["surface"]}},
        hovertemplate="%{x} · %{y:.1f} %<extra>" + labels["break_even"] + "</extra>",
    ))
    fig.update_layout(**theme.layout(height=320, showlegend=True))
    fig.update_layout(bargap=0.5)
    fig.update_yaxes(ticksuffix=" %", range=[60, 100])
    return fig
