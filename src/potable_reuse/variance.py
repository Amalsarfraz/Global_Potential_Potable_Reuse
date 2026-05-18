"""Variance decomposition for the GCAM scenario ensemble.

"""

from __future__ import annotations

from typing import Iterable, Mapping

import numpy as np
import pandas as pd


# default factor set for the GCAM potable reuse ensemble
DEFAULT_FACTORS = ("ssp", "rcp", "supply", "rc")

# all unordered pairs of the four factors
DEFAULT_INTERACTIONS = (
    ("ssp", "rcp"),    ("ssp", "supply"), ("ssp", "rc"),
    ("rcp", "supply"), ("rcp", "rc"),     ("supply", "rc"),
)


def _conditional_mean_variance(
    df: pd.DataFrame,
    factor_cols: list[str],
    metric: str,
) -> float:
    """Variance of the conditional means E[Y | factor_cols].

    Returns 0 when there are not enough levels to estimate it.
    """
    means = df.groupby(factor_cols)[metric].mean()
    if len(means) <= 1:
        return 0.0
    return float(means.var())


def decompose_year(
    df: pd.DataFrame,
    metric: str = "value",
    factors: Iterable[str] = DEFAULT_FACTORS,
    interactions: Iterable[tuple[str, str]] = DEFAULT_INTERACTIONS,
    min_rows: int = 8,
    min_total_var: float = 1e-10,
) -> dict | None:

    factors = list(factors)
    interactions = list(interactions)

    total_var = float(df[metric].var())
    if total_var < min_total_var or len(df) < min_rows:
        return None

    comp: dict[str, float] = {}

    # main effects
    for f in factors:
        comp[f] = _conditional_mean_variance(df, [f], metric)

    # two-way interactions
    for f1, f2 in interactions:
        joint = _conditional_mean_variance(df, [f1, f2], metric)
        comp[f"{f1}_{f2}"] = max(0.0, joint - comp[f1] - comp[f2])

    # residual: whatever the sum of the above misses
    comp["residual"] = max(0.0, total_var - sum(comp.values()))

    # report as percentage shares of the resolved total
    denom = max(sum(comp.values()), min_total_var)
    return {k: v / denom * 100.0 for k, v in comp.items()}


def run_decomposition(
    df: pd.DataFrame,
    regions: Iterable[str],
    metric: str = "value",
    factors: Iterable[str] = DEFAULT_FACTORS,
    interactions: Iterable[tuple[str, str]] = DEFAULT_INTERACTIONS,
) -> pd.DataFrame:
    """Run `decompose_year` over every (region, year) cell in `df`.

    """
    rows = []
    years = sorted(df["year"].unique())

    for year in years:
        for region in regions:
            sub = df[(df["year"] == year) & (df["region"] == region)]
            res = decompose_year(
                sub,
                metric=metric,
                factors=factors,
                interactions=interactions,
            )
            if res is not None:
                rows.append({"year": year, "region": region, **res})

    return pd.DataFrame(rows)


# default plotting palette / labels for the 4-factor ensemble
COMPONENT_STYLES: Mapping[str, dict] = {
    "ssp":        {"color": "#1f77b4", "label": "SSP"},
    "rcp":        {"color": "#ff7f0e", "label": "RCP"},
    "supply":     {"color": "#2ca02c", "label": "Supply capacity"},
    "rc":         {"color": "#9467bd", "label": "Reuse cost"},
    "ssp_rcp":    {"color": "#d62728", "label": "SSP \u00d7 RCP"},
    "ssp_supply": {"color": "#17becf", "label": "SSP \u00d7 Supply"},
    "ssp_rc":     {"color": "#8c564b", "label": "SSP \u00d7 RC"},
    "rcp_supply": {"color": "#bcbd22", "label": "RCP \u00d7 Supply"},
    "rcp_rc":     {"color": "#e377c2", "label": "RCP \u00d7 RC"},
    "supply_rc":  {"color": "#7f7f7f", "label": "Supply \u00d7 RC"},
    "residual":   {"color": "#d9d9d9", "label": "Residual"},
}


def smooth_series(values: np.ndarray, window: int = 5) -> np.ndarray:
    """Symmetric rolling mean used for time-series displays.


    """
    from scipy.ndimage import uniform_filter1d
    return uniform_filter1d(np.asarray(values, dtype=float), size=window)
