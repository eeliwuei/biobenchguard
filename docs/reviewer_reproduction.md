# Reviewer reproduction (one page)

**Environment:** CPU-only. Python 3.11 recommended (3.9+ supported). No GPU anywhere. Either local venv or Docker.

```bash
pip install -r requirements.lock && pip install --no-deps -e .   # or: docker build -t biobenchguard:paper .
```

| Step | Command | Expected | Time | Hardware |
|------|---------|----------|------|----------|
| Tests pass | `pytest -q` | 15 passed | < 1 min | CPU |
| Tool runs | `biobenchguard --version` | `BioBenchGuard 0.3.0` | instant | CPU |
| Demo audit | `biobenchguard demo --out demo_results` | report.md/.json written | seconds | CPU |
| Example statuses | `biobenchguard audit examples/typeE_selection_leakage/case.yaml --out r1` | E/A/F = present | seconds | CPU |
| Null is honest | `biobenchguard audit examples/null_degenerate_tdc/case.yaml --out r2` | a `not_measurable` status | seconds | CPU |
| Figures (quick) | `biobenchguard reproduce-figures --quick --out figs` | `repro_typeE_power.png`, `repro_typeA_vs_typeE.png` | seconds | CPU |
| Source data (quick) | `biobenchguard reproduce-results --quick --out res` | 13+ CSVs checksummed, manifest written | seconds | CPU |

**Quick mode** (above) reproduces the headline figures and verifies the locked source data — this is the reviewer path.

**Full mode** recomputes the source data from public raw inputs (`pip install -e ".[full]"`, datasets per
`docs/data_sources.md`, omit `--quick`). It is **CPU-bound and can take hours** on a multicore machine. There is **no
GPU step** anywhere; all models are classic CPU machine learning (linear / GBLUP / random forest).

If a figure or number does not match, check `results_locked/RESULTS_INDEX.md` (figure → source file) and
`source_data/source_data_manifest.csv` (md5).
