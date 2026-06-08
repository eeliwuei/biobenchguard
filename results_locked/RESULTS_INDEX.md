# Results index — current-paper claims only

Each headline figure (rendered PDF in `results_locked/figures/`) maps to md5-locked source data in
`source_data/` (see `source_data_manifest.csv`). Quick reproduction redraws the data-driven panels:
`biobenchguard reproduce-figures --quick`. **Only current benchmark-metrology claims are listed here.** Superseded L2
results are background (bottom of this page; details in [`../AUDIT_TRAIL.md`](../AUDIT_TRAIL.md)).

## Locked figure → data → claim

### Fig 3 — Type E (selection-leakage) operating characteristic
- **Status:** locked.
- **Source data:** `typeE_detector_fp.csv`, `typeE_matched_fpr_power.csv`, `rice_typeE_detector.csv`, `rice_typeE_power.csv`.
- **Scope:** wheat, microbiome CRC, rice RDP1.
- **Claim:** a calibrated threshold controls the false-positive rate toward nominal, but detection **power is
  geometry-dependent** across bases/domains.
- **Boundary:** characterises the detector; does **not** "solve" leakage detection.

### Fig 4 — Leakage-detection limit (LOD)
- **Status:** locked.
- **Source data:** `lod_ci_results.csv`, `lod_power_curves.csv`, `rice_lod_ci.csv`, `rice_lod_curves.csv`.
- **Scope:** wheat, microbiome CRC, rice RDP1.
- **Claim:** a limit of detection **exists** and is orderable (microbiome ≈600 < wheat ≈1000); **rice is
  right-censored** within the tested range.
- **Boundary:** grid-based detection limit, **not** a biological effect size.

### Fig 5 — Type A vs Type E mechanism specificity
- **Status:** locked.
- **Source data:** `typeA_corrected_g3.csv`, `typeA_rice_g3.csv`, `wheat_typeA_g3.csv` (Type A) vs the Type E source above.
- **Scope:** microbiome CRC, microbiome OB, rice RDP1, wheat.
- **Claim:** a **group shortcut drives Type A**; the Type E statistic (C−B) **does not rise and can fall** under a
  group shortcut.
- **Boundary:** Type E is **not** a detector for Type A — different mechanism, different contrast (hence a battery).

### Fig 6 — uncertainty and repeatability/reproducibility
- **Status:** locked.
- **Source data:** `uncertainty_budget_results.csv`, `rr_results.csv`.
- **Claim:** verdicts **near the LOD are unstable**; the data/reference component dominates the uncertainty budget.
- **Boundary:** a **minimal GUM-inspired** budget, **not** a full GUM treatment.

### Fig 7 — A worked example (operating-characteristic read-out)
- **Status:** locked (regenerable from the rule-based engine + locked source tables).
- **Source:** wheat selection-leakage numbers from `source_data/` (floor95 0.234, FPR 0.08, power 0.88 @ L=1,000);
  drug scaffold status from running the engine on `examples/null_degenerate_tdc/`; regenerate with
  `development/.../26_benchmark_metrology_manuscript/figures/make_v10_1_figures.py`. Raw engine report archived as FigS1.
- **Claim:** on a wheat selection-leakage reference the battery reports **Type E = present** (C−B clears its calibrated
  floor; FPR 0.08 at nominal 0.05; power 0.88 at L=1,000), null-validity measurable, supported = selection-leakage /
  unsupported = clean-benchmark; on the singleton-dominated drug scaffold it reports **null-validity = not measurable**
  (Type E absent), withholding a clean verdict — the operating-characteristic report in practice (current vocabulary).
- **Boundary:** a read-out on controlled references of known truth; **no claim** that any published benchmark is wrong.

### TDC scaffold — null-validity boundary
- **Status:** boundary / **not measurable** (see `examples/null_degenerate_tdc/`).
- **Claim:** scaffold grouping is singleton-dominated, so the group-aware null is degenerate and **cannot be
  interpreted as "clean"**.
- **Boundary:** a boundary case, **not** a fully characterised active domain.

## Superseded (background only — not current claims)
- **60% / `37/62` claim-audit headline:** background/motivation only; downgraded (no human gold standard).
- **Calibration sign flip:** **withdrawn** (oracle/observed-scale audit).
- **Binary saturation:** a coding artefact, **corrected**.

These must not reappear as current results. See [`../AUDIT_TRAIL.md`](../AUDIT_TRAIL.md) and
[`GOLDEN_FILES.md`](GOLDEN_FILES.md) (golden tests fail if superseded outputs return).
