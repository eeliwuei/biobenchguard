# BioBenchGuard audit report — tdc_bbb_martins_scaffold (drug)

Rule-based, transparent (not a trained model). Status per Type A-G:

- **Type G**: `measurable_structure_present` — raw_features=True, structure=scaffold
- **Type A**: `absent_with_sufficient_contrast` — random 0.921 vs structure-aware 0.905 (gap +0.016; eps 0.03)
- **Type B**: `not_tested` — no train-test structure contrast reported
- **Type C**: `absent_with_sufficient_contrast` — flexible - tuned baseline = +0.031 (eps 0.03); 'present' = baseline competitive
- **Type D**: `not_applicable` — no surviving flexible advantage after A/C controls
- **Type E**: `absent_with_sufficient_contrast` — three-arm: selector -0.027, pure-leak +0.004, total -0.023 (eps 0.02)
- **Type F**: `not_measurable_low_coverage` — only 1 group(s) with >= 30 units: within-group metric not reliably measurable

## Allowed
- Type A: the artefact was measurable and not detected (true absence in this benchmark).  (random 0.921 vs structure-aware 0.905 (gap +0.016; eps 0.03))
- Type C: the artefact was measurable and not detected (true absence in this benchmark).  (flexible - tuned baseline = +0.031 (eps 0.03); 'present' = baseline competitive)
- Type E: the artefact was measurable and not detected (true absence in this benchmark).  (three-arm: selector -0.027, pure-leak +0.004, total -0.023 (eps 0.02))

## Forbidden
- Type F: do NOT report the within-group metric as a finding (too few groups).  (only 1 group(s) with >= 30 units: within-group metric not reliably measurable)

## Recommended validation design
- Type B: vary structure distance at matched training-N; ensure train-test contrast >= gate before any absence claim.
- Type F: report pooled AND within-group metrics over groups with sufficient units.
