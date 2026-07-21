"""No published table may carry an on-chain identity.

An address is a permanent, non-revocable identifier: this test is the gate that
stands between the archive and a public repository.
"""
import pathlib
import re

import pandas as pd
import pytest

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
TABLES = ["decisions", "resolutions", "market_snapshots", "real_trades"]

ADDRESS = re.compile(r"0x[a-fA-F0-9]{40}")
TX_HASH = re.compile(r"0x[a-fA-F0-9]{64}")
FORBIDDEN_COLUMNS = {"raw_activity", "proxyWallet", "wallet", "name",
                     "pseudonym", "tx_hash", "activity_id"}


@pytest.mark.parametrize("table", TABLES)
def test_no_identifying_columns(table):
    df = pd.read_parquet(DATA / f"{table}.parquet")
    assert not FORBIDDEN_COLUMNS & set(df.columns)


@pytest.mark.parametrize("table", TABLES)
def test_no_address_or_hash_in_any_value(table):
    df = pd.read_parquet(DATA / f"{table}.parquet")
    for column in df.select_dtypes(include=["object", "string"]).columns:
        joined = df[column].dropna().astype(str).str.cat(sep=" ")
        assert not ADDRESS.search(joined), f"address leaked in {table}.{column}"
        assert not TX_HASH.search(joined), f"tx hash leaked in {table}.{column}"


def test_real_trades_kept_their_analytic_value():
    """Anonymisation must not cost us the analysis: the money columns stay."""
    df = pd.read_parquet(DATA / "real_trades.parquet")
    assert len(df) == 127
    assert {"price", "shares", "usdc_size", "trade_side", "type"} <= set(df.columns)
