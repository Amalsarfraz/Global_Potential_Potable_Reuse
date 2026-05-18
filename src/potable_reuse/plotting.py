"""Plotting helpers shared across all figure scripts.

The paper sticks to PNG (raster, 300 dpi default), SVG (vector for
journal submission), and a self-contained HTML wrapper around the SVG
for browser preview. 
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body  {{ font-family: Arial, Helvetica, sans-serif; margin: 24px; color: #222; }}
h2    {{ font-weight: 600; }}
svg   {{ max-width: 100%; height: auto; }}
</style>
</head>
<body>
<h2>{title}</h2>
{svg_text}
</body>
</html>
"""


def save_all(
    fig: plt.Figure,
    out_dir: Path | str,
    stem: str,
    dpi: int = 1200,
    facecolor: str = "white",
    verbose: bool = True,
) -> dict[str, Path]:
    """Save `fig` as PNG, SVG, and an HTML wrapper of the SVG.

    Parameters
    ----------
    fig
        The matplotlib Figure to save.
    out_dir
        Directory to write into; created if missing.
    stem
        Filename stem, no extension. The three outputs are
        `<stem>.png`, `<stem>.svg`, `<stem>.html`.
    dpi
        PNG raster resolution. SVG is vector and ignores dpi.

    Returns
    -------
    dict
        Mapping {"png": Path, "svg": Path, "html": Path}.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    png  = out_dir / f"{stem}.png"
    svg  = out_dir / f"{stem}.svg"
    html = out_dir / f"{stem}.html"

    fig.savefig(png, dpi=dpi, bbox_inches="tight", facecolor=facecolor)
    fig.savefig(svg,           bbox_inches="tight", facecolor=facecolor)

    svg_text = svg.read_text(encoding="utf-8")
    html.write_text(
        _HTML_TEMPLATE.format(title=stem, svg_text=svg_text),
        encoding="utf-8",
    )

    if verbose:
        print(f"  Saved: {png.name} | {svg.name} | {html.name}")

    return {"png": png, "svg": svg, "html": html}
