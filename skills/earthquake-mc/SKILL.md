---
name: earthquake-mc
description: Estimate earthquake catalog magnitude of completeness Mc using normalized cumulative occurrence curves, especially the Petrillo & Zhuang normalized quantity method used in the EMQTP fault-zone correlation paper. Use when the user asks to calculate, explain, plot, justify, or report Mc/completeness magnitude for earthquake catalogs before b-value, Gutenberg-Richter, declustering, correlation, or seismicity-rate analysis.
---

# Earthquake Mc

## Core Task

Estimate and explain the magnitude of completeness (`Mc`) for an earthquake catalog by comparing normalized cumulative occurrence curves for a range of threshold magnitudes. Use this skill when a catalog must be filtered to a complete magnitude range before downstream seismicity statistics.

The motivating paper is:

- *Correlation of earthquake occurrence among major fault zones in the eastern margin of the Tibetan Plateau through Big Data Analysis*, The Innovation Geoscience, 2025.
- It cites Petrillo and Zhuang (2023), *Verifying the Magnitude Dependence in Earthquake Occurrence*, Phys. Rev. Lett. 131, 154101.
- In the EMQTP case, threshold curves were tested for `Mc = 0.5, 1.0, 1.5, 2.0, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.5`. Curves were dispersed for `Mc <= 2.0` and nearly overlapped for `Mc >= 2.5`, so the paper adopted `Mc = 2.5`.

Do not hard-code `2.5` for new catalogs. Treat it as an example from that paper.

## Required Inputs

Require or infer:

- Event origin time or an event order column.
- Magnitude column.
- Study region, time window, catalog source, magnitude type, and magnitude precision if available.
- Candidate magnitude thresholds, usually spanning below and above the likely completeness magnitude.

Before estimating `Mc`, check:

- Time values are parseable and sorted chronologically.
- Magnitudes are numeric and use one magnitude scale or documented mixed scales.
- The catalog time span does not combine strongly incompatible network eras without noting the limitation.
- Each candidate threshold has enough events to support a curve. Flag thresholds with too few events.

## Normalized Quantity Method

For each threshold magnitude `m_th`, select events with `M >= m_th`. Compute the normalized cumulative count as a function of time:

```text
F(t | m_th) = count(events with time <= t and M >= m_th) / count(events with M >= m_th)
```

This is the empirical cumulative distribution of occurrence times for events above each threshold.

Interpretation:

- If `m_th` is below the completeness magnitude, early or low-detectability periods usually miss small events. The normalized curves for lower thresholds separate from higher-threshold curves.
- If `m_th` is at or above `Mc`, the curves for all higher thresholds should become visually indistinct or nearly collapse, apart from small noise.
- Choose the lowest threshold at which the curve family is stable/collapsed and event counts remain adequate.

The method is a catalog-completeness diagnostic, not a standalone proof. Combine the plot with event counts, known station/network changes, magnitude precision, and study purpose.

## Workflow

1. Load the catalog and identify time and magnitude fields.
2. Define candidate thresholds. If the user does not provide them, use the catalog magnitude precision:
   - `0.1` spacing for high-resolution catalogs.
   - `0.5` spacing for coarse historical or regional catalogs.
   - Include several thresholds below and above the apparent transition.
3. For each threshold, calculate event count and `F(t | m_th)`.
4. Plot all normalized cumulative curves on the same time axis. Overlay catalog events or a magnitude-time scatter when useful.
5. Quantify curve separation using a common time grid:
   - Interpolate each threshold curve on the same grid.
   - Compare the envelope of curves from each candidate threshold upward.
   - Report max and median separation; use this only as a guide, not a substitute for visual inspection.
6. Select the lowest threshold where higher-threshold curves collapse and sample size is still sufficient.
7. Write a short justification that includes candidate thresholds, accepted `Mc`, rejected lower thresholds, event counts, and known caveats.

## Script

Use `scripts/estimate_mc_normalized.py` when the user provides a CSV catalog or asks for a reproducible calculation.

Example:

```bash
python scripts/estimate_mc_normalized.py catalog.csv \
  --time-column time \
  --mag-column magnitude \
  --thresholds 0.5,1.0,1.5,2.0,2.5,2.6,2.7,2.8,2.9,3.0,3.5 \
  --out-dir mc_results
```

The script writes:

- `normalized_curves.csv`
- `threshold_summary.csv`
- `mc_report.md`
- `normalized_curves.png` if `matplotlib` is installed

Treat the script recommendation as a first pass. Always inspect the plot and the event counts before giving the final `Mc`.

## Reporting Template

When reporting `Mc`, include:

```text
Catalog: <source, region, time window>
Method: normalized cumulative occurrence curves after Petrillo & Zhuang (2023)
Candidate thresholds: <list>
Accepted Mc: <value>
Reason: curves below <value> are separated; curves from <value> upward nearly overlap/collapse.
Event count at Mc: <n>
Caveats: <network changes, magnitude type, sparse high-threshold curves, mixed catalog sources, etc.>
Downstream use: use events with M >= Mc for statistics requiring catalog completeness.
```

## Relationship To b-Value

Do not claim that the EMQTP paper computed a b-value unless the user provides additional supporting text. In that paper's main text, the relevant section uses the normalized quantity method to choose `Mc`; it does not present a b-value calculation workflow.

If the user asks to calculate b-value after `Mc`, use a standard Gutenberg-Richter/Aki-Utsu maximum-likelihood estimate on events with `M >= Mc`:

```text
b = log10(e) / (mean(M) - (Mc - deltaM / 2))
```

Use `deltaM` equal to the catalog magnitude bin width, commonly `0.1` when magnitudes are rounded to 0.1. State whether the b-value is calculated from the raw or declustered catalog.
