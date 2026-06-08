# Source data (locked)

Derived numerical data behind the manuscript's headline figures. Each file is **md5-pinned** in
`source_data_manifest.csv`; `biobenchguard reproduce-results --quick` re-emits and checksums them, and
`tests/test_golden_files.py` fails on drift.

These are **our derived outputs** (Apache-2.0), not third-party raw data. Raw public datasets are fetched on demand by
`scripts/download_public_data.py` and are **not** vendored here (see `docs/data_sources.md`).

## Files
| File | Rows×Cols | Behind |
|------|-----------|--------|
| `typeE_detector_fp.csv` | 2×6 | Type E false-positive rate (detector under the null) |
| `typeE_matched_fpr_power.csv` | 24×5 | Type E power at matched FPR across bases/domains |
| `rice_typeE_detector.csv` | 1×4 | Rice Type E detector summary |
| `rice_typeE_power.csv` | 12×8 | Rice Type E power curve (right-censored LOD) |
| `lod_ci_results.csv` | 6×6 | Limit-of-detection point + CI (microbiome/wheat) |
| `lod_power_curves.csv` | 12×5 | LOD power-vs-effect curves |
| `rice_lod_ci.csv` | 3×6 | Rice LOD CI (right-censored) |
| `rice_lod_curves.csv` | 6×5 | Rice LOD curves |
| `typeA_corrected_g3.csv` | 18×8 | Type A (group shortcut) corrected, g=3 |
| `typeA_rice_g3.csv` | 6×9 | Type A rice, g=3 |
| `wheat_typeA_g3.csv` | 6×9 | Wheat Type A, g=3 (v8 coverage expansion) |
| `uncertainty_budget_results.csv` | 6×8 | Uncertainty budget |
| `rr_results.csv` | 4×9 | Reproducibility / robustness summary |

Figure → file mapping: `results_locked/RESULTS_INDEX.md`. Lock policy: `results_locked/GOLDEN_FILES.md`.
