# BioBenchGuard input schema (`case.yaml`)

One YAML file describes one benchmark/claim. It consolidates the six logical inputs (dataset metadata, group
structure, split metadata, baseline config, preprocessing log, results). All fields optional; missing fields make the
relevant artefact `not_tested` / `not_measurable` rather than guessed. **The tool never invents data.**

```yaml
name: <string>
domain: <string>                 # genomic_prediction | protein | drug | microbiome | human_prs | ...
thresholds:                      # optional overrides of the explicit gate constants
  tau_contrast: 0.05             # Type B structure-contrast gate
  collapse_eps: 0.03             # Type A material random-vs-structure gap
  baseline_eps: 0.03             # Type C baseline-competitiveness band
  leak_eps: 0.02                 # Type E material leakage
  typef_min_group: 30            # Type F minimum units/group
  typef_eps: 0.03                # Type F material pooled-vs-within gap
dataset_metadata:
  raw_features_available: bool   # raw genotypes/sequences/SMILES/taxa (gates Type E)
  labels_available: bool
  structure_axis: relatedness|family|scaffold|target|study|ancestry|environment|none
  evidence_tier: raw|matrix_only|summary_level|score_only
  n_units: int
group_structure:
  n_groups: int
  min_group_size: int
  groups_with_ge_min: int        # #groups with >= typef_min_group units (Type F coverage)
split_metadata:
  split_type: random|structure_aware|scaffold|leave_study_out|cold_target|leave_cluster|leave_family|leave_environment|cross_ancestry|none
  structure_contrast: float|null # train-test relatedness/scaffold/study contrast (Type B gate)
  matched_n_reported: bool
  sample_size_coupling: confounded_with_n|decoupled|null   # used when no numeric contrast
baseline_config:
  tuned_baseline_present: bool
  baseline_name: <string>
preprocessing_log:
  feature_selection: none|within_fold|full_data|unknown    # full_data => leak
  duplicate_control: bool
  global_scaling_before_split: bool
results:
  random_metric: float|null
  structure_aware_metric: float|null
  matched_n_metric: float|null
  pooled_metric: float|null
  within_group_metric: float|null
  flexible_minus_baseline: float|null      # flexible model minus tuned baseline (strict regime)
  three_arm:                               # optional matched three-arm (Type E)
    clean_variance: float
    clean_supervised: float
    leaky_supervised: float
```

Outputs (written to `<case_dir>/output/`): `feasibility_matrix.csv`, `type_A_to_G_status.csv`, `allowed_claims.md`,
`forbidden_claims.md`, `recommended_validation_design.md`, `audit_report.md`.
