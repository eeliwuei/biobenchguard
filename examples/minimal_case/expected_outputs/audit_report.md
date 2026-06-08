# BioBenchGuard audit report — microbiome_crc_loso (microbiome)

Rule-based, transparent (not a trained model). Status per Type A-G:

- **Type G**: `measurable_structure_present` — raw_features=True, structure=study
- **Type A**: `absent_with_sufficient_contrast` — random 0.810 vs structure-aware 0.790 (gap +0.020; eps 0.03)
- **Type B**: `not_tested` — no train-test structure contrast reported
- **Type C**: `absent_with_sufficient_contrast` — flexible - tuned baseline = +0.244 (eps 0.03); 'present' = baseline competitive
- **Type D**: `not_applicable` — no surviving flexible advantage after A/C controls
- **Type E**: `present` — three-arm: selector +0.063, pure-leak +0.054, total +0.117 (eps 0.02)
- **Type F**: `absent_with_sufficient_contrast` — pooled 0.765 vs within-group 0.790 (gap -0.025; eps 0.03)

## Allowed
- Type A: the artefact was measurable and not detected (true absence in this benchmark).  (random 0.810 vs structure-aware 0.790 (gap +0.020; eps 0.03))
- Type C: the artefact was measurable and not detected (true absence in this benchmark).  (flexible - tuned baseline = +0.244 (eps 0.03); 'present' = baseline competitive)
- Type E: the artefact is present and was properly measured.  (three-arm: selector +0.063, pure-leak +0.054, total +0.117 (eps 0.02))
- Type F: the artefact was measurable and not detected (true absence in this benchmark).  (pooled 0.765 vs within-group 0.790 (gap -0.025; eps 0.03))

## Forbidden
- (none)

## Recommended validation design
- Type B: vary structure distance at matched training-N; ensure train-test contrast >= gate before any absence claim.
