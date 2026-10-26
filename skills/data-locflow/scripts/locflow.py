#!/usr/bin/env python3
"""Input and catalogue acceptance tools for the data-locflow specification.

Uses only the Python standard library. This does not invoke scientific backends.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys


STAGES = [
    ("00_inputs", [], "waveform_index.csv, station_epochs.csv, response_index.csv, input_manifest.json"),
    ("01_waveforms", ["00_inputs"], "waveform_qc.csv, waveform_index_normalized.csv"),
    ("02_picks", ["01_waveforms"], "picks.csv, pick_qc.csv"),
    ("03_association", ["02_picks"], "events_real.csv, event_picks.csv, association_qc.csv"),
    ("04_absolute", ["03_association"], "events_absolute.csv, residuals_absolute.csv"),
    ("05_dd_catalog", ["04_absolute"], "events_dtct.csv, dt.ct, pair_qc.csv"),
    ("06_correlation", ["05_dd_catalog"], "dt.cc, correlation_qc.csv, pair_batch_manifest.json"),
    ("07_dd_cc", ["06_correlation"], "events_dtcc.csv, residuals_dtcc.csv, rejected_events.csv"),
    ("08_magnitude", ["07_dd_cc"], "station_magnitudes.csv, event_magnitudes.csv"),
    ("09_uncertainty", ["07_dd_cc"], "location_uncertainty.csv, perturbation_manifest.json, sensitivity.csv"),
    ("10_catalog", ["08_magnitude", "09_uncertainty"], "catalog_all.csv, catalog_high_precision.csv, catalog_manifest.json"),
    ("11_figures", ["10_catalog"], "figure_manifest.json, numbered PNG/TXT/JSON/TSV files"),
    ("12_acceptance", ["11_figures"], "acceptance.json, run_summary.md"),
]
CORE_FIELDS = ["event_uid", "origin_time_utc", "latitude", "longitude", "depth_km",
               "catalog_source", "final_relocation_stage",
               "location_qc", "magnitude_qc"]


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def instant(value: str) -> datetime:
    out = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if out.tzinfo is None or out.utcoffset() is None:
        raise ValueError("time requires an explicit timezone offset")
    return out.astimezone(timezone.utc)


def finite(value: str | float) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise ValueError("nonfinite number")
    return out


def validate_region(region):
    if len(region) != 4:
        raise ValueError("region needs west, east, south, north")
    west, east, south, north = map(finite, region)
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise ValueError("invalid geographic region")
    return west, east, south, north


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames or [], list(reader)


def result(kind: str, path: Path | None = None) -> dict:
    return {"check": kind, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "path": str(path.resolve()) if path else None, "errors": [], "warnings": []}


def finish(report: dict) -> dict:
    report["passed"] = not report["errors"]
    return report


def audit_catalog(path: Path, region=None, expected_count=None, expected_sources=None,
                  magnitude_column="magnitude", magnitude_type_column="magnitude_type",
                  default_magnitude_type=None) -> dict:
    report = result("catalogue_acceptance", path)
    if region is not None:
        try:
            region = validate_region(region)
        except (ValueError, TypeError) as exc:
            report["errors"].append(str(exc))
            return finish(report)
    report["sha256"] = sha256(path)
    fields, rows = read_csv(path)
    if len(set(fields)) != len(fields):
        report["errors"].append("duplicate CSV column names")
    report["records"] = len(rows)
    required = [*CORE_FIELDS, magnitude_column]
    if default_magnitude_type is None:
        required.append(magnitude_type_column)
    missing = sorted(set(required) - set(fields))
    if missing:
        report["errors"].append({"missing_columns": missing})
        return finish(report)
    if not rows:
        report["errors"].append("empty catalogue")
    if expected_count is not None and len(rows) != expected_count:
        report["errors"].append({"expected_records": expected_count, "actual": len(rows)})
    identifiers, identities, counts, stages, times = set(), set(), Counter(), Counter(), []
    invalid, duplicate_ids, duplicate_origins, outside = [], [], [], []
    magnitude_values, negative_depth, uncertainty_counts = {}, 0, Counter()
    for line, row in enumerate(rows, start=2):
        if None in row or any(row.get(key) is None for key in required):
            invalid.append({"line": line, "reason": "malformed CSV row: missing or extra fields"})
            continue
        uid = row["event_uid"].strip()
        if not uid or uid in identifiers:
            duplicate_ids.append(line)
        identifiers.add(uid)
        try:
            time = instant(row["origin_time_utc"])
            lat, lon, dep, mag = (finite(row[k]) for k in
                                  ("latitude", "longitude", "depth_km", magnitude_column))
            mag_type = (row.get(magnitude_type_column) or "").strip() or default_magnitude_type
            if not mag_type or not str(mag_type).strip():
                raise ValueError("magnitude type is missing; declare it explicitly")
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("geographic coordinate out of range")
            times.append(time)
            magnitude_values.setdefault(mag_type, []).append(mag)
            negative_depth += dep < 0
            key = (time, lat, lon, dep)
            if key in identities:
                duplicate_origins.append(line)
            identities.add(key)
            if region and not (region[0] <= lon <= region[1] and region[2] <= lat <= region[3]):
                outside.append(uid)
        except (ValueError, TypeError) as exc:
            invalid.append({"line": line, "event_uid": uid, "reason": str(exc)})
        for key in ("catalog_source", "final_relocation_stage", "location_qc", "magnitude_qc"):
            if not row[key].strip():
                invalid.append({"line": line, "event_uid": uid, "reason": f"blank {key}"})
        counts[row["catalog_source"]] += 1
        stages[row["final_relocation_stage"]] += 1
        method = (row.get("uncertainty_method") or "").strip()
        uncertainty_counts[method or "not_declared_in_this_file"] += 1
    for label, entries in (("invalid_rows", invalid), ("blank_or_duplicate_uid_lines", duplicate_ids),
                           ("exact_duplicate_origin_location_depth_lines", duplicate_origins)):
        if entries:
            report["errors"].append({label: entries[:20], "count": len(entries)})
    if outside:
        report["errors"].append({"outside_region": outside[:20], "count": len(outside)})
    if negative_depth:
        report["warnings"].append({"negative_depth_records": negative_depth,
                                   "action": "verify depth datum; do not silently truncate"})
    if uncertainty_counts["not_declared_in_this_file"]:
        report["warnings"].append("This table alone does not establish location accuracy; join method-tagged uncertainty and sensitivity results. ex_m/ey_m/ez_m are not automatically bootstrap errors.")
    report["source_counts"] = dict(counts)
    report["relocation_stage_counts"] = dict(stages)
    report["uncertainty_method_counts"] = dict(uncertainty_counts)
    report["time_range_utc"] = [min(times).isoformat(), max(times).isoformat()] if times else None
    report["magnitude_column"] = magnitude_column
    report["magnitude_type_column"] = magnitude_type_column
    report["declared_default_magnitude_type"] = default_magnitude_type
    report["magnitude_ranges_by_type"] = {kind: [min(values), max(values)] for kind, values in magnitude_values.items()}
    report["magnitude_counts_by_type"] = {kind: len(values) for kind, values in magnitude_values.items()}
    if expected_sources is not None and dict(counts) != expected_sources:
        report["errors"].append({"expected_source_counts": expected_sources, "actual": dict(counts)})
    report["interpretation"] = "Schema and consistency acceptance only; passing does not prove a high-precision catalogue."
    return finish(report)


def check_travel_table(path: Path, grid: dict) -> dict:
    report = result("travel_time_grid", path)
    report["sha256"] = sha256(path)
    dx, dz = finite(grid["distance_step_deg"]), finite(grid["depth_step_km"])
    xmax, zmax = finite(grid["distance_max_deg"]), finite(grid["depth_max_km"])
    if min(dx, dz, xmax) <= 0 or zmax < 0:
        raise ValueError("grid steps and distance extent must be positive; depth extent nonnegative")
    nx, nz = round(xmax / dx), round(zmax / dz)
    if not math.isclose(nx * dx, xmax, abs_tol=1e-8) or not math.isclose(nz * dz, zmax, abs_tol=1e-8):
        raise ValueError("grid extents must be integer multiples of steps")
    expected = [(round(ix * dx, 8), round(iz * dz, 8))
                for iz in range(nz + 1) for ix in range(1, nx + 1)]
    actual, invalid = [], []
    with path.open() as stream:
        for line, text in enumerate(stream, start=1):
            if not text.strip() or text.lstrip().startswith("#"):
                continue
            try:
                parts = text.split()
                x, z, tp, ts = map(finite, parts[:4])
                if len(parts) != 10 or parts[8] not in ("P", "p") or parts[9] not in ("S", "s") or not (tp > 0 and ts > tp):
                    raise ValueError("requires 8 numeric fields, P/p and S/s phase names, and 0 < tp < ts")
                list(map(finite, parts[4:8]))
                actual.append((round(x, 8), round(z, 8)))
            except (ValueError, TypeError) as exc:
                invalid.append({"line": line, "reason": str(exc)})
    report.update({"expected_grid": grid, "expected_rows": len(expected), "actual_rows": len(actual),
                   "actual_distance_nodes": len({x for x, _ in actual}),
                   "actual_depth_nodes": len({z for _, z in actual})})
    if actual:
        report["actual_bounds"] = {"distance_deg": [min(x for x, _ in actual), max(x for x, _ in actual)],
                                    "depth_km": [min(z for _, z in actual), max(z for _, z in actual)]}
    if invalid:
        report["errors"].append({"invalid_rows": invalid[:20], "count": len(invalid)})
    if actual != expected:
        report["errors"].append({"grid_or_row_order_mismatch": True,
                                   "missing_nodes": len(set(expected) - set(actual)),
                                   "extra_nodes": len(set(actual) - set(expected)),
                                   "duplicate_nodes": len(actual) - len(set(actual))})
    report["index_convention"] = "REAL/FDTCC 10-column adapter: depth-major; distances start at one positive step, not zero"
    return finish(report)


def check_hypodd_model(path: Path) -> dict:
    report = result("hypodd_layer_model", path)
    report["sha256"] = sha256(path)
    lines = path.read_text().splitlines()
    def following(marker: str):
        for i, text in enumerate(lines):
            if re.match(marker, text.strip(), flags=re.IGNORECASE):
                for value in lines[i + 1:]:
                    if value.strip() and not value.lstrip().startswith("*"):
                        return value.split()
        raise ValueError(f"model marker missing: {marker}")
    nlay, ratio = following(r"\*\s*NLAY\s+RATIO\b")[:2]
    top = list(map(finite, following(r"\*\s*TOP\s*$")))
    vel = list(map(finite, following(r"\*\s*VEL\s*$")))
    nlay = int(nlay)
    ratio = finite(ratio)
    report.update({"declared_layers": nlay, "top_values": len(top), "velocity_values": len(vel),
                   "vp_vs_ratio": ratio})
    if len(top) != nlay or len(vel) != nlay:
        report["errors"].append("NLAY must equal both TOP and VEL lengths; implicit ignored trailing layers are forbidden")
    if not top or any(b <= a for a, b in zip(top, top[1:])) or any(v <= 0 for v in vel) or ratio <= 1:
        report["errors"].append("invalid depth order, velocity, or Vp/Vs ratio")
    return finish(report)


def resolve(config_file: Path, value: str) -> Path:
    out = Path(value).expanduser()
    return out.resolve() if out.is_absolute() else (config_file.parent / out).resolve()


def unresolved_configuration(config: dict) -> list[str]:
    """Required project inputs must never fall back to a particular case study."""
    keys = ["project.start_time_utc", "project.end_time_utc",
            "project.region_west_east_south_north", "project.coordinate_datum",
            "project.depth_datum", "project.waveform_time_basis",
            "inputs.waveforms.path", "inputs.waveforms.glob", "inputs.stations.path",
            "inputs.velocity_model.path"]
    if config.get("magnitude", {}).get("enabled"):
        keys.append("inputs.responses.path")
    missing = []
    for key in keys:
        value = config
        for part in key.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if value is None or value == "" or value == []:
            missing.append(key)
    return missing


def preflight(config_file: Path, header_limit: int = 0) -> dict:
    config = json.loads(config_file.read_text())
    report = result("workflow_preflight", config_file)
    report["config_sha256"] = sha256(config_file)
    unresolved = unresolved_configuration(config)
    if unresolved:
        report["errors"].append({"required_project_configuration": unresolved})
        report["implementation_status"] = "preflight utility; no scientific backend has been launched"
        return finish(report)
    inputs = config["inputs"]
    checks = []
    for key in ("waveforms", "stations", "velocity_model"):
        path = resolve(config_file, inputs[key]["path"])
        if not path.exists():
            report["errors"].append(f"missing {key}: {path}")
        elif key == "waveforms" and not path.is_dir():
            report["errors"].append(f"waveforms must be a directory: {path}")
        elif key != "waveforms" and not path.is_file():
            report["errors"].append(f"{key} must be a CSV file: {path}")
    try:
        start, end = instant(config["project"]["start_time_utc"]), instant(config["project"]["end_time_utc"])
    except (ValueError, TypeError, AttributeError) as exc:
        report["errors"].append(f"invalid project time: {exc}")
        return finish(report)
    if start >= end:
        report["errors"].append("project start must precede end (half-open interval)")
    try:
        validate_region(config["project"]["region_west_east_south_north"])
    except (ValueError, TypeError) as exc:
        report["errors"].append(str(exc))
    station_path = resolve(config_file, inputs["stations"]["path"])
    station_rows, station_keys = [], set()
    if station_path.is_file():
        fields, station_rows = read_csv(station_path)
        required = {"network", "station", "latitude", "longitude", "elevation_m", "start_time_utc", "end_time_utc"}
        if not required.issubset(fields):
            report["errors"].append({"station_missing_columns": sorted(required-set(fields))})
        else:
            epochs = {}
            for line, row in enumerate(station_rows, 2):
                try:
                    if None in row or any(row.get(key) is None for key in required):
                        raise ValueError("malformed station CSV row")
                    lat, lon, _ = [finite(row[k]) for k in ("latitude", "longitude", "elevation_m")]
                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                        raise ValueError("station coordinate out of range")
                    key = (row["network"].strip(), row["station"].strip())
                    if not all(key):
                        raise ValueError("blank network/station")
                    first, last = instant(row["start_time_utc"]), instant(row["end_time_utc"])
                    if first >= last:
                        raise ValueError("empty deployment epoch")
                    for previous_first, previous_last in epochs.get(key, []):
                        if max(first, previous_first) < min(last, previous_last):
                            raise ValueError("overlapping deployment epochs for the same station")
                    epochs.setdefault(key, []).append((first, last))
                    if max(first, start) < min(last, end):
                        station_keys.add(key)
                except (ValueError, TypeError) as exc:
                    report["errors"].append(f"station row {line}: {exc}")
            if not station_keys:
                report["errors"].append("no station deployment intersects the project interval")
    model_path = resolve(config_file, inputs["velocity_model"]["path"])
    if model_path.is_file():
        fields, rows = read_csv(model_path)
        needed = {"top_depth_km", "vp_km_s", "vs_km_s"}
        if not needed.issubset(fields):
            report["errors"].append("canonical velocity model must be CSV: top_depth_km,vp_km_s,vs_km_s")
        else:
            try:
                layers = [(finite(r["top_depth_km"]), finite(r["vp_km_s"]), finite(r["vs_km_s"])) for r in rows]
                if not layers or layers[0][0] != 0 or any(b[0] <= a[0] for a,b in zip(layers,layers[1:])) or any(not (vp>vs>0) for _,vp,vs in layers):
                    raise ValueError("model requires first top at 0, strictly increasing tops and Vp > Vs > 0")
                report["velocity_layers"] = len(layers)
            except (ValueError, TypeError) as exc:
                report["errors"].append(f"velocity model: {exc}")
    magnitude = config["magnitude"]
    if magnitude["enabled"]:
        response_path = resolve(config_file, inputs["responses"]["path"])
        if not response_path.exists():
            report["errors"].append(f"magnitude requires response metadata: {response_path}")
        if not magnitude["calibration"]["validated_for_project"]:
            report["errors"].append("magnitude calibration has not been validated for this project")
        report["warnings"].append("Response path existence is not channel/epoch/unit validation. The waveform adapter must validate every measured channel before magnitude acceptance.")
    waveform_path = resolve(config_file, inputs["waveforms"]["path"])
    candidates = sorted(p for p in waveform_path.glob(inputs["waveforms"]["glob"]) if p.is_file()) if waveform_path.is_dir() else []
    report["waveform_files_found"] = len(candidates)
    report["waveform_header_files_checked"] = 0
    if waveform_path.exists() and not candidates:
        report["errors"].append("no waveform files match the configured directory/glob")
    if header_limit:
        try:
            from obspy import read
            for path in candidates[:header_limit] if header_limit > 0 else candidates:
                try:
                    stream = read(str(path), headonly=True)
                    if not stream:
                        raise ValueError("empty waveform stream")
                    for trace in stream:
                        key = (trace.stats.network, trace.stats.station)
                        if key not in station_keys:
                            raise ValueError(f"waveform network/station not in active metadata: {key}")
                        if trace.stats.sampling_rate <= 0 or trace.stats.npts <= 0:
                            raise ValueError("nonpositive sampling rate/npts")
                        t0 = trace.stats.starttime.datetime.replace(tzinfo=timezone.utc)
                        t1 = trace.stats.endtime.datetime.replace(tzinfo=timezone.utc)
                        if not any(ef <= t0 and t1 < el for ef,el in epochs[key]):
                            raise ValueError("trace crosses or lies outside a station deployment epoch")
                    report["waveform_header_files_checked"] += 1
                except Exception as exc:
                    report["errors"].append(f"waveform header {path}: {exc}")
        except ImportError:
            report["errors"].append("--header-limit requires ObsPy; header check was not performed")
    else:
        report["warnings"].append("Waveform headers have not been inspected; use --header-limit -1 for all files. No amplitude, gap, clipping or orientation acceptance is claimed.")
    for name, method, params in (
        ("travel_table", check_travel_table, config["travel_time_grid"]),
        ("hypodd_input", check_hypodd_model, None),
    ):
        value = inputs.get(name)
        if value and value.get("path"):
            path = resolve(config_file, value["path"])
            if not path.is_file():
                report["errors"].append(f"missing {name}: {path}")
            else:
                check = method(path, params) if params is not None else method(path)
                checks.append(check)
                if not check["passed"]:
                    report["errors"].append(f"{name} check failed; see subchecks")
    report["subchecks"] = checks
    report["implementation_status"] = "preflight utility; scientific backend adapters are not implemented by this command"
    return finish(report)


def build_plan(config_file: Path) -> dict:
    config = json.loads(config_file.read_text())
    return {"project": config["project"], "config_sha256": sha256(config_file),
            "execution": "design only; this command never launches scientific backends",
            "unresolved_project_inputs": unresolved_configuration(config),
            "stages": [{"id": name, "depends_on": deps, "outputs": outputs,
                        "cache_key_requires": ["input hashes", "resolved parameters", "backend executable hashes", "adapter version"],
                        "completion": "zero exit status AND nonempty parsed products AND scientific acceptance"}
                       for name, deps, outputs in STAGES],
            "optional_extensions": ["template matching with local relocation and deduplication", "external catalogue validation", "geology and fault overlays"],
            "scope_note": "Template matching is a separate optional branch; uncertainty must be recomputed per final location source."}


def emit(report: dict, output: Path | None):
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text)
        status = ('PASS' if report['passed'] else 'FAIL') if 'passed' in report else 'WRITTEN'
        print(f"{output}: {status}")
    else:
        print(text, end="")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("plan", "preflight"):
        p = sub.add_parser(command)
        p.add_argument("--config", type=Path, required=True)
        p.add_argument("--output", type=Path)
        if command == "preflight":
            p.add_argument("--header-limit", type=int, default=0, help="0: none; N>0: first N files; -1: all files")
    p = sub.add_parser("audit-catalog")
    p.add_argument("--catalog", type=Path, required=True)
    p.add_argument("--region", nargs=4, type=float)
    p.add_argument("--expected-count", type=int)
    p.add_argument("--expected-sources", help="Optional JSON object of source counts; no fixed sources or counts")
    p.add_argument("--magnitude-column", default="magnitude")
    p.add_argument("--magnitude-type-column", default="magnitude_type")
    p.add_argument("--default-magnitude-type", help="Explicit fallback for source tables without magnitude-type metadata")
    p.add_argument("--output", type=Path)
    p = sub.add_parser("check-travel-table")
    p.add_argument("--table", type=Path, required=True)
    for option in ("distance-max-deg", "distance-step-deg", "depth-max-km", "depth-step-km"):
        p.add_argument(f"--{option}", type=float, required=True)
    p.add_argument("--output", type=Path)
    p = sub.add_parser("check-hypodd-model")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            report = build_plan(args.config)
        elif args.command == "preflight":
            if args.header_limit < -1:
                raise ValueError("header limit must be -1, 0, or positive")
            report = preflight(args.config, args.header_limit)
        elif args.command == "audit-catalog":
            report = audit_catalog(args.catalog, args.region, args.expected_count,
                                   json.loads(args.expected_sources) if args.expected_sources else None,
                                   args.magnitude_column, args.magnitude_type_column,
                                   args.default_magnitude_type)
        elif args.command == "check-travel-table":
            grid = {key: getattr(args, key) for key in ("distance_max_deg", "distance_step_deg", "depth_max_km", "depth_step_km")}
            report = check_travel_table(args.table, grid)
        else:
            report = check_hypodd_model(args.input)
        emit(report, args.output)
        return 0 if report.get("passed", True) else 2
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
