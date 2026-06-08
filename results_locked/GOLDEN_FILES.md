# Golden files

"Golden files" are the locked reference outputs that tests compare against, so unintended numerical drift fails loudly.

## What is locked
- **Source data:** the 13 CSVs in `source_data/`, each pinned by md5 in `source_data_manifest.csv`.
- **Figures:** the rendered headline PDFs in `results_locked/figures/` (`Fig1`–`Fig6`).
- **Example statuses:** the expected per-mechanism statuses for the four bundled `case.yaml` examples.

## How the lock is enforced (tests, CPU, deterministic)
- `tests/test_golden_files.py`
  - `test_source_data_md5_matches_golden` — every packaged CSV must match its recorded md5.
  - `test_quick_reproduce_results` — quick reproduction copies are **byte-identical** to the locked source.
  - `test_quick_reproduce_figures` — quick reproduction emits the two headline PNGs, non-empty.
- `tests/test_cli.py`
  - each example audits to its **expected status** (incl. `null_degenerate_tdc` → `not_measurable`);
  - `audit` emits `report.md` + `report.json` with the soft-wording fields.

Run: `pytest -q` → **15 passed**.

## If a golden test fails
1. A red md5 means the source data changed. That is intentional only if a result was deliberately updated — in which
   case update the manifest **and** record the change in `AUDIT_TRAIL.md`. Otherwise it is unintended drift: investigate.
2. A figure test failure usually means a plotting-path change; inspect the emitted PNG under the test's `tmp_path`.

> The locks exist so that "the numbers moved" can never happen silently. Locked ≠ frozen-forever; locked = *changes are
> visible and recorded*.
