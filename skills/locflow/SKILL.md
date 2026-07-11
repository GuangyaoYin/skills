---
name: locflow
description: End-to-end LOC-FLOW earthquake catalog processing skill for monthly or campaign-based PhaseNet, REAL, VELEST, hypoDD dtct, FDTCC, and hypoDD dtcc workflows. Use when the user provides new waveform/station metadata or asks to run, audit, QC, tune, plot, or report a LOC-FLOW processing cycle.
---

# LOC-FLOW Processing Skill

This skill manages a complete earthquake catalog processing cycle based on
PhaseNet, REAL, VELEST, hypoDD catalog differential times (`dtct`), FDTCC
cross-correlation differential times, and hypoDD cross-correlation relocation
(`dtcc`).

Use this skill when the user mentions LOC-FLOW, `LOC-FLOW`, PhaseNet, REAL,
VELEST, hypoDD, `ph2dt`, `dtct`, FDTCC, `dtcc`, dense seismic array processing,
monthly earthquake catalog processing, or asks to QC or rerun a catalog workflow.

The goal is not only to run programs. The goal is to produce a defensible,
auditable, reproducible catalog with explicit inputs, parameter snapshots,
quality gates, figures, and stage-by-stage retention statistics.

## Operating Principles

1. Treat every processing month or campaign as an independent project.
2. Put all constants, paths, station counts, date ranges, executable paths,
   velocity models, region bounds, and program parameters in config files.
3. Never hard-code month strings, station counts, absolute paths, or Datong-area
   parameters inside scripts.
4. Station count must be computed from data and final station enable lists. Do
   not assume `569` or any other fixed count.
5. Every stage has an acceptance gate. If the gate fails, stop before the next
   stage, explain the failure, and propose parameter or data fixes.
6. Prefer recall in PhaseNet first-pass picking. Do not raise probability
   thresholds only because raw pick counts are large.
7. Diagnose abnormal travel times at event level before deleting all picks that
   deviate from theoretical curves.
8. Preserve raw data and manually confirmed files. Derived outputs may be
   deleted or overwritten during reruns after recording what changed.
9. Use PyGMT for all maps. Stage-comparison maps in one project must use the
   same map region.
10. For each run, save config snapshots, input manifests, checksums when
    feasible, software versions, logs, figures, summaries, and event retention
    tables.

## Runtime Expectations

When running commands in the user's synchronized personal work directory, follow
the local `AGENTS.md`: use the WSL conda environment `env_py3.11` when the
runtime is available. If running on macOS or another machine, inspect the project
configuration for the correct environment and executable paths.

Before executing external programs, confirm or discover:

- Python/conda environment.
- PhaseNet model and executable command.
- REAL executable path.
- VELEST executable path.
- hypoDD/ph2dt executable paths.
- FDTCC executable path.
- PyGMT/GMT availability.
- Obspy and waveform-processing dependencies.

If any required executable or environment is missing, do not invent paths. Stop
and produce a setup checklist.

## Canonical Project Layout

Each cycle uses:

```text
loc-flow-YYYYMM/
├── config/
├── Data/
├── Pick/
├── REAL/
├── VELEST/
├── hypoDD_dtct/
├── hypoDD_dtcc/
├── plot_dir/
├── logs/
└── workflow_summary/
```

`config/` is the single source of truth. It should contain or generate:

- processing time range
- waveform root and file pattern
- station metadata path
- instrument type mapping rules
- study-region bounds
- velocity model
- PhaseNet parameters
- REAL parameters
- VELEST parameters
- hypoDD dtct parameters
- FDTCC and hypoDD dtcc parameters
- plotting parameters
- environment and executable paths
- catalog policy options, including `dtcc_catalog_policy`

Recommended config file names:

```text
config/project.yaml
config/paths.yaml
config/instruments.yaml
config/region.yaml
config/velocity_model.txt
config/phasenet.yaml
config/real.yaml
config/velest.yaml
config/hypodd_dtct.yaml
config/fdtcc.yaml
config/hypodd_dtcc.yaml
config/plotting.yaml
```

## Standard Stage Directory Contract

Every processing stage should keep only:

```text
config_snapshot/
input_manifest/
formal inputs
formal outputs
results_figure/
summary.txt
run.log
```

For reruns:

- Delete or overwrite old derived results for the same stage.
- Do not delete raw waveform data.
- Do not delete manually confirmed station metadata, analyst-reviewed picks, or
  manually curated catalogs unless the user explicitly requests it.
- Avoid unnamed scratch folders such as `test1`, `new`, `temp-final`, or
  scattered date-specific output directories.

## Stage 0: Project Initialization

When receiving new data:

1. Infer project month and data time range from waveform dates and user-provided
   campaign information.
2. Create `loc-flow-YYYYMM/` or ask before reusing an existing project directory.
3. Create the canonical directory tree.
4. Create initial config files from discovered data and user-provided settings.
5. Store all absolute paths only in config files.
6. Initialize `logs/` and `workflow_summary/`.
7. Write `workflow_summary/project_init_summary.txt`.

Initial summary must include:

- project ID
- time range
- waveform root
- station metadata path
- detected instruments
- study region
- velocity model path
- software paths or missing software checklist

## Stage 1: Raw Data Audit

Audit raw data for every cycle, even if earlier cycles used similar stations.

Inspect:

- stations present in waveform files
- stations present in station metadata
- instrument type and response information
- sampling rates
- channel names
- component orientation
- available time windows per station
- missing dates
- missing components
- three-component start/end consistency
- three-component length consistency
- damaged files
- duplicate files
- abnormal amplitudes
- coordinate consistency
- elevation consistency
- station-name consistency

Generate exactly these station lists:

```text
stations_metadata.txt
stations_waveform_available.txt
stations_processing_enabled.txt
```

Rules:

- All later programs must read `stations_processing_enabled.txt`.
- Do not let later scripts independently infer station sets unless explicitly
  performing a diagnostic comparison.
- Separate excluded stations by reason in an audit table.
- Instrument type should be derived from metadata and response information, not
  station-name prefixes.

Acceptance gate:

- `stations_processing_enabled.txt` exists and has nonzero stations.
- Every enabled station has usable coordinates.
- Enabled stations have enough component/time coverage for the configured task.
- Severe file corruption or station-name mismatch is either fixed or documented.

If the gate fails, stop before waveform standardization.

## Stage 2: Instrument and Waveform Standardization

Standardize by metadata-driven instrument identification.

Normalize:

- sampling rate
- time base
- three-component naming
- file format
- units and polarity
- waveform length
- daily file splitting

Before downsampling:

- Apply anti-alias low-pass filtering.

Instrument response policy is task-controlled:

- PhaseNet: usually use the waveform standardization required by the model.
- Arrival-time cross correlation: for same-station event pairs, response removal
  is often not required, but mean removal, detrending, windowing, and bandpass
  filtering are required.
- Amplitude, magnitude, or cross-instrument waveform comparison: instrument
  response must be considered.

Always report data quality and later residual statistics separately by
instrument type.

Acceptance gate:

- Standardized files cover the configured time range.
- Component naming and length consistency pass for enabled stations.
- Sampling-rate changes record anti-alias parameters.
- Response-removal policy is explicit in config and summary.

## Stage 3: PhaseNet Picking

Recommended initial thresholds:

```text
P_threshold: 0.30
S_threshold: 0.30
```

These are recall-first starting values, not permanent constants.

For every batch, inspect:

- daily pick counts
- hourly pick counts
- station pick rates
- P/S count ratio
- probability distributions
- stations with abnormal high-frequency triggers
- pick differences by instrument type
- later REAL association rate
- relationship between pick probability and arrival-time residuals

Rules:

- Raise thresholds only when noise triggering is demonstrably uncontrolled.
- Do not raise thresholds only because raw pick count is large.
- Keep PhaseNet raw picks and filtered/accepted picks separate.

Acceptance gate:

- Pick volume is plausible relative to station count and time span.
- P/S ratio is not obviously pathological without explanation.
- No small set of stations dominates picks due to noise without flagging.
- Pick files are compatible with REAL input conversion.

If the gate fails, tune PhaseNet preprocessing or thresholds and rerun PhaseNet.

## Stage 4: Velocity Model and Travel-Time Table

Before REAL:

1. Read the initial 1-D velocity model.
2. Check that velocity changes with depth are physically reasonable.
3. Check abnormal low velocities, jumps, and Vp/Vs.
4. Determine travel-time table range from station distances and expected source
   depths.
5. Regenerate travel-time tables.
6. Plot P and S theoretical travel-time curves.

Consistency rule:

- The velocity model, representative velocities used in REAL, and hypoDD model
  must be physically consistent, even if file formats differ.

Acceptance gate:

- Velocity model covers expected depth range.
- P and S curves are plotted.
- Travel-time table range covers study geometry.
- REAL and hypoDD configs cite the same physical model family.

## Stage 5: REAL Association

Recommended initial association parameters:

```text
min_P: 5
min_S: 3
min_P_plus_S: 8
min_same_station_PS: 4
std0: 0.35
dtps: 0.10
nrt: 1.5
drt: 0.35
```

The search range must be computed from the study region and station distribution.
Do not reuse Datong-area parameters blindly.

REAL QC must include:

- daily event counts
- phase counts
- P/S travel-time curves
- association residuals
- station azimuthal gap
- depth boundary piling
- duplicate events
- single-station abnormal contribution
- residual differences by instrument type
- epicenter distribution
- depth distribution

Acceptance gate:

- Event and phase counts are plausible.
- Travel-time residuals have no unexplained systematic offset.
- Depths are not dominated by boundary piles without diagnosis.
- Duplicate events are identified and handled.
- Instrument-specific residual differences are summarized.

If abnormal travel times exist, diagnose by event, station, phase, and instrument
before deleting picks globally.

## Stage 6: VELEST

Input is the REAL catalog and phases after REAL acceptance.

Read from config:

- processing center
- maximum event/station distance
- velocity model
- filtering thresholds

Recommended initial filters:

```text
RMS <= 0.8 s
GAP <= 220 degrees
depth within velocity-model coverage
```

GAP must follow network geometry:

- Dense and well-encircling arrays may tighten to `180 degrees`.
- Linear or one-sided arrays may require `220 degrees` or higher.
- Compare event count, RMS, depth, and spatial distribution before and after any
  GAP change.

VELEST QC must include:

- location changes before and after VELEST
- RMS distribution
- GAP distribution
- depth changes and boundary piling
- P residuals
- S residuals
- station residuals
- residuals by instrument type
- event retention at each filter step

Acceptance gate:

- RMS and GAP distributions improve or are scientifically explainable.
- Location shifts are plausible.
- Depth boundary piling is documented and not blindly accepted.
- Station residual outliers are diagnosed.

## Stage 7: hypoDD dtct

Recommended initial `ph2dt` parameters:

```text
MAXDIST: 150 km
MAXSEP: 12 km
MAXNGH: 30
MINLNK: 8
MINOBS: 8
MAXOBS: 40
```

Adjust by catalog geometry:

- Small dense clusters should use smaller `MAXSEP`.
- Sparse catalogs may require larger `MAXSEP` and `MAXNGH`.
- Too-high `MINOBS` can discard many events.
- Too-low `MINOBS` can produce weakly constrained small clusters.

QC must inspect:

- event-pair count
- main-cluster fraction
- catalog residuals
- formal errors
- relocation displacement from previous stage
- weakly connected clusters

Acceptance gate:

- Main cluster and subclusters are interpretable.
- Retention is not catastrophically low without explanation.
- Formal errors and displacement distributions are plausible.

## Stage 8: FDTCC and hypoDD dtcc

For each event, cut P and S waveform windows using theoretical or catalog arrival
times.

Standard preprocessing:

- remove mean
- detrend
- taper
- bandpass filter
- resample if needed
- check component and polarity
- calculate SNR

Recommended FDTCC initial thresholds:

```text
CC >= 0.55
SNR >= 2
abs(dtcc - dtct) <= 1.0 s
```

Recommended event-pair settings:

```text
MAXDIST: 120 km
MAXSEP: 12 km
MAXNGH: 50
MINLNK: 8
MINOBS: 8
MAXOBS: 100
OBSCC: 6
```

Report separately by instrument type:

- P cross-correlation observation count
- S cross-correlation observation count
- CC distribution
- differential-time distribution
- SNR distribution
- rejected fraction
- final event connectivity

`dtcc_catalog_policy` must come from config. Allowed values:

- `raw`: use all successfully relocated events.
- `qc`: use only main-cluster events satisfying error thresholds.
- `both`: main result uses `raw`, while QC catalog is also exported.

Current user projects may choose `raw`, but this skill must not hard-code it.

Acceptance gate:

- CC and SNR distributions support the chosen thresholds.
- Rejected fraction is explainable by data quality, station coverage, or
  instrument type.
- Final event connectivity is sufficient for the target catalog.
- Final catalog policy is recorded in config and summary.

## Plotting Requirements

Each stage writes plots to its own `results_figure/`.

Final selected figures are collected in:

```text
plot_dir/results_figure/
```

Standard figures:

- velocity model
- station and instrument-type distribution
- PhaseNet QC figures
- REAL travel-time curves
- REAL event-quality figures
- VELEST residuals and location-change figures
- dtct connectivity, residual, and error figures
- FDTCC cross-correlation QC figures
- dtcc horizontal and vertical location-error figures
- stage-by-stage epicenter distribution panels
- stage-by-stage depth-section panels
- event-retention workflow chart

Map rules:

- Use PyGMT for all maps.
- Map region is read from config.
- Stage-comparison maps in the same project must use exactly the same region.
- Figures must annotate event count, stage name, time range, and necessary QC
  conditions.

## Workflow Report Contract

At the end of each accepted stage, update:

```text
workflow_summary/stage_retention_table.csv
workflow_summary/stage_quality_summary.md
workflow_summary/parameter_change_log.md
workflow_summary/software_versions.txt
workflow_summary/input_manifest_checksums.txt
```

At the end of the full workflow, produce:

```text
workflow_summary/final_report.md
workflow_summary/final_catalog_manifest.txt
workflow_summary/final_event_retention_table.csv
workflow_summary/final_parameter_snapshot/
```

The final report must include:

- project ID and time range
- enabled station count computed from data
- instrument-type summary
- velocity model summary
- PhaseNet thresholds and QC
- REAL parameters, event counts, and QC
- VELEST filters, retained events, and residuals
- dtct parameters, pair counts, clusters, and errors
- FDTCC thresholds and observation counts
- dtcc catalog policy and retained events
- stage-by-stage retention rates
- figure index
- warnings and unresolved limitations
- recommended next parameter adjustments

## Required Assistant Behavior

When the user provides new data, the assistant should:

1. Identify project month and data range.
2. Audit waveforms, station metadata, and instruments.
3. Build the unified station processing list.
4. Decide whether PhaseNet needs to be rerun.
5. Check the velocity model and regenerate travel-time tables.
6. Run REAL only after PhaseNet and velocity-model gates pass.
7. Run VELEST only after REAL acceptance.
8. Run hypoDD dtct only after VELEST acceptance.
9. Run FDTCC and hypoDD dtcc only after dtct acceptance and waveform-window QC.
10. Perform quality diagnostics at every stage.
11. Suggest parameter changes when QC fails.
12. Stop before the next stage when acceptance fails.
13. Overwrite/update formal derived results and figures when rerunning.
14. Preserve raw data and manually confirmed files.
15. Output a complete workflow report, parameter snapshots, and event-retention
    statistics.

## Common Stop Conditions

Stop and ask for user input or produce a fix checklist when:

- station metadata is missing or inconsistent with waveform stations
- enabled station list is empty or scientifically unusable
- executable paths are missing
- velocity model does not cover expected depths
- PhaseNet picks are dominated by obvious noise stations
- REAL produces severe unexplained travel-time anomalies
- VELEST relocation collapses to boundary depths
- dtct or dtcc connectivity is too weak for the target catalog
- final catalog policy is missing
- requested deletion would affect raw data or manually curated files

## Do Not Do

- Do not hard-code station count, especially `569`.
- Do not scatter absolute paths across scripts.
- Do not carry one month's search bounds into another project without checking
  region and station geometry.
- Do not treat high PhaseNet pick volume as failure by itself.
- Do not delete all off-curve picks without event-level diagnosis.
- Do not mix raw and derived outputs without manifests.
- Do not use inconsistent map extents for stage-comparison figures.
- Do not silently advance to the next stage after failed QC.
- Do not hard-code `dtcc_catalog_policy: raw`.
