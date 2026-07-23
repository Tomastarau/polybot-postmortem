"""The numbers quoted in the story must be reproducible from the published data.

If a table changes and these fail, the story is wrong — not the test.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app import analysis  # noqa: E402


@pytest.fixture(scope="module")
def trades():
    return analysis.paper_trades()


def test_headline_numbers(trades):
    stats = analysis.summarise(trades)
    assert stats["trades"] == 752
    assert stats["pnl_usd"] == pytest.approx(1.12, abs=0.01)
    assert stats["win_rate"] == pytest.approx(0.883, abs=0.001)


def test_win_rate_is_not_an_edge(trades):
    """88% wins at an average entry near 0.88 is break-even, not skill."""
    stats = analysis.summarise(trades)
    assert abs(stats["roi"]) < 0.01
    assert trades["entry_price"].mean() == pytest.approx(stats["win_rate"], abs=0.02)


def test_monthly_breakdown(trades):
    by_month = {m: analysis.summarise(g) for m, g in trades.groupby("month")}
    assert by_month["2026-06"]["trades"] == 422
    assert by_month["2026-06"]["pnl_usd"] == pytest.approx(9.11, abs=0.01)
    assert by_month["2026-07"]["trades"] == 320
    assert by_month["2026-07"]["pnl_usd"] == pytest.approx(-0.13, abs=0.01)


def test_city_blacklist_is_overfitting(trades):
    """Fitted on May-June it looks excellent; on unseen July it is worthless."""
    result = analysis.out_of_sample_city_filter(trades)
    assert len(result["blacklist"]) == 9
    assert result["train"]["roi"] == pytest.approx(0.0724, abs=0.0005)
    assert result["test"]["roi"] == pytest.approx(-0.0040, abs=0.0005)
    assert result["train"]["roi"] > 0.05 > result["test"]["roi"]


def test_surviving_filter_is_positive_but_weak(trades):
    """Cheap entry + model agreement survives both halves, but the training
    half is thin enough that it stays a hypothesis, not a proven edge."""
    result = analysis.surviving_filter(trades)
    assert result["train"]["roi"] == pytest.approx(0.0145, abs=0.0005)
    assert result["test"]["roi"] == pytest.approx(0.1376, abs=0.0005)
    assert result["train"]["trades"] == 81
    assert result["test"]["trades"] == 48


def test_zero_spread_is_not_dropped(trades):
    """Regression guard: `spread or 9` treated a perfect model agreement (0.0)
    as a 9 degree spread and silently excluded the best observations."""
    assert (trades["forecast_spread_c"] == 0.0).sum() > 0
    kept = trades[(trades["entry_price"] <= 0.85) & (trades["forecast_spread_c"] <= 1.0)]
    assert (kept["forecast_spread_c"] == 0.0).sum() > 0


def test_pnl_is_indistinguishable_from_the_null_model(trades):
    """If the market price was always right, +1.12 $ is the expected outcome.

    The bot neither beat nor missed the market: it matched it, which is what
    having no edge means.
    """
    result = analysis.permutation_pnl(trades)
    assert 40 < result["percentile"] < 60
    assert result["std"] > 15
    assert result["observed"] == pytest.approx(1.12, abs=0.01)


def test_permutation_is_deterministic(trades):
    first = analysis.permutation_pnl(trades, iterations=500, seed=7)
    second = analysis.permutation_pnl(trades, iterations=500, seed=7)
    assert first["percentile"] == second["percentile"]
    assert first["median"] == second["median"]
