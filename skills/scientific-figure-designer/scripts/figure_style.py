"""Reusable plotting style; no fitting, resampling, or data changes."""

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager


CATEGORICAL = (
    "#0072B2", "#E69F00", "#009E73", "#D55E00",
    "#CC79A7", "#56B4E9", "#595959",
)
PPT_COLORS = {"red": "#C00000", "blue": "#0070C0", "dark_blue": "#002060"}


def check_fonts(chinese_font="SimSun", english_font="Times New Roman"):
    """Resolve requested fonts without silently accepting a substitute."""
    resolved = {}
    missing = []
    for family in (chinese_font, english_font):
        try:
            resolved[family] = font_manager.findfont(
                font_manager.FontProperties(family=family),
                fallback_to_default=False,
            )
        except ValueError:
            missing.append(family)
    if missing:
        raise RuntimeError(
            "Required fonts unavailable: " + ", ".join(missing)
            + ". Make them available or explicitly choose and disclose replacements."
        )
    return resolved


def apply_style(base_size=9.0, chinese_font="SimSun", english_font="Times New Roman"):
    """Configure a starting style; sizes must be checked at final output scale."""
    if base_size <= 0:
        raise ValueError("base_size must be positive")
    fonts = check_fonts(chinese_font, english_font)
    mpl.rcParams.update({
        "font.family": [english_font, chinese_font],
        "font.size": base_size,
        "axes.labelsize": base_size,
        "axes.titlesize": base_size + 1,
        "xtick.labelsize": max(6.0, base_size - 1),
        "ytick.labelsize": max(6.0, base_size - 1),
        "legend.fontsize": max(6.0, base_size - 1),
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.25,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "grid.color": "#D0D0D0",
        "grid.linewidth": 0.45,
        "grid.alpha": 0.45,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),
        "mathtext.fontset": "stix",
        "axes.unicode_minus": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    return fonts


def add_panel_label(ax, label, x=-0.1, y=1.04, size=None):
    """Add a figure-panel label in axes coordinates, including 3D axes."""
    if size is None:
        size = float(mpl.rcParams["font.size"]) + 2
    text_method = ax.text2D if getattr(ax, "name", "") == "3d" else ax.text
    return text_method(
        x, y, str(label), transform=ax.transAxes,
        fontsize=size, fontweight="bold", ha="left", va="top", clip_on=False,
    )


def style_3d_axes(ax, elev=24, azim=-55, projection="ortho", box_aspect=None):
    """Use public APIs; do not alter data, limits, or axis direction.

    Camera values are starting points, not scientific optimization. Supply a
    box_aspect only when its meaning and any exaggeration are understood.
    """
    if getattr(ax, "name", "") != "3d":
        raise ValueError("style_3d_axes requires a 3D axes")
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type(projection)
    if box_aspect is not None:
        ax.set_box_aspect(box_aspect)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor((0.82, 0.82, 0.82, 0.5))
    ax.tick_params(pad=1)
    return ax


def export_figure(fig, stem, formats=("svg", "pdf", "png"), dpi=300):
    """Export requested formats; retain text in SVG and create PNG previews.

    The caller owns naming, overwrite decisions, caption and data provenance.
    Successful export is not visual or native-editability validation.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    allowed = {"svg", "pdf", "png"}
    extensions = tuple(fmt.lower().lstrip(".") for fmt in formats)
    if not extensions or any(fmt not in allowed for fmt in extensions):
        raise ValueError("formats must contain svg, pdf, or png")
    if dpi <= 0:
        raise ValueError("dpi must be positive")
    paths = []
    for fmt in extensions:
        target = stem.with_suffix("." + fmt)
        fig.savefig(target, dpi=dpi, bbox_inches="tight", facecolor="white")
        paths.append(target)
    return paths
