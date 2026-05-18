"""Shared matplotlib style for paper figures.

Enforces the manuscript-wide visual conventions:
  - axis labels at 16 pt
  - no grid lines on any axes
  - 1200 dpi for raster (PNG) output
  - all subplots show their own tick labels

Call `apply_style()` once at the top of any notebook, after pyplot is
imported. Individual figures can still override on a per-Axes basis if
needed; this only sets the defaults.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


# manuscript-wide constants. 
AXIS_LABEL_SIZE = 16
TITLE_SIZE      = 16
TICK_LABEL_SIZE = 12
LEGEND_SIZE     = 11
SAVE_DPI        = 1200


def apply_style() -> None:
    """Set the paper-wide matplotlib defaults.

    """
    plt.rcParams.update({
        # typography
        "font.family":       "sans-serif",
        "font.sans-serif":   ["Arial", "Helvetica", "DejaVu Sans"],
        "axes.labelsize":    AXIS_LABEL_SIZE,
        "axes.titlesize":    TITLE_SIZE,
        "xtick.labelsize":   TICK_LABEL_SIZE,
        "ytick.labelsize":   TICK_LABEL_SIZE,
        "legend.fontsize":   LEGEND_SIZE,

        # raster resolution: only affects savefig(), not on-screen display
        "figure.dpi":        110,
        "savefig.dpi":       SAVE_DPI,
        "savefig.bbox":      "tight",

        # no grid anywhere by default
        "axes.grid":         False,
        "axes.spines.top":   False,
        "axes.spines.right": False,
    })


def show_all_axes(axes) -> None:
    """Force tick labels and axis labels visible on every subplot.

    """
    for ax in np.atleast_1d(axes).ravel():
        ax.tick_params(labelbottom=True, labelleft=True)
        # also re-enable spines that sharex/sharey can hide
        for spine in ("bottom", "left"):
            ax.spines[spine].set_visible(True)


def strip_grid(axes) -> None:
    """Turn off the grid on every supplied Axes.

    """
    for ax in np.atleast_1d(axes).ravel():
        ax.grid(False)
