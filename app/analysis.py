"""P&L reconstruction from the gold tables.

Pure pandas, no Streamlit: the numbers quoted in the story are produced here and
locked by tests, so the narrative can never drift from the data.
"""
import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
STAKE_USD = 2.0


def load(name):
    return pd.read_parquet(DATA / f"{name}.parquet")


def bucket_contains(row):
    """Did the official temperature land inside the bucket the bot bet against?"""
    value = row["official_bucket_value"]
    low, high = row["bucket_low"], row["bucket_high"]
    if pd.isna(value) or pd.isna(low):
        return None
    if row["bucket_kind"] == "exact":
        return value == low
    if pd.isna(high):
        return value >= low
    return low <= value <= high


def paper_trades():
    """Every decision the bot would have taken, joined to the official outcome.

    The bot bets NO on a temperature bucket: it wins when the official value
    lands outside the bucket. Stake is fixed, so P&L per trade is
    (stake/price - stake) on a win and -stake on a loss.
    """
    decisions = load("decisions")
    resolutions = load("resolutions")

    df = decisions[decisions["would_trade"] & (decisions["side"] == "NO")].copy()
    df = df.merge(
        resolutions[["city", "target_date", "official_bucket_value",
                     "official_raw_value", "official_source"]],
        on=["city", "target_date"], how="inner",
    )
    df = df[df["entry_price"].notna() & (df["entry_price"] > 0)]

    df["inside"] = df.apply(bucket_contains, axis=1)
    df = df[df["inside"].notna()].copy()
    df["win"] = ~df["inside"].astype(bool)
    df["pnl_usd"] = df["win"].map({True: 0.0, False: -STAKE_USD})
    df.loc[df["win"], "pnl_usd"] = STAKE_USD / df.loc[df["win"], "entry_price"] - STAKE_USD
    df["month"] = pd.to_datetime(df["ts"]).dt.strftime("%Y-%m")
    return df


def summarise(df):
    deployed = STAKE_USD * len(df)
    return {
        "trades": len(df),
        "pnl_usd": round(df["pnl_usd"].sum(), 2),
        "deployed_usd": round(deployed, 2),
        "roi": round(df["pnl_usd"].sum() / deployed, 6) if deployed else 0.0,
        "win_rate": round(df["win"].mean(), 4) if len(df) else 0.0,
    }


def out_of_sample_city_filter(df, split="2026-07-01"):
    """The overfitting demonstration: a city blacklist fitted on the training
    half, then applied untouched to the unseen half."""
    train = df[df["month"] < split[:7]]
    test = df[df["month"] >= split[:7]]

    by_city = train.groupby("city")["pnl_usd"].agg(["sum", "count"])
    blacklist = set(by_city[(by_city["sum"] < 0) & (by_city["count"] >= 5)].index)

    return {
        "blacklist": sorted(blacklist),
        "train": summarise(train[~train["city"].isin(blacklist)]),
        "test": summarise(test[~test["city"].isin(blacklist)]),
        "train_baseline": summarise(train),
        "test_baseline": summarise(test),
    }


def surviving_filter(df):
    """The only filter positive on both halves: cheap entry + model agreement."""
    keep = (df["entry_price"] <= 0.85) & (df["forecast_spread_c"] <= 1.0)
    return {
        "train": summarise(df[keep & (df["month"] < "2026-07")]),
        "test": summarise(df[keep & (df["month"] >= "2026-07")]),
    }


def forecast_error():
    """Forecast minus official temperature, per market unit.

    Fahrenheit markets store their official value in Fahrenheit while the
    forecast stays Celsius: comparing them raw produces a ~54 degree error that
    is an accounting artefact, not a bad forecast.
    """
    decisions = load("decisions")
    resolutions = load("resolutions")
    df = decisions.merge(
        resolutions[["city", "target_date", "official_raw_value"]],
        on=["city", "target_date"], how="inner",
    )
    df = df[df["forecast_value_c"].notna() & df["official_raw_value"].notna()].copy()
    df["official_celsius"] = df["official_raw_value"].where(
        df["unit"] != "fahrenheit", (df["official_raw_value"] - 32) * 5 / 9
    )
    df["error_raw"] = df["forecast_value_c"] - df["official_raw_value"]
    df["error_fixed"] = df["forecast_value_c"] - df["official_celsius"]
    return df[["city", "unit", "target_date", "error_raw", "error_fixed",
               "forecast_spread_c"]]


def error_by_unit(df):
    grouped = df.groupby("unit")
    return [
        {
            "unit": unit,
            "cities": int(group_all["city"].nunique()),
            "decisions": len(group_all),
            "median_abs_raw": round(group_all["error_raw"].abs().median(), 2),
            "median_abs_fixed": round(group_all["error_fixed"].abs().median(), 2),
        }
        for unit, group_all in grouped
    ]


def skip_reasons(top=6):
    decisions = load("decisions")
    counts = decisions["skip_reason"].fillna("would_trade").value_counts()
    return counts.head(top).reset_index().rename(
        columns={"index": "skip_reason", "count": "decisions"})


def roi_by_entry_price(df):
    """Where the edge lived, by how much the bot paid to enter."""
    bands = [(0.0, 0.70), (0.70, 0.85), (0.85, 0.93), (0.93, 1.01)]
    rows = []
    for low, high in bands:
        subset = df[(df["entry_price"] >= low) & (df["entry_price"] < high)]
        if subset.empty:
            continue
        stats = summarise(subset)
        stats["band"] = f"{low:.2f}–{high:.2f}"
        stats["break_even"] = round(subset["entry_price"].mean(), 3)
        rows.append(stats)
    return rows


def hourly_activity():
    decisions = load("decisions")
    hours = pd.to_datetime(decisions["ts"]).dt.hour.value_counts().sort_index()
    return [{"hour": int(h), "decisions": int(n)} for h, n in hours.items() if n > 100]


def real_money():
    """What actually moved on-chain, split by ledger event type.

    BUY is money out, SELL and REDEEM are money back. Counting every row as a
    cost was the mistake that produced a -57 dollar first diagnosis.
    """
    trades = load("real_trades")
    spent = trades[trades["trade_side"] == "BUY"]["usdc_size"].sum()
    sold = trades[trades["trade_side"] == "SELL"]["usdc_size"].sum()
    redeemed = trades[trades["type"] == "REDEEM"]["usdc_size"].sum()
    return {
        "spent": round(spent, 2),
        "sold": round(sold, 2),
        "redeemed": round(redeemed, 2),
        "net": round(sold + redeemed - spent, 2),
        "buys": int((trades["trade_side"] == "BUY").sum()),
        "stop_losses": int((trades["trade_side"] == "SELL").sum()),
        "redemptions": int((trades["type"] == "REDEEM").sum()),
        "first_day": str(trades["sync_ts"].min())[:10],
        "last_day": str(trades["sync_ts"].max())[:10],
    }


def permutation_pnl(df, iterations=10000, seed=0):
    """Total P&L if the market price had always been right.

    Each bet wins with the probability the market gave it, which is its entry
    price. Replaying the bets under that assumption gives the distribution of
    P&L in the absence of any edge, so the real result can be placed against it
    instead of being argued about.
    """
    price = df["entry_price"].to_numpy()
    gain = STAKE_USD / price - STAKE_USD
    rng = np.random.default_rng(seed)
    won = rng.random((iterations, len(price))) < price
    simulated = np.where(won, gain, -STAKE_USD).sum(axis=1)
    observed = float(df["pnl_usd"].sum())
    return {
        "simulated": simulated,
        "observed": round(observed, 2),
        "percentile": round(float((simulated < observed).mean() * 100), 1),
        "median": round(float(np.median(simulated)), 2),
        "std": round(float(simulated.std()), 2),
    }
