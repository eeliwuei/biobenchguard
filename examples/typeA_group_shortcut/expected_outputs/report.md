# BioBenchGuard audit — crop_wheat_GP (genomic_prediction)

_Rule-based, transparent (not a trained model, not an automated reviewer, not a clinical tool)._

## Per-mechanism status

- **Type G**: `measurable_structure_present` — raw_features=True, structure=relatedness
- **Type A**: `present` — random 0.517 vs structure-aware 0.193 (gap +0.324; eps 0.03)
- **Type B**: `not_tested` — no train-test structure contrast reported
- **Type C**: `present` — flexible - tuned baseline = -0.033 (eps 0.03); 'present' = baseline competitive
- **Type D**: `not_applicable` — no surviving flexible advantage after A/C controls
- **Type E**: `present` — three-arm: selector +0.191, pure-leak +0.036, total +0.227 (eps 0.02)
- **Type F**: `absent_with_sufficient_contrast` — pooled 0.187 vs within-group 0.193 (gap -0.006; eps 0.03)

## Evidence currently supports
- Type A: the artefact is present and was properly measured.  (random 0.517 vs structure-aware 0.193 (gap +0.324; eps 0.03))
- Type C: the artefact is present and was properly measured.  (flexible - tuned baseline = -0.033 (eps 0.03); 'present' = baseline competitive)
- Type E: the artefact is present and was properly measured.  (three-arm: selector +0.191, pure-leak +0.036, total +0.227 (eps 0.02))
- Type F: the artefact was measurable and not detected (true absence in this benchmark).  (pooled 0.187 vs within-group 0.193 (gap -0.006; eps 0.03))

## Evidence does not yet support
- (none flagged)

## Recommended validation design
- Type B: vary structure distance at matched training-N; ensure train-test contrast >= gate before any absence claim.

_'not measurable' is distinct from 'clean'; no production threshold is changed by this audit._
