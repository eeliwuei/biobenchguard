# BioBenchGuard audit report — livestock_pig_GP (genomic_prediction)

Rule-based, transparent (not a trained model). Status per Type A-G:

- **Type G**: `measurable_structure_present` — raw_features=True, structure=relatedness
- **Type A**: `present` — random 0.722 vs structure-aware 0.279 (gap +0.443; eps 0.03)
- **Type B**: `present_structural` — contrast 0.222 >= gate; matched-N metric 0.700 ~ random 0.722 -> structural, not support
- **Type C**: `present` — flexible - tuned baseline = -0.041 (eps 0.03); 'present' = baseline competitive
- **Type D**: `not_applicable` — no surviving flexible advantage after A/C controls
- **Type E**: `present` — three-arm: selector +0.003, pure-leak +0.117, total +0.120 (eps 0.02)
- **Type F**: `present` — pooled 0.155 vs within-group -0.041 (gap +0.196; eps 0.03)

## Allowed
- Type A: the artefact is present and was properly measured.  (random 0.722 vs structure-aware 0.279 (gap +0.443; eps 0.03))
- Type B: the artefact is present and was properly measured.  (contrast 0.222 >= gate; matched-N metric 0.700 ~ random 0.722 -> structural, not support)
- Type C: the artefact is present and was properly measured.  (flexible - tuned baseline = -0.041 (eps 0.03); 'present' = baseline competitive)
- Type E: the artefact is present and was properly measured.  (three-arm: selector +0.003, pure-leak +0.117, total +0.120 (eps 0.02))
- Type F: the artefact is present and was properly measured.  (pooled 0.155 vs within-group -0.041 (gap +0.196; eps 0.03))

## Forbidden
- (none)

## Recommended validation design
- adequate
