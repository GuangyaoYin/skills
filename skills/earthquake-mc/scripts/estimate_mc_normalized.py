#!/usr/bin/env python3
"""Estimate catalog completeness magnitude with normalized cumulative curves."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
from pathlib import Path


def parse_time(value: str) -> float:
    text = value.strip()
    if not text:
        raise ValueError("empty time value")
    try:
        return float(text)
    except ValueError:
        pass
    normalized = text.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(normalized).timestamp()
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(text, fmt).timestamp()
        except ValueError:
            continue
    raise ValueError(f"unparseable time value: {value!r}")


def read_catalog(path: Path, time_column: str, mag_column: str) -> list[tuple[float, float, str]]:
    events: list[tuple[float, float, str]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("CSV file has no header row")
        missing = [col for col in (time_column, mag_column) if col not in reader.fieldnames]
        if missing:
            raise SystemExit(f"Missing column(s): {', '.join(missing)}. Available: {', '.join(reader.fieldnames)}")
        for line_no, row in enumerate(reader, start=2):
            try:
                time_value = parse_time(row[time_column])
                mag_value = float(row[mag_column])
            except Exception as exc:
                raise SystemExit(f"Bad row {line_no}: {exc}") from exc
            events.append((time_value, mag_value, row[time_column]))
    if not events:
        raise SystemExit("No events found")
    events.sort(key=lambda item: item[0])
    return events


def normalized_curve(events: list[tuple[float, float, str]], threshold: float) -> list[tuple[float, float, str]]:
    selected = [(t, original) for t, mag, original in events if mag >= threshold]
    total = len(selected)
    if total == 0:
        return []
    return [(t, idx / total, original) for idx, (t, original) in enumerate(selected, start=1)]


def interp_step(curve: list[tuple[float, float, str]], grid_time: float) -> float:
    if not curve:
        return math.nan
    lo, hi = 0, len(curve) - 1
    if grid_time < curve[0][0]:
        return 0.0
    if grid_time >= curve[-1][0]:
        return 1.0
    while lo <= hi:
        mid = (lo + hi) // 2
        if curve[mid][0] <= grid_time:
            lo = mid + 1
        else:
            hi = mid - 1
    return curve[hi][1]


def separation_metrics(curves: dict[float, list[tuple[float, float, str]]], thresholds: list[float], grid_size: int) -> dict[float, tuple[float, float]]:
    valid_times = [point[0] for curve in curves.values() for point in curve]
    if not valid_times:
        return {threshold: (math.nan, math.nan) for threshold in thresholds}
    start, end = min(valid_times), max(valid_times)
    if start == end:
        return {threshold: (0.0, 0.0) for threshold in thresholds}
    grid = [start + (end - start) * i / (grid_size - 1) for i in range(grid_size)]
    metrics: dict[float, tuple[float, float]] = {}
    for threshold in thresholds:
        active = [thr for thr in thresholds if thr >= threshold and curves.get(thr)]
        spreads: list[float] = []
        for gt in grid:
            values = [interp_step(curves[thr], gt) for thr in active]
            values = [value for value in values if not math.isnan(value)]
            if len(values) >= 2:
                spreads.append(max(values) - min(values))
        if spreads:
            spreads_sorted = sorted(spreads)
            median = spreads_sorted[len(spreads_sorted) // 2]
            metrics[threshold] = (max(spreads), median)
        else:
            metrics[threshold] = (math.nan, math.nan)
    return metrics


def maybe_plot(curves: dict[float, list[tuple[float, float, str]]], out_path: Path) -> bool:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except Exception:
        return False
    plt.figure(figsize=(10, 6))
    for threshold, curve in sorted(curves.items()):
        if not curve:
            continue
        times = [dt.datetime.fromtimestamp(point[0]) for point in curve]
        values = [point[1] for point in curve]
        plt.step(times, values, where="post", label=f"M >= {threshold:g}")
    plt.xlabel("Time")
    plt.ylabel("Normalized cumulative count")
    plt.ylim(0, 1.02)
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2, fontsize=8)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog_csv", type=Path)
    parser.add_argument("--time-column", required=True)
    parser.add_argument("--mag-column", required=True)
    parser.add_argument("--thresholds", required=True, help="Comma-separated threshold magnitudes")
    parser.add_argument("--out-dir", type=Path, default=Path("mc_results"))
    parser.add_argument("--grid-size", type=int, default=200)
    parser.add_argument("--collapse-tolerance", type=float, default=0.08)
    parser.add_argument("--min-events", type=int, default=100)
    args = parser.parse_args()

    thresholds = sorted({float(item.strip()) for item in args.thresholds.split(",") if item.strip()})
    if len(thresholds) < 2:
        raise SystemExit("Provide at least two threshold magnitudes")

    events = read_catalog(args.catalog_csv, args.time_column, args.mag_column)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    curves = {threshold: normalized_curve(events, threshold) for threshold in thresholds}
    metrics = separation_metrics(curves, thresholds, args.grid_size)

    recommendation = None
    for threshold in thresholds:
        count = len(curves[threshold])
        max_sep, _ = metrics[threshold]
        if count >= args.min_events and not math.isnan(max_sep) and max_sep <= args.collapse_tolerance:
            recommendation = threshold
            break

    with (args.out_dir / "normalized_curves.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["threshold", "time_original", "time_epoch", "normalized_cumulative"])
        for threshold in thresholds:
            for time_epoch, value, original in curves[threshold]:
                writer.writerow([threshold, original, f"{time_epoch:.6f}", f"{value:.8f}"])

    with (args.out_dir / "threshold_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["threshold", "event_count", "max_curve_separation_from_threshold_up", "median_curve_separation_from_threshold_up"])
        for threshold in thresholds:
            max_sep, med_sep = metrics[threshold]
            writer.writerow([threshold, len(curves[threshold]), max_sep, med_sep])

    plotted = maybe_plot(curves, args.out_dir / "normalized_curves.png")

    with (args.out_dir / "mc_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Mc Normalized Curve Report\n\n")
        handle.write(f"- Catalog: `{args.catalog_csv}`\n")
        handle.write(f"- Events read: {len(events)}\n")
        handle.write(f"- Thresholds: {', '.join(f'{thr:g}' for thr in thresholds)}\n")
        handle.write(f"- Collapse tolerance used for first-pass screening: {args.collapse_tolerance:g}\n")
        handle.write(f"- Minimum events required at threshold: {args.min_events}\n")
        handle.write(f"- First-pass suggested Mc: {recommendation if recommendation is not None else 'not determined'}\n")
        handle.write(f"- Plot written: {'yes' if plotted else 'no, matplotlib unavailable'}\n\n")
        handle.write("Review `normalized_curves.png` and `threshold_summary.csv` before accepting Mc. ")
        handle.write("Use the lowest threshold where all higher-threshold curves nearly collapse and event counts remain adequate.\n")

    print(f"Wrote results to {args.out_dir}")
    if recommendation is not None:
        print(f"First-pass suggested Mc: {recommendation:g}")
    else:
        print("First-pass suggested Mc: not determined")


if __name__ == "__main__":
    main()
