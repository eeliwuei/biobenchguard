# Command reference

All commands are CPU-only and deterministic. Install first: `pip install -r requirements.lock && pip install --no-deps -e .`

| Command | What it does | Key flags | Writes |
|---------|--------------|-----------|--------|
| `biobenchguard demo` | Audit a bundled example end-to-end (quick sanity check). | `--out DIR` | report + matrices under `DIR` |
| `biobenchguard validate CASE` | Check a `case.yaml` against the schema; report missing/!invalid fields. | — | stdout (exit 0 = valid) |
| `biobenchguard audit CASE` | Run the rule-based audit on your benchmark. | `--out DIR` | `report.md`, `report.json`, `feasibility_matrix.csv`, `type_A_to_G_status.csv`, `allowed_claims.md`, `forbidden_claims.md`, `recommended_validation_design.md`, `audit_report.md` |
| `biobenchguard reproduce-figures` | Redraw the paper's headline figures from locked source data. | `--quick`, `--out DIR` | `repro_typeE_power.png`, `repro_typeA_vs_typeE.png` |
| `biobenchguard reproduce-results` | Re-emit and checksum the locked source data. | `--quick`, `--out DIR` | `source_data/` copy + `reproduced_results_manifest.csv` |

## Report wording (deliberate)
`audit` reports describe each mechanism (Type A–G) as one of:
- **evidence currently supports** the artefact is present,
- **does not yet support** its presence (absent *with sufficient contrast*),
- **not measurable** (insufficient contrast / degenerate structure — distinct from "clean"),
and end with a **recommended validation design**. Reports never say a benchmark/paper is "wrong".

## Quick vs full
- `--quick` (default for reviewers): verify packaging + plotting from `source_data/`. Seconds to minutes, CPU-only.
- Full (omit `--quick`): recompute source data from public raw inputs. **CPU-bound, can take hours**; needs the `full`
  extra (`pip install -e ".[full]"`) and the public datasets (see `docs/data_sources.md`). No GPU required.

See `docs/reviewer_reproduction.md` for the one-page reproduction table.
