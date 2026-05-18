"""Shared utilities for the potable reuse paper figure pipeline.

Provides:
  io          parquet loaders, scenario-folder parser, regional aggregation
  variance    ANOVA-style variance decomposition
  plotting    triple-format save (PNG, SVG, HTML) used in every figure script
  style       manuscript-wide matplotlib style (axis labels at 16, no grid,
              dpi 1200, all subplots show their axes)
"""

from . import io
from . import variance
from . import plotting
from . import style

__all__ = ["io", "variance", "plotting", "style"]
__version__ = "1.0.0"
