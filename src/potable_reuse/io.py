"""Data IO layer for the GCAM potable reuse scenario ensemble.

The scenario ensemble lives on disk as one folder per scenario, named
    SSP{1..5}_{rcp}_{HRC|MRC|LRC}_{H|M|L}_{PR0|PR50|PR100}
each containing the relevant GCAM query parquets.

This module hides that convention behind a couple of small helpers so the
notebooks themselves stay focused on the science.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


# scenario folder name like 'SSP2_4p5_MRC_M_PR50'
# groups: ssp, rcp, reuse cost tier, supply capacity tier, PR level
_SCENARIO_RE = re.compile(
    r"^(SSP\d)_([\dp]+)_(HRC|MRC|LRC)_(H|M|L)_(PR\d+)$",
    re.IGNORECASE,
)


def parse_scenario_folder(name: str) -> dict | None:
    """Parse a scenario folder name into its design dimensions.

    Returns None if the name does not match. Callers can use that to
    silently skip stray folders (logs, README backups, etc.) without
    blowing up the load loop.
    """
    m = _SCENARIO_RE.match(name)
    if m is None:
        return None
    return {
        "ssp":      m.group(1).upper(),
        "rcp":      m.group(2),
        "ssp_rcp":  f"{m.group(1).upper()}_{m.group(2)}",
        "rc":       m.group(3).upper(),
        "supply":   m.group(4).upper(),
        "pr":       m.group(5).upper(),
        "scenario": name,
    }


def load_scenario_query(
    base_dir: Path,
    query_file: str,
    cache_path: Path | None = None,
    verbose: bool = True,
) -> pd.DataFrame:
    """Load one GCAM query across every scenario in `base_dir`.

    Each scenario folder is expected to contain `query_file`. The
    returned frame is the row-wise concatenation of all of them with the
    scenario design dimensions appended as new columns.

    Optional `cache_path` lets us write the concatenated frame as a
    single parquet so subsequent runs skip the per-folder reads. This is
    the bottleneck on Figure 1: 459 scenarios x ~25 MB each.
    """
    base_dir = Path(base_dir)

    if cache_path is not None and Path(cache_path).exists():
        if verbose:
            print(f"  Loading cache: {Path(cache_path).name}")
        df = pd.read_parquet(cache_path)
        if verbose:
            print(f"    {len(df):,} rows | "
                  f"{df['scenario'].nunique()} scenarios")
        return df

    frames = []
    n_folders = 0
    n_with_query = 0
    for folder in sorted(base_dir.iterdir()):
        if not folder.is_dir():
            continue
        meta = parse_scenario_folder(folder.name)
        if meta is None:
            continue
        n_folders += 1

        pq = folder / query_file
        if not pq.exists():
            continue
        n_with_query += 1

        df = pd.read_parquet(pq)
        for k, v in meta.items():
            df[k] = v
        frames.append(df)

    if not frames:
        raise FileNotFoundError(
            f"No scenario folders matching the SSP*_*_*_*_PR* pattern "
            f"contained '{query_file}' under {base_dir}."
        )

    out = pd.concat(frames, ignore_index=True)

    if verbose:
        print(f"  {n_folders} scenario folders matched, "
              f"{n_with_query} contained the query, "
              f"{len(out):,} total rows")

    if cache_path is not None:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        out.to_parquet(cache_path, index=False)
        if verbose:
            print(f"  Cached: {Path(cache_path).name}")

    return out


def filter_municipal_withdrawal(
    df: pd.DataFrame,
    year_min: int = 2025,
    year_max: int = 2100,
    group_keys: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Aggregate the 'water withdrawals by water mapping source' query
    to municipal withdrawals, summed over within-region subresources.

    GCAM emits one row per (region, subresource, sector, year, scenario);
    we want the muncipal sector total per (region, year, scenario).
    """
    default_keys = ["ssp", "rcp", "rc", "supply", "pr", "region", "year"]
    keys = list(group_keys) if group_keys is not None else default_keys

    muni = df[
        (df["year"] >= year_min)
        & (df["year"] <= year_max)
        & (df["input"] == "water_td_muni_W")
    ]
    return muni.groupby(keys, as_index=False)["value"].sum()


def normalize_region_name(name: str) -> str:
    """Lowercase, strip, drop spaces and underscores.

    GCAM, the parquet outputs, and the rmap shapefiles disagree slightly
    on how to spell EU-12 vs EU_12 vs eu 12. Normalising before matching
    avoids spurious mismatches.
    """
    return name.lower().replace("_", "").replace(" ", "").strip()


def match_region(
    candidates: Iterable[str],
    available: Iterable[str],
) -> str | None:
    """Best effort match for a region name.

    Tries exact normalised match first, then substring fallback.
    Returns the canonical name from `available`, or None if no match.
    """
    norm_avail = {normalize_region_name(r): r for r in available}

    for c in candidates:
        if normalize_region_name(c) in norm_avail:
            return norm_avail[normalize_region_name(c)]

    # substring fallback (e.g. "USA" -> "United States")
    for c in candidates:
        nc = normalize_region_name(c)
        for na, original in norm_avail.items():
            if nc in na or na in nc:
                return original
    return None
